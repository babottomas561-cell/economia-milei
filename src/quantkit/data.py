"""Price loading with a local CSV cache so every result in the repo is reproducible offline.

The first run downloads from Yahoo Finance and freezes the data in ``data/``; later runs
read the frozen file. Delete the file to refresh. Freezing matters: Yahoo revises adjusted
prices after dividends and splits, which would silently change published numbers.
"""

from __future__ import annotations

import hashlib
import warnings
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parents[2] / "data"


def _cache_path(tickers: list[str], start: str, end: str | None, field: str, adjusted: bool) -> Path:
    key = f"{','.join(sorted(tickers))}|{start}|{end}|{field}|{adjusted}"
    digest = hashlib.sha1(key.encode()).hexdigest()[:10]
    return DATA_DIR / f"{field.lower()}_{'adj' if adjusted else 'raw'}_{digest}.csv"


def load_prices(
    tickers: list[str],
    start: str = "2005-01-01",
    end: str | None = "2026-10-31",
    field: str = "Close",
    adjusted: bool = True,
    how: str = "any",
) -> pd.DataFrame:
    """Daily prices from Yahoo Finance, one column per ticker.

    ``adjusted=True`` returns dividend- and split-adjusted prices (for returns);
    ``adjusted=False`` returns the prices actually printed on the exchange (needed when
    two listings must be compared at the same moment, e.g. an ADR vs its local share).
    ``how="any"`` keeps only days where every ticker traded (a rectangular panel);
    ``how="all"`` keeps every day with at least one price.
    """
    path = _cache_path(tickers, start, end, field, adjusted)
    if path.exists():
        return pd.read_csv(path, index_col=0, parse_dates=True)[tickers]

    import yfinance as yf

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        raw = yf.download(tickers, start=start, end=end, auto_adjust=adjusted, progress=False)
    prices = raw[field].reindex(columns=tickers).dropna(how=how)
    missing = [t for t in tickers if prices[t].notna().sum() < 250]
    if missing:  # never freeze a partial download (Yahoo times out intermittently)
        raise RuntimeError(f"Download incomplete for {missing}; re-run to retry.")
    DATA_DIR.mkdir(exist_ok=True)
    prices.to_csv(path)
    return prices


def load_ohlcv(ticker: str, start: str = "2005-01-01", end: str | None = "2026-10-31") -> pd.DataFrame:
    """Adjusted OHLCV bars for a single ticker (columns: Open, High, Low, Close, Volume)."""
    fields = ["Open", "High", "Low", "Close", "Volume"]
    cols = {f: load_prices([ticker], start, end, field=f)[ticker] for f in fields}
    return pd.DataFrame(cols).dropna()


def load_panel(tickers: list[str], start: str = "2000-01-01", end: str | None = "2026-10-31",
               adjusted: bool = True) -> dict[str, pd.DataFrame]:
    """Open/High/Low/Close panels for many tickers, keeping each ticker's own history."""
    return {f: load_prices(tickers, start, end, field=f, adjusted=adjusted, how="all")
            for f in ["Open", "High", "Low", "Close"]}


def load_data912(tickers: list[str], kind: str = "bonds", field: str = "c") -> pd.DataFrame:
    """Daily closes from data912.com (BYMA prices), frozen to ``data/`` like ``load_prices``.

    Used for Argentine sovereign bonds, which Yahoo does not carry. The ``D`` tickers
    (GD30D, GD35D...) are quoted in dollars (MEP), so they compare directly with ADRs."""
    key = f"data912|{kind}|{','.join(sorted(tickers))}|{field}"
    path = DATA_DIR / f"data912_{kind}_{hashlib.sha1(key.encode()).hexdigest()[:10]}.csv"
    if path.exists():
        return pd.read_csv(path, index_col=0, parse_dates=True)[tickers]

    import requests

    cols = {}
    for t in tickers:
        resp = requests.get(f"https://data912.com/historical/{kind}/{t}", timeout=30)
        resp.raise_for_status()
        d = pd.DataFrame(resp.json())
        cols[t] = d.assign(date=pd.to_datetime(d["date"])).set_index("date")[field].sort_index()
    prices = pd.DataFrame(cols)
    DATA_DIR.mkdir(exist_ok=True)
    prices.to_csv(path)
    return prices


def _argentinadatos(endpoint: str, name: str, field: str = "valor") -> pd.Series:
    """One series from the public ArgentinaDatos API, frozen to ``data/{name}.csv``."""
    path = DATA_DIR / f"{name}.csv"
    if path.exists():
        return pd.read_csv(path, index_col=0, parse_dates=True)[name]

    import requests

    resp = requests.get(f"https://api.argentinadatos.com/v1/{endpoint}", timeout=30)
    resp.raise_for_status()
    d = pd.DataFrame(resp.json())
    s = d.assign(fecha=pd.to_datetime(d["fecha"])).set_index("fecha")[field].sort_index().rename(name)
    s = s[~s.index.duplicated(keep="last")]
    DATA_DIR.mkdir(exist_ok=True)
    s.to_frame().to_csv(path)
    return s


def load_riesgo_pais() -> pd.Series:
    """Riesgo país (spread EMBI de JP Morgan para Argentina, en puntos básicos), diario,
    desde la API pública de ArgentinaDatos. Congelado a ``data/`` como el resto."""
    return _argentinadatos("finanzas/indices/riesgo-pais", "riesgo_pais")


def load_inflacion() -> pd.Series:
    """Inflación mensual del IPC (INDEC), en % mensual; la fecha es el último día del mes."""
    return _argentinadatos("finanzas/indices/inflacion", "inflacion")


def load_bcra(variable: int, name: str, start: str = "2015-01-01", end: str = "2026-10-31") -> pd.Series:
    """One series from the BCRA's monetary statistics API (v4.0), frozen to ``data/{name}.csv``."""
    path = DATA_DIR / f"{name}.csv"
    if path.exists():
        return pd.read_csv(path, index_col=0, parse_dates=True)[name]

    import requests

    rows, offset, limit = [], 0, 1000
    while True:
        resp = requests.get(f"https://api.bcra.gob.ar/estadisticas/v4.0/monetarias/{variable}",
                            params={"desde": start, "hasta": end, "limit": limit, "offset": offset}, timeout=30)
        resp.raise_for_status()
        page = resp.json()["results"][0]["detalle"]
        rows += page
        if len(page) < limit:
            break
        offset += limit
    d = pd.DataFrame(rows)
    s = d.assign(fecha=pd.to_datetime(d["fecha"])).set_index("fecha")["valor"].sort_index().rename(name)
    DATA_DIR.mkdir(exist_ok=True)
    s.to_frame().to_csv(path)
    return s


def load_dolares() -> pd.DataFrame:
    """Dólar oficial mayorista (Comunicación A 3500 del BCRA), contado con liquidación y blue
    (ArgentinaDatos, venta): pesos por dólar, diario.

    El mayorista sale del BCRA y no de ArgentinaDatos: allí la serie queda congelada en
    366,45 del 11/12/2023 al 10/1/2024 y se pierde la devaluación del 13/12/2023."""
    return pd.concat([load_bcra(5, "dolar_a3500").rename("oficial"),
                      _argentinadatos("cotizaciones/dolares/contadoconliqui", "dolar_contadoconliqui", "venta").rename("CCL"),
                      _argentinadatos("cotizaciones/dolares/blue", "dolar_blue", "venta").rename("blue")], axis=1)


def load_series(ids: dict[str, str], start: str = "2016-01-01") -> pd.DataFrame:
    """Official statistics (INDEC, Hacienda, Trabajo) from the Series de Tiempo API of
    datos.gob.ar, one column per entry of ``ids`` ({our name: series id}), frozen to ``data/``.

    Every id in one call must share a frequency: when they differ, the API silently
    aggregates all of them to the lowest one (monthly CPI comes back as a quarterly mean)."""
    key = f"series|{start}|{','.join(f'{k}={v}' for k, v in sorted(ids.items()))}"
    path = DATA_DIR / f"series_{hashlib.sha1(key.encode()).hexdigest()[:10]}.csv"
    if path.exists():
        return pd.read_csv(path, index_col=0, parse_dates=True)[list(ids)]

    import requests

    resp = requests.get("https://apis.datos.gob.ar/series/api/series/",
                        params={"ids": ",".join(ids.values()), "start_date": start, "limit": 5000,
                                "format": "json"}, timeout=60)
    resp.raise_for_status()
    rows = resp.json()["data"]
    out = pd.DataFrame(rows, columns=["fecha", *ids]).assign(fecha=lambda d: pd.to_datetime(d["fecha"]))
    out = out.set_index("fecha").astype(float)
    empty = [k for k in ids if out[k].notna().sum() == 0]
    if empty:  # a wrong id returns an empty column instead of an error
        raise RuntimeError(f"No data for {empty}; check the ids.")
    DATA_DIR.mkdir(exist_ok=True)
    out.to_csv(path)
    return out
