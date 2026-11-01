"""Capítulo de análisis descriptivo: cada variable del scorecard, por gobierno (Macri,
Fernández, Milei), con tablas de estadística descriptiva, distribución de frecuencias,
gráficos y las pruebas que preparan el modelo econométrico (raíz unitaria, ACF/PACF,
estacionalidad y quiebres estructurales).

Reutiliza los loaders (datos congelados en ``data/``) y las transformaciones de
``estudio/run.py``. Genera las figuras en ``estudio/descriptivo/figuras/`` y escribe
``ANALISIS_DESCRIPTIVO.md`` a partir de ``plantilla.md``: el texto interpretativo vive en la
plantilla y cada ``{{clave}}`` se reemplaza por una tabla o un número calculado acá.

    uv run python estudio/descriptivo/descriptivo.py
"""

from __future__ import annotations

import re
import sys
import warnings
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tools.sm_exceptions import InterpolationWarning
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller, kpss, zivot_andrews

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
import run as base  # noqa: E402  (estudio/run.py: ids, IPC extendido, deflactor, helpers)

from quantkit import style  # noqa: E402
from quantkit.bonos import total_return  # noqa: E402
from quantkit.data import (load_bcra, load_data912, load_dolares, load_inflacion, load_prices,  # noqa: E402
                           load_riesgo_pais, load_series)

FIG = HERE / "figuras"
BASE_M = base.BASE_M

# El mes (o trimestre, o semestre) se asigna al gobierno que estaba en el cargo en su punto medio:
# diciembre de 2023 es de Milei (asumió el 10), el cuarto trimestre de 2023 es de Fernández.
GOBIERNOS = {"Macri": "2015-12-10", "Fernández": "2019-12-10", "Milei": "2023-12-10"}
ORDEN = list(GOBIERNOS)
COLOR = {"Macri": style.YELLOW, "Fernández": style.AQUA, "Milei": style.BLUE}
MITAD = {"D": 0, "M": 14, "Q": 45, "S": 91}
EVENTOS = {"2019-08-11": "PASO 2019", "2019-09-01": "Vuelve el cepo", "2020-03-20": "Cuarentena (ASPO)",
           "2021-11-14": "Legislativas 2021", "2023-11-19": "Balotaje 2023", "2023-12-13": "Devaluación (118%)",
           "2025-04-14": "Salida del cepo", "2025-09-07": "Elección en PBA", "2025-10-26": "Legislativas 2025"}
DESDE, HASTA = pd.Timestamp("2016-01-01"), pd.Timestamp("2026-12-31")
EXCLUIR_SHOCK = ("2023-11-01", "2024-03-31")   # devaluación y arrastre: fuera del cálculo de estacionalidad
INFL_DESDE = "2016-05-01"   # el INDEC volvió a publicar el IPC (GBA) en may-2016; ene-abr 2016 son de CABA

# Oferta y demanda globales a precios corrientes (millones de $, a tasa anual). La serie de
# exportaciones a precios corrientes (4.4_DGE_2004_T_26) viene vacía en la API: se obtiene por
# identidad, demanda global menos el resto de sus componentes.
DEMANDA_NOMINAL = {"pib": "4.4_OGP_2004_T_17", "demanda_global": "4.4_DGT_2004_T_20",
                   "consumo_privado": "4.4_DGCP_2004_T_27", "consumo_publico": "4.4_DGCP_2004_T_30",
                   "inversion": "4.4_DGI_2004_T_19", "importaciones": "4.4_OGI_2004_T_25",
                   "existencias": "4.4_DE_2004_T_24", "discrepancia": "4.4_VE_2004_T_21"}

# Valores críticos del test QLR (sup-F de Quandt-Andrews), 15% de recorte, q = 2 parámetros:
# Stock y Watson, "Introduction to Econometrics", tabla 14.5 (de Andrews, 1993/2003).
QLR_CRIT = {"10%": 5.00, "5%": 5.86, "1%": 7.78}


# ---------------------------------------------------------------- formato

def num(x: float, d: int = 1) -> str:
    """Número con coma decimal y punto de miles, como se escribe en español."""
    if x is None or pd.isna(x):
        return "–"
    return f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def md_tabla(df: pd.DataFrame, index: bool = True) -> str:
    """DataFrame (ya formateado como texto) a tabla Markdown, con la primera columna a la izquierda."""
    df = df.reset_index() if index else df
    cols = [str(c) for c in df.columns]
    lines = ["| " + " | ".join(cols) + " |", "|" + "|".join([":---"] + ["---:"] * (len(cols) - 1)) + "|"]
    lines += ["| " + " | ".join(str(v) for v in row) + " |" for row in df.to_numpy()]
    return "\n".join(lines)


def per(d: pd.Timestamp, freq: str) -> str:
    if freq == "Q":
        return f"T{d.quarter}-{d:%y}"
    if freq == "S":
        return f"S{1 if d.month <= 6 else 2}-{d:%y}"
    if freq == "D":
        return f"{d:%d/%m/%y}"
    return base.mes(d)


# ---------------------------------------------------------------- gobiernos

def gobierno(idx: pd.DatetimeIndex, freq: str) -> pd.Series:
    t = idx + pd.Timedelta(days=MITAD[freq])
    out = pd.Series(None, index=idx, dtype=object)
    for g, d in GOBIERNOS.items():
        out[t >= pd.Timestamp(d)] = g
    return out


def por_gobierno(s: pd.Series, freq: str) -> dict[str, pd.Series]:
    s = s.dropna()
    g = gobierno(s.index, freq)
    return {k: s[g == k] for k in ORDEN if (g == k).any()}


def describir(s: pd.Series) -> dict:
    s = s.dropna()
    media, desvio = s.mean(), s.std()
    return {"N": len(s), "Media": media, "Mediana": s.median(), "Desvío": desvio, "Mín": s.min(), "Máx": s.max(),
            # el CV solo tiene sentido en variables estrictamente positivas (niveles, no tasas que cambian de signo)
            "CV (%)": 100 * desvio / media if (s > 0).all() else np.nan,
            "Asimetría": s.skew(), "Curtosis": s.kurt()}


def tabla_descriptiva(s: pd.Series, freq: str, d: int = 1) -> tuple[str, pd.DataFrame]:
    """Estadística descriptiva por gobierno y para toda la muestra. La curtosis es en exceso
    (0 = normal); asimetría y curtosis son los estimadores insesgados de pandas."""
    grupos = por_gobierno(s, freq)
    s = s.dropna()
    s = s[gobierno(s.index, freq).notna()]
    grupos["Toda la muestra"] = s
    raw = pd.DataFrame({k: describir(v) for k, v in grupos.items()}).T
    txt = pd.DataFrame(index=raw.index)
    txt["Período"] = [f"{per(v.index[0], freq)} a {per(v.index[-1], freq)}" for v in grupos.values()]
    for c in raw.columns:
        txt[c] = [f"{int(v):,}".replace(",", ".") if c == "N" else num(v, 2 if c in ("Asimetría", "Curtosis") else d)
                  for v in raw[c]]
    txt.index.name = "Gobierno"
    return md_tabla(txt), raw


# ---------------------------------------------------------------- datos

def cargar() -> dict:
    m = load_series(base.MENSUAL)
    f = load_series(base.FISCAL)
    q = load_series(base.TRIMESTRAL)
    energia = load_series(base.SUBSIDIO_ENERGIA)["sub_energia"]
    dem_n = load_series(DEMANDA_NOMINAL)

    var = load_inflacion()
    var.index = var.index.to_period("M").to_timestamp()
    ipc = base.ipc_extendido(m["ipc"])
    # El IPC nacional arranca en dic-2016: se extiende hacia atrás hasta abr-2016 con las variaciones
    # del IPC-GBA del INDEC, para poder deflactar los salarios de casi todo el gobierno de Macri.
    for d in var.loc[INFL_DESDE:ipc.index[0]].index[::-1]:
        prev = d - pd.DateOffset(months=1)
        ipc.loc[prev] = ipc.loc[d] / (1 + var.loc[d] / 100)
    ipc = ipc.sort_index()

    s = {}
    s["infl_m"] = var.loc[INFL_DESDE:]
    s["infl_a"] = 100 * ipc.pct_change(12)
    s["log_ipc"] = np.log(ipc)
    for k in ["sal_priv_reg", "sal_publico", "sal_no_reg", "smvm"]:
        nominal = m[k].shift(-base.REZAGO_NO_REG) if k == "sal_no_reg" else m[k]
        r = base.real(nominal, ipc).loc[: ipc.index[-1]]
        s[k] = r
        s[f"d_{k}"] = 100 * r.pct_change()
        s[f"nom_{k}"] = nominal.reindex(r.index)              # mismo período que la serie real
        s[f"dn_{k}"] = 100 * s[f"nom_{k}"].pct_change()
    emae = (100 * m["emae"] / m["emae"].loc[BASE_M]).dropna()
    s["emae"], s["d_emae"] = emae, 100 * emae.pct_change()

    dol = load_dolares()
    of = dol["oficial"].resample("MS").mean()
    s["dep_oficial"] = 100 * of.pct_change()
    tcr = (of / ipc).dropna()
    s["tcr"] = 100 * tcr / tcr.loc[BASE_M]
    s["brecha"] = (100 * (dol["CCL"] / dol["oficial"] - 1)).resample("MS").mean()

    # Fiscal: flujos de 12 meses sobre el PBI nominal de los 4 trimestres correspondientes.
    # El PBI trimestral está a tasa anual: su promedio móvil de 12 meses es el PBI anual. Los dos
    # últimos meses fiscales (sin PBI publicado) usan el último PBI anual disponible.
    pib_m = q["pib_nominal"].dropna().resample("MS").ffill()
    pib_m = pib_m.reindex(pd.date_range(pib_m.index[0], pib_m.index[-1] + pd.DateOffset(months=2), freq="MS")).ffill()
    pib12 = pib_m.rolling(12).mean().reindex(f.index).ffill(limit=3)
    gasto = f["ing_primarios"] - f["sup_primario_spn"]
    s["res_primario"] = 100 * f["res_primario"].rolling(12).sum() / pib12
    s["res_financiero"] = 100 * (f["res_primario"] - f["intereses"]).rolling(12).sum() / pib12
    s["gasto_pib"] = 100 * gasto.rolling(12).sum() / pib12
    s["gasto_real"] = gasto / ipc
    s["d_gasto_real"] = 100 * s["gasto_real"].pct_change(12)

    # Trimestrales
    s["pib_real"] = q["pib_real"].dropna()
    s["ibif_real"] = q["ibif_real"].dropna()
    s["g_pib"] = 100 * s["pib_real"].pct_change(4)
    s["g_ibif"] = 100 * s["ibif_real"].pct_change(4)
    s["tasa_inv"] = 100 * dem_n["inversion"].rolling(4).sum() / dem_n["pib"].rolling(4).sum()
    s["sub_energia_pib"] = 100 * energia / (q["pib_nominal"] / 4)     # flujo del trimestre sobre el PBI del trimestre
    s["desocupacion"] = 100 * q["desocupacion"].dropna()
    s["pobreza"] = pd.Series({pd.Timestamp(f"{k[:4]}-{'01' if k[-1] == '1' else '07'}-01"): v
                              for k, v in base.POBREZA.items()})

    # Diarias
    rp = load_riesgo_pais()
    s["riesgo_pais"] = rp.loc["2015-12-10":]
    s["rp_completo"] = rp
    s["log_rp"] = np.log(rp.resample("MS").mean().loc["2016-01-01":])
    p = load_prices(base.AR + ["SPY", "EEM", "EWZ", "^MERV"], start="2019-01-01", how="all")
    px = p[base.AR].ffill().dropna()
    canasta = (px / px.iloc[0]).mean(axis=1)
    s["adr_canasta"] = canasta
    s["r_adr"] = 100 * np.log(canasta).diff()
    s["r_spy"] = 100 * np.log(p["SPY"].dropna()).diff()
    tr, _ = total_return(load_data912(base.BONOS).rename(columns=lambda c: c[:-1]))
    tr = tr.loc["2021-10-01":]                       # desde que cotizan los tres Globales
    s["r_bonos"] = 100 * tr.mean(axis=1)             # cartera equiponderada GD30/GD35/GD41, rebalanceo diario
    s["bonos_idx"] = 100 * np.exp(tr.mean(axis=1).fillna(0).cumsum())
    s["reservas"] = load_bcra(1, "reservas") / 1000
    return {"s": s, "m": m, "f": f, "q": q, "ipc": ipc, "energia": energia, "dem_n": dem_n, "dol": dol}


# ---------------------------------------------------------------- helpers de gráfico

def sombrear(ax: plt.Axes, etiquetas: bool = True, eventos: bool = True) -> None:
    """Fondo de color por gobierno y líneas punteadas numeradas en cada evento (ver EVENTOS)."""
    lims = [pd.Timestamp(d) for d in GOBIERNOS.values()] + [HASTA]
    for (g, _), d0, d1 in zip(GOBIERNOS.items(), lims[:-1], lims[1:]):
        ax.axvspan(d0, d1, color=COLOR[g], alpha=0.10, lw=0)
        if etiquetas:
            ax.annotate(g, xy=(d0, 0), xycoords=("data", "axes fraction"), xytext=(4, 4), textcoords="offset points",
                        va="bottom", fontsize=8.5, color=style.INK_2, fontweight="bold")
    if eventos:
        nivel, previo = 0, None
        for i, d in enumerate(EVENTOS, 1):
            d = pd.Timestamp(d)
            nivel = nivel + 1 if previo is not None and (d - previo).days < 150 else 0   # escalona eventos cercanos
            previo = d
            ax.axvline(d, color=style.INK_2, lw=0.7, ls=":", alpha=0.8)
            ax.annotate(str(i), xy=(d, 1), xycoords=("data", "axes fraction"), xytext=(0, -2 - 13 * nivel),
                        textcoords="offset points", ha="center", va="top", fontsize=7.5, color=style.INK_2,
                        bbox={"boxstyle": "circle,pad=0.15", "fc": style.SURFACE, "ec": style.BASELINE, "lw": 0.6})
    ax.set_xlim(DESDE, HASTA)
    ax.xaxis.set_major_locator(mdates.YearLocator(2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))


def nota_eventos() -> str:
    return "Eventos: " + " · ".join(f"{i} {n} ({pd.Timestamp(d):%d/%m/%y})" for i, (d, n) in enumerate(EVENTOS.items(), 1))


def leyenda_gobiernos(fig: plt.Figure, y: float = 1.0) -> None:
    handles = [plt.Rectangle((0, 0), 1, 1, color=COLOR[g], alpha=0.35) for g in ORDEN]
    fig.legend(handles, [f"{g} (desde {pd.Timestamp(d):%m/%Y})" for g, d in GOBIERNOS.items()], loc="upper right",
               ncols=3, bbox_to_anchor=(0.99, y), fontsize=9.5)


# ---------------------------------------------------------------- figuras: series largas

def fig_series_precios(s: dict) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    a = axes[0, 0]
    v = s["infl_m"]
    a.bar(v.index, v, width=25, color=[COLOR[g] for g in gobierno(v.index, "M")])
    a.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
    a.set_title("Inflación mensual")
    style.subtitle(a, "IPC, variación % mensual")
    sombrear(a)
    a = axes[0, 1]
    y = s["infl_a"].dropna()
    a.plot(y.index, y, color=style.INK)
    a.set_yscale("log")
    a.set_yticks([10, 20, 30, 50, 100, 200, 300])
    a.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"{x:.0f}%"))
    a.minorticks_off()
    a.set_title("Inflación interanual")
    style.subtitle(a, "Variación % contra el mismo mes del año anterior (escala log)")
    sombrear(a)
    a = axes[1, 0]
    for k, name, color in [("sal_priv_reg", "Privado registrado", style.INK), ("sal_publico", "Público", style.ORANGE),
                           ("sal_no_reg", "No registrado", style.MUTED)]:
        a.plot(s[k].index, s[k], color=color, lw=1.8, label=name)
    a.axhline(100, color=style.INK_2, lw=0.8)
    a.set_title("Salario real")
    style.subtitle(a, "Índice de salarios del INDEC deflactado por el IPC, nov-2023 = 100")
    a.legend(loc="upper right", bbox_to_anchor=(1, 0.93), fontsize=9)
    sombrear(a)
    a = axes[1, 1]
    a.plot(s["smvm"].index, s["smvm"], color=style.VIOLET, label="Salario mínimo")
    a.plot(s["tcr"].index, s["tcr"], color=style.GREEN, lw=1.6, label="Dólar oficial real")
    a.axhline(100, color=style.INK_2, lw=0.8)
    a.set_title("Salario mínimo y tipo de cambio real")
    style.subtitle(a, "Deflactados por el IPC, nov-2023 = 100")
    a.legend(loc="upper left", bbox_to_anchor=(0, 0.93), fontsize=9)
    sombrear(a)
    fig.subplots_adjust(hspace=0.42)
    leyenda_gobiernos(fig, 1.02)
    style.source(fig, "Fuente: INDEC (IPC, índice de salarios), Ministerio de Trabajo (SMVM) y BCRA (Com. A 3500). "
                      "El salario no registrado se corre 5 meses (rezago de publicación).\n" + nota_eventos())
    style.save(fig, FIG / "D01_series_precios_salarios.png")


def fig_series_actividad(s: dict) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    a = axes[0, 0]
    a.plot(s["emae"].index, s["emae"], color=style.INK)
    a.axhline(100, color=style.INK_2, lw=0.8)
    a.set_title("Actividad económica mensual (EMAE)")
    style.subtitle(a, "Desestacionalizado, nov-2023 = 100")
    sombrear(a)
    a = axes[0, 1]
    for k, name, color in [("g_pib", "PBI", style.INK), ("g_ibif", "Inversión (IBIF)", style.GREEN)]:
        a.plot(s[k].index + pd.DateOffset(days=45), s[k], color=color, marker="o", ms=3, lw=1.6, label=name)
    a.axhline(0, color=style.INK_2, lw=0.8)
    a.set_ylim(-45, 50)          # el rebote de 2021 tras la cuarentena (IBIF +70%) se recorta
    a.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
    a.set_title("PBI e inversión")
    style.subtitle(a, "Variación % interanual del trimestre, precios de 2004 (eje recortado en ±45%)")
    a.legend(loc="upper left", fontsize=9)
    sombrear(a)
    a = axes[1, 0]
    for k, name, color in [("res_primario", "Primario", style.BLUE), ("res_financiero", "Financiero", style.ORANGE)]:
        a.plot(s[k].index, s[k], color=color, label=name)
    a.axhline(0, color=style.INK_2, lw=0.8)
    a.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
    a.set_title("Resultado fiscal")
    style.subtitle(a, "Sector Público Nacional, base caja, suma de 12 meses, % del PBI")
    a.legend(loc="lower left", fontsize=9)
    sombrear(a)
    a = axes[1, 1]
    a.plot(s["pobreza"].index + pd.DateOffset(months=3), s["pobreza"], color=style.RED, marker="o", ms=4, label="Pobreza")
    a.plot(s["desocupacion"].index + pd.DateOffset(days=45), s["desocupacion"], color=style.VIOLET, marker="o", ms=3,
           lw=1.4, label="Desocupación")
    a.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
    a.set_ylim(0, 60)
    a.set_title("Pobreza y desocupación")
    style.subtitle(a, "% de personas (pobreza, semestral) y % de la PEA (desocupación, trimestral)")
    a.legend(loc="upper left", fontsize=9)
    sombrear(a)
    fig.subplots_adjust(hspace=0.42)
    leyenda_gobiernos(fig, 1.02)
    style.source(fig, "Fuente: INDEC (EMAE, cuentas nacionales, EPH) y Secretaría de Hacienda (IMIG).\n" + nota_eventos())
    style.save(fig, FIG / "D02_series_actividad_fiscal_social.png")


def fig_series_mercados(s: dict) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    a = axes[0, 0]
    rp = s["riesgo_pais"]
    a.plot(rp.index, rp, color=style.INK, lw=1.2)
    a.set_yscale("log")
    a.set_yticks([300, 500, 1000, 2000, 3000, 5000])
    a.yaxis.set_major_formatter(mtick.FuncFormatter(lambda v, _: f"{v:,.0f}".replace(",", ".")))
    a.minorticks_off()
    a.set_title("Riesgo país")
    style.subtitle(a, "Spread EMBI de JP Morgan, puntos básicos (escala log)")
    sombrear(a)
    a = axes[0, 1]
    c = 100 * s["adr_canasta"]
    spy = s["r_spy"].dropna().cumsum()
    a.plot(c.index, c, color=style.BLUE, lw=1.4, label="13 ADRs argentinos")
    a.plot(spy.index, 100 * np.exp(spy / 100), color=style.MUTED, lw=1.2, label="S&P 500")
    a.set_yscale("log")
    a.set_yticks([25, 50, 100, 200, 400])
    a.yaxis.set_major_formatter(mtick.ScalarFormatter())
    a.minorticks_off()
    a.set_title("Acciones argentinas en dólares")
    style.subtitle(a, "Canasta equiponderada de ADRs, 2/1/2019 = 100 (escala log)")
    a.legend(loc="upper left", fontsize=9)
    sombrear(a)
    a = axes[1, 0]
    b = s["bonos_idx"]
    a.plot(b.index, b, color=style.AQUA, lw=1.4)
    a.axhline(100, color=style.INK_2, lw=0.8)
    a.set_title("Bonos soberanos en dólares")
    style.subtitle(a, "Retorno total de una cartera GD30/GD35/GD41, 1/10/2021 = 100")
    sombrear(a)
    a = axes[1, 1]
    a.plot(s["reservas"].index, s["reservas"], color=style.GREEN, lw=1.4, label="Reservas brutas (US$ miles de M)")
    a2 = a.twinx()
    br = s["brecha"].loc["2016-01-01":]
    a2.plot(br.index, br, color=style.ORANGE, lw=1.4, label="Brecha CCL/oficial (%, eje derecho)")
    a2.grid(False)
    a2.spines["right"].set_visible(True)
    a2.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
    a.set_title("Reservas y brecha cambiaria")
    style.subtitle(a, "Reservas brutas del BCRA y brecha promedio mensual")
    h1, l1 = a.get_legend_handles_labels()
    h2, l2 = a2.get_legend_handles_labels()
    a.legend(h1 + h2, l1 + l2, loc="upper left", fontsize=9)
    sombrear(a)
    fig.subplots_adjust(hspace=0.42)
    leyenda_gobiernos(fig, 1.02)
    style.source(fig, "Fuente: JP Morgan vía ArgentinaDatos, Yahoo Finance, BYMA vía data912, BCRA.\n" + nota_eventos())
    style.save(fig, FIG / "D03_series_mercados.png")


# ---------------------------------------------------------------- distribución de la inflación

BINS = [0, 1, 2, 3, 4, 5, 7.5, 10, 15, 30]


def tabla_frecuencias(v: pd.Series) -> pd.DataFrame:
    """Distribución de frecuencias con intervalos [a, b) fijos y comunes a los tres gobiernos,
    para que las frecuencias relativas se puedan comparar entre ellos."""
    cats = pd.cut(v, BINS, right=False)
    fa = cats.value_counts().reindex(cats.cat.categories, fill_value=0)
    out = pd.DataFrame({"Marca de clase": [(i.left + i.right) / 2 for i in fa.index], "Frec. absoluta": fa.to_numpy(),
                        "Frec. relativa (%)": 100 * fa.to_numpy() / fa.sum()})
    out["Frec. abs. acumulada"] = out["Frec. absoluta"].cumsum()
    out["Frec. rel. acumulada (%)"] = out["Frec. relativa (%)"].cumsum()
    out.index = [f"[{num(i.left, 1 if i.left % 1 else 0)}; {num(i.right, 1 if i.right % 1 else 0)})" for i in fa.index]
    out.index.name = "Inflación mensual (%)"
    return out


def fmt_frecuencias(t: pd.DataFrame) -> str:
    txt = pd.DataFrame(index=t.index)
    txt["Marca de clase"] = [num(x, 2) for x in t["Marca de clase"]]
    txt["Frec. absoluta"] = t["Frec. absoluta"].astype(int)
    txt["Frec. relativa (%)"] = [num(x, 1) for x in t["Frec. relativa (%)"]]
    txt["Frec. abs. acumulada"] = t["Frec. abs. acumulada"].astype(int)
    txt["Frec. rel. acumulada (%)"] = [num(x, 1) for x in t["Frec. rel. acumulada (%)"]]
    total = pd.DataFrame({"Marca de clase": [""], "Frec. absoluta": [int(t["Frec. absoluta"].sum())],
                          "Frec. relativa (%)": ["100,0"], "Frec. abs. acumulada": [""], "Frec. rel. acumulada (%)": [""]},
                         index=["**Total**"])
    return md_tabla(pd.concat([txt, total]).rename_axis(t.index.name))


def fig_histogramas(s: dict) -> dict:
    grupos = por_gobierno(s["infl_m"], "M")
    fig, axes = plt.subplots(1, 3, figsize=(16, 5), sharey=True)
    out = {}
    for a, (g, v) in zip(axes, grupos.items()):
        t = tabla_frecuencias(v)
        out[g] = t
        # Intervalos de ancho distinto: el histograma grafica densidad (frecuencia relativa / ancho)
        # para que el área, no la altura, sea proporcional a la frecuencia.
        a.hist(v, bins=BINS, density=True, color=COLOR[g], edgecolor=style.SURFACE, lw=1.2)
        a.axvline(v.mean(), color=style.INK, lw=1.2, ls="--")
        a.axvline(v.median(), color=style.INK, lw=1.2, ls=":")
        a.annotate(f"media {num(v.mean(), 1)}%\nmediana {num(v.median(), 1)}%", xy=(0.97, 0.95), xycoords="axes fraction",
                   ha="right", va="top", fontsize=9.5)
        a.set_xlim(0, 30)
        a.set_xticks([0, 2, 4, 5, 10, 15, 20, 25, 30])
        a.xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"{x:g}%"))
        a.set_title(f"{g} (N = {len(v)})")
        style.subtitle(a, f"{per(v.index[0], 'M')} a {per(v.index[-1], 'M')}")
        a.set_xlabel("Inflación mensual")
    axes[0].set_ylabel("Densidad (frecuencia relativa / ancho del intervalo)")
    style.source(fig, "Fuente: INDEC. Intervalos comunes [0;1), [1;2) … [15;30). Línea rayada: media; punteada: mediana.")
    style.save(fig, FIG / "D04_histogramas_inflacion.png")
    return out


# ---------------------------------------------------------------- barras

def variacion_por_gobierno(s: dict) -> pd.DataFrame:
    """Variación acumulada y anualizada de cada variable entre el último dato del gobierno
    anterior y el último dato del propio (o el último disponible)."""
    specs = {"IPC (inflación)": (np.exp(s["log_ipc"]), "M"), "Salario real privado registrado": (s["sal_priv_reg"], "M"),
             "Salario real público": (s["sal_publico"], "M"), "Salario real no registrado": (s["sal_no_reg"], "M"),
             "Salario mínimo real": (s["smvm"], "M"), "Actividad (EMAE)": (s["emae"], "M"),
             "PBI (4 trimestres)": (s["pib_real"].rolling(4).mean(), "Q"),
             "Inversión (4 trimestres)": (s["ibif_real"].rolling(4).mean(), "Q"), "Dólar oficial real": (s["tcr"], "M"),
             "Riesgo país": (s["rp_completo"], "D")}
    return variaciones(specs)


def variaciones(specs: dict[str, tuple[pd.Series, str]]) -> pd.DataFrame:
    rows = []
    for name, (v, freq) in specs.items():
        v = v.dropna()
        g = gobierno(v.index, freq)
        for gob in ORDEN:
            dentro = v[g == gob]
            if dentro.empty:
                continue
            antes = v[v.index < dentro.index[0]]
            ini = antes.iloc[-1] if len(antes) else dentro.iloc[0]
            d0 = antes.index[-1] if len(antes) else dentro.index[0]
            d1 = dentro.index[-1]
            anios = (d1 - d0).days / 365.25
            acum = 100 * (dentro.iloc[-1] / ini - 1)
            rows.append({"Variable": name, "Gobierno": gob, "Desde": per(d0, freq), "Hasta": per(d1, freq),
                         "Años": anios, "Acumulada (%)": acum,
                         "Anualizada (%)": 100 * ((1 + acum / 100) ** (1 / anios) - 1),
                         "completo": len(antes) > 0 and (gob != "Macri" or d0 <= pd.Timestamp("2016-01-01"))})
    return pd.DataFrame(rows)


def fig_barras(s: dict, desc: dict, var: pd.DataFrame) -> None:
    # Promedios por gobierno
    specs = [("infl_m", "Inflación mensual", "%"), ("d_sal_priv_reg", "Var. mensual del salario real privado", "%"),
             ("g_pib", "Crecimiento interanual del PBI", "%"), ("res_primario", "Resultado primario", "% PBI"),
             ("desocupacion", "Desocupación", "% PEA"), ("pobreza", "Pobreza", "% personas")]
    fig, axes = plt.subplots(2, 3, figsize=(16, 9))
    for a, (k, titulo, unidad) in zip(axes.flat, specs):
        raw = desc[k].loc[ORDEN]
        a.bar(range(len(ORDEN)), raw["Media"], color=[COLOR[g] for g in ORDEN], width=0.6,
                     yerr=raw["Desvío"] / np.sqrt(raw["N"]), capsize=4, error_kw={"color": style.INK_2, "lw": 1})
        # El valor va debajo del nombre del gobierno: arriba de la barra choca con la barra de error
        a.set_xticks(range(len(ORDEN)), [f"{g}\n{num(v, 2 if abs(v) < 1 else 1)}" for g, v in zip(ORDEN, raw["Media"])])
        a.axhline(0, color=style.INK_2, lw=0.8)
        a.grid(axis="x", visible=False)
        a.set_title(titulo)
        style.subtitle(a, f"Media del período ({unidad}) ± 1 error estándar")
    fig.subplots_adjust(hspace=0.45)
    style.source(fig, "Fuente: INDEC y Secretaría de Hacienda. El error estándar (desvío/√N) supone observaciones "
                      "independientes: con series persistentes subestima la incertidumbre real.")
    style.save(fig, FIG / "D05_barras_promedios.png")

    # Variación acumulada y anualizada
    fig, (a, b) = plt.subplots(1, 2, figsize=(16, 6.2), gridspec_kw={"width_ratios": [1, 2.4]})
    ipc = var[var["Variable"] == "IPC (inflación)"].set_index("Gobierno")
    x = np.arange(len(ipc))
    w = 0.38
    for i, (col, alpha) in enumerate([("Acumulada (%)", 1.0), ("Anualizada (%)", 0.55)]):
        bars = a.bar(x + (i - 0.5) * w, ipc[col], width=w, color=[COLOR[g] for g in ipc.index], alpha=alpha,
                     label=col.replace(" (%)", ""))
        for bar, v in zip(bars, ipc[col]):
            a.annotate(f"{num(v, 0)}%", xy=(bar.get_x() + w / 2, v), xytext=(0, 3), textcoords="offset points",
                       ha="center", va="bottom", fontsize=8.5)
    a.set_xticks(x, ipc.index)
    a.set_yscale("log")
    a.yaxis.set_major_formatter(mtick.FuncFormatter(lambda v, _: f"{num(v, 0)}%"))
    a.minorticks_off()
    a.grid(axis="x", visible=False)
    a.set_title("Inflación por gobierno")
    style.subtitle(a, "Acumulada (barra llena) y anualizada (clara), escala log")
    reales = [v for v in var["Variable"].unique() if v not in ("IPC (inflación)", "Riesgo país")]
    t = var[var["Variable"].isin(reales)].pivot(index="Variable", columns="Gobierno", values="Anualizada (%)")
    t = t.loc[reales, ORDEN]
    y = np.arange(len(t))
    h = 0.26
    for i, g in enumerate(ORDEN):
        b.barh(y + (1 - i) * h, t[g], height=h, color=COLOR[g], label=g)
        for yi, v in zip(y + (1 - i) * h, t[g]):
            b.annotate(f"{v:+.1f}".replace(".", ","), xy=(v, yi), xytext=(3 if v >= 0 else -3, 0), textcoords="offset points",
                       ha="left" if v >= 0 else "right", va="center", fontsize=8)
    b.set_yticks(y, t.index)
    b.invert_yaxis()
    b.axvline(0, color=style.INK_2, lw=0.8)
    b.grid(axis="y", visible=False)
    b.xaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
    b.set_title("Variación real anualizada por gobierno")
    style.subtitle(b, "% por año entre el último dato del gobierno anterior y el último del propio")
    b.legend(loc="lower right", reverse=True)
    fig.subplots_adjust(wspace=0.55)
    style.source(fig, "Fuente: INDEC, Ministerio de Trabajo, BCRA. Anualizar corrige que Milei lleva menos tiempo. "
                      "Macri: salarios desde abr-16 e inflación desde may-16 (no hay IPC del INDEC antes).")
    style.save(fig, FIG / "D06_barras_variacion_por_gobierno.png")


# ---------------------------------------------------------------- salario nominal contra real

SALARIOS = {"sal_priv_reg": "Privado registrado", "sal_publico": "Público", "sal_no_reg": "No registrado",
            "smvm": "Salario mínimo"}


def nominal_vs_real(s: dict) -> pd.DataFrame:
    """Descompone la variación de cada salario por gobierno: (1 + real) = (1 + nominal) / (1 + inflación),
    con la inflación medida en exactamente la misma ventana que el salario."""
    ipc = np.exp(s["log_ipc"])
    rows = []
    for k, nombre in SALARIOS.items():
        nom = variaciones({nombre: (s[f"nom_{k}"], "M")}).set_index("Gobierno")
        for gob, r in nom.iterrows():
            # ventana idéntica a la del salario: del último dato del gobierno anterior (o el primero) al último propio
            v = s[f"nom_{k}"].dropna()
            g = gobierno(v.index, "M")
            dentro = v[g == gob]
            antes = v[v.index < dentro.index[0]]
            d0 = antes.index[-1] if len(antes) else dentro.index[0]
            pi = 100 * (ipc.loc[dentro.index[-1]] / ipc.loc[d0] - 1)
            real_ = 100 * ((1 + r["Acumulada (%)"] / 100) / (1 + pi / 100) - 1)
            anual = lambda x: 100 * ((1 + x / 100) ** (1 / r["Años"]) - 1)  # noqa: E731
            rows.append({"Salario": nombre, "Gobierno": gob, "Desde": r["Desde"], "Hasta": r["Hasta"],
                         "Nominal acum. (%)": r["Acumulada (%)"], "Inflación acum. (%)": pi, "Real acum. (%)": real_,
                         "Nominal anual (%)": r["Anualizada (%)"], "Inflación anual (%)": anual(pi),
                         "Real anual (%)": anual(real_), "completo": r["completo"]})
    return pd.DataFrame(rows)


def fig_nominal(s: dict, nr: pd.DataFrame) -> None:
    fig, (a, b) = plt.subplots(1, 2, figsize=(16, 5.8), gridspec_kw={"width_ratios": [1.25, 1]})
    desde = "2022-01-01"
    inf = s["infl_m"].loc[desde:]
    a.bar(inf.index, inf, width=25, color=style.BASELINE, label="Inflación (IPC)")
    # El salario mínimo queda fuera de este panel: se ajusta por escalones y sus ceros mensuales tapan a los demás
    for k, color in [("sal_priv_reg", style.INK), ("sal_publico", style.ORANGE)]:
        dn = s[f"dn_{k}"].loc[desde:]
        a.plot(dn.index, dn, color=color, lw=1.6, marker="o", ms=2.5, label=f"Salario {SALARIOS[k].lower()} (nominal)")
    a.axvline(pd.Timestamp("2023-12-01"), color=style.BLUE, lw=1, ls="--", alpha=0.7)
    a.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
    a.set_title("Salario nominal contra inflación, mes a mes")
    style.subtitle(a, "Variación % mensual. Cuando la línea queda debajo de la barra, el salario real cae")
    a.legend(loc="upper right", fontsize=9)
    a.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 7]))
    a.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y"))

    t = nr.set_index(["Salario", "Gobierno"])
    x = np.arange(len(ORDEN))
    w = 0.2
    for i, (nombre, color) in enumerate(zip(SALARIOS.values(), [style.INK, style.ORANGE, style.MUTED, style.VIOLET])):
        vals = [t.loc[(nombre, g), "Nominal anual (%)"] for g in ORDEN]
        b.bar(x + (i - 1.5) * w, vals, width=w, color=color, label=nombre)
    pi = [t.loc[("Privado registrado", g), "Inflación anual (%)"] for g in ORDEN]
    for xi, p_ in zip(x, pi):
        b.hlines(p_, xi - 2 * w, xi + 2 * w, color=style.RED, lw=2.2)
        b.annotate(f"inflación {num(p_, 0)}%", xy=(xi, p_), xytext=(0, 4), textcoords="offset points", ha="center",
                   va="bottom", fontsize=9, color=style.RED, fontweight="bold")
    b.set_xticks(x, ORDEN)
    b.grid(axis="x", visible=False)
    b.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
    b.set_title("Aumento nominal anualizado por gobierno")
    style.subtitle(b, "% por año; la línea roja es la inflación anualizada de la misma ventana")
    b.legend(loc="upper left", fontsize=9)
    style.source(fig, "Fuente: INDEC (índice de salarios, IPC) y Ministerio de Trabajo (SMVM). Real = (1 + nominal) / (1 + inflación) − 1. "
                      "Macri desde abr-16; el no registrado, corrido 5 meses\n(su ventana con Milei termina en feb-26, con una inflación anualizada de 81%; la línea roja usa la del privado registrado).")
    style.save(fig, FIG / "D13_salario_nominal_vs_real.png")


# ---------------------------------------------------------------- tortas

def composicion_gasto(f: pd.DataFrame, energia: pd.Series) -> pd.DataFrame:
    """Estructura del gasto primario por rubro (% del total, pesos corrientes del año)."""
    cap = [c for c in f.columns if c.startswith("cap_")] + ["fondo_sojero"]
    comp = f.assign(capital=f[cap].sum(axis=1, min_count=1), gasto=f["ing_primarios"] - f["sup_primario_spn"])
    anual = comp.groupby(comp.index.year).sum(min_count=1)
    anual["sub_energia"] = energia.groupby(energia.index.year).sum()
    out = {}
    for y in [2023, 2025]:
        r = {k: anual.loc[y, c] for k, c in base.RUBROS.items()}
        r["Resto del gasto primario"] = anual.loc[y, "gasto"] - sum(r.values())
        out[y] = 100 * pd.Series(r) / anual.loc[y, "gasto"]
    return pd.DataFrame(out)


def composicion_demanda(d: pd.DataFrame) -> pd.DataFrame:
    """Usos del PBI a precios corrientes (% del PBI): C + G + I + X + existencias − M = PBI."""
    # Hasta 2023 el INDEC publica la variación de existencias dentro de la discrepancia estadística.
    d = d.assign(existencias=d["existencias"].fillna(0) + d["discrepancia"])
    d = d.assign(exportaciones=d["demanda_global"] - d[["consumo_privado", "consumo_publico", "inversion",
                                                        "existencias"]].sum(axis=1))
    anual = d.groupby(d.index.year).mean()[d.groupby(d.index.year).count()["pib"] == 4]
    cols = {"consumo_privado": "Consumo privado", "consumo_publico": "Consumo público", "inversion": "Inversión (IBIF)",
            "exportaciones": "Exportaciones", "importaciones": "Importaciones",
            "existencias": "Existencias y discrepancia"}
    return (100 * anual[list(cols)].div(anual["pib"], axis=0)).rename(columns=cols).loc[[2017, 2019, 2023, 2025]].T


def fig_tortas(gasto: pd.DataFrame, dem: pd.DataFrame) -> None:
    colores = [style.BLUE, style.AQUA, style.GREEN, style.VIOLET, style.ORANGE, style.YELLOW, style.MAGENTA, style.RED,
               style.BASELINE]
    fig, axes = plt.subplots(1, 2, figsize=(15, 7))
    for a, y in zip(axes, gasto.columns):
        v = gasto[y]
        wedges, _, autot = a.pie(v, colors=colores, startangle=90, counterclock=False, autopct=lambda p: f"{num(p, 1)}%",
                                 pctdistance=0.78, wedgeprops={"edgecolor": style.SURFACE, "lw": 1.5, "width": 0.45},
                                 textprops={"fontsize": 9})
        for t_, p in zip(autot, v):
            t_.set_visible(p >= 2.5)
        a.set_title(f"{y}", loc="center", fontsize=15)
    fig.legend(wedges, [f"{k}" for k in gasto.index], loc="lower center", ncols=3, fontsize=10, bbox_to_anchor=(0.5, 0.0))
    fig.suptitle("Estructura del gasto primario del Estado nacional, antes y después del ajuste", x=0.01, y=0.99,
                 ha="left", fontweight="bold", fontsize=14)
    fig.subplots_adjust(top=0.86, bottom=0.17)
    style.source(fig, "Fuente: Secretaría de Hacienda (IMIG, Sector Público Nacional no financiero, base caja). "
                      "% del gasto primario del año, en pesos corrientes. Porciones menores a 2,5% sin etiqueta.")
    style.save(fig, FIG / "D07_tortas_gasto.png")

    usos = ["Consumo privado", "Consumo público", "Inversión (IBIF)", "Exportaciones"]
    fig, axes = plt.subplots(1, 2, figsize=(15, 7))
    for a, y in zip(axes, [2023, 2025]):
        v = dem.loc[usos, y]
        wedges, _, _ = a.pie(v, colors=[style.BLUE, style.VIOLET, style.GREEN, style.AQUA], startangle=90,
                             counterclock=False, autopct=lambda p: f"{num(p, 1)}%", pctdistance=0.78,
                             wedgeprops={"edgecolor": style.SURFACE, "lw": 1.5, "width": 0.45}, textprops={"fontsize": 10})
        a.set_title(str(y), loc="center", fontsize=15)
        a.annotate(f"Importaciones:\n{num(dem.loc['Importaciones', y], 1)}% del PBI", xy=(0.5, 0.5), xycoords="axes fraction",
                   ha="center", va="center", fontsize=10, color=style.INK_2)
    fig.legend(wedges, usos, loc="lower center", ncols=4, fontsize=10, bbox_to_anchor=(0.5, 0.0))
    fig.suptitle("Composición de la demanda final por componente", x=0.01, y=0.99, ha="left", fontweight="bold", fontsize=14)
    fig.subplots_adjust(top=0.86, bottom=0.1)
    style.source(fig, "Fuente: INDEC, oferta y demanda globales a precios corrientes. % de la suma C + G + I + X; las "
                      "importaciones (centro) y la variación de existencias quedan fuera de la torta. Exportaciones por identidad.")
    style.save(fig, FIG / "D08_tortas_demanda.png")


# ---------------------------------------------------------------- boxplots

def fig_boxplots(s: dict) -> None:
    specs = [("infl_m", "M", "Inflación mensual (%)"), ("d_sal_priv_reg", "M", "Var. mensual salario real privado (%)"),
             ("d_emae", "M", "Var. mensual del EMAE (%)"), ("g_pib", "Q", "PBI, var. interanual (%)"),
             ("res_primario", "M", "Resultado primario 12m (% PBI)"), ("riesgo_pais", "D", "Riesgo país (pb, escala log)")]
    fig, axes = plt.subplots(2, 3, figsize=(16, 9))
    for a, (k, freq, titulo) in zip(axes.flat, specs):
        g = por_gobierno(s[k], freq)
        bp = a.boxplot(list(g.values()), tick_labels=list(g), patch_artist=True, widths=0.55,
                       medianprops={"color": style.INK, "lw": 1.6}, whiskerprops={"color": style.INK_2},
                       capprops={"color": style.INK_2},
                       flierprops={"marker": "o", "ms": 3, "mfc": style.MUTED, "mec": "none", "alpha": 0.6})
        for patch, gob in zip(bp["boxes"], g):
            patch.set_facecolor(COLOR[gob])
            patch.set_alpha(0.75)
            patch.set_edgecolor(style.INK_2)
        if k == "riesgo_pais":
            a.set_yscale("log")
            a.set_yticks([400, 700, 1000, 2000, 4000])
            a.yaxis.set_major_formatter(mtick.FuncFormatter(lambda v, _: f"{v:,.0f}".replace(",", ".")))
            a.yaxis.set_minor_formatter(mtick.NullFormatter())
        if k in ("d_sal_priv_reg", "d_emae", "g_pib", "res_primario"):
            a.axhline(0, color=style.INK_2, lw=0.8)
        a.grid(axis="x", visible=False)
        a.set_title(titulo, fontsize=12.5)
    fig.subplots_adjust(hspace=0.35)
    style.source(fig, "Caja: rango intercuartil (P25-P75); línea: mediana; bigotes: 1,5 × RIC; puntos: valores atípicos. "
                      "Fuente: INDEC, Hacienda, JP Morgan.")
    style.save(fig, FIG / "D09_boxplots.png")


# ---------------------------------------------------------------- preparación para el modelo

def raiz_unitaria(s: dict) -> tuple[str, pd.DataFrame]:
    """ADF (H0: raíz unitaria) y KPSS (H0: estacionaria) en niveles y en primeras diferencias.
    Usarlas juntas evita leer la falta de rechazo de una sola como prueba de lo contrario."""
    m0 = "2016-06-01"
    specs = {"Inflación mensual (%)": (s["infl_m"], "c"), "Inflación interanual (%)": (s["infl_a"].loc[m0:], "c"),
             "log IPC": (s["log_ipc"], "ct"), "log salario real privado registrado": (np.log(s["sal_priv_reg"]), "c"),
             "log salario real público": (np.log(s["sal_publico"]), "c"),
             "log salario real no registrado": (np.log(s["sal_no_reg"].dropna()), "c"),
             "log EMAE": (np.log(s["emae"].loc[m0:]), "c"), "Depreciación mensual oficial (%)": (s["dep_oficial"].loc[m0:], "c"),
             "log tipo de cambio real": (np.log(s["tcr"]), "c"), "Resultado primario 12m (% PBI)": (s["res_primario"], "c"),
             "log riesgo país (prom. mensual)": (s["log_rp"], "c"),
             "log PBI real (trimestral)": (np.log(s["pib_real"]), "ct"), "log IBIF real (trimestral)": (np.log(s["ibif_real"]), "ct")}
    rows = []
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", InterpolationWarning)
        warnings.simplefilter("ignore", FutureWarning)   # statsmodels 0.15 avisa que cambiará el tipo de retorno
        for name, (x, reg) in specs.items():
            x = x.dropna()
            res = {"Variable": name, "Det.": reg, "N": len(x)}
            for etapa, serie, r in [("nivel", x, reg), ("dif.", x.diff().dropna(), "c")]:
                adf = adfuller(serie, regression=r, autolag="AIC")
                kp = kpss(serie, regression=r, nlags="auto")
                res[f"ADF {etapa}"], res[f"p ADF {etapa}"] = adf[0], adf[1]
                res[f"KPSS {etapa}"], res[f"p KPSS {etapa}"] = kp[0], kp[1]
            rows.append(res)
    t = pd.DataFrame(rows).set_index("Variable")

    def veredicto(p_adf: float, p_kpss: float) -> str:
        if p_adf < 0.05 and p_kpss > 0.05:
            return "I(0)"
        if p_adf >= 0.05 and p_kpss <= 0.05:
            return "raíz unitaria"
        return "ambiguo"

    t["Nivel"] = [veredicto(a, k) for a, k in zip(t["p ADF nivel"], t["p KPSS nivel"])]
    t["Diferencia"] = [veredicto(a, k) for a, k in zip(t["p ADF dif."], t["p KPSS dif."])]
    txt = pd.DataFrame(index=t.index)
    txt["Det."] = t["Det."]
    txt["N"] = t["N"]
    for etapa in ["nivel", "dif."]:
        txt[f"ADF {etapa} (p)"] = [f"{num(a, 2)} ({num(p, 3)})" for a, p in zip(t[f"ADF {etapa}"], t[f"p ADF {etapa}"])]
        # statsmodels acota el p-valor del KPSS a [0,01; 0,10] (interpola en la tabla de Kwiatkowski et al.)
        txt[f"KPSS {etapa} (p)"] = [f"{num(a, 2)} ({'≤0,01' if p <= 0.01 else '≥0,10' if p >= 0.1 else num(p, 3)})"
                                    for a, p in zip(t[f"KPSS {etapa}"], t[f"p KPSS {etapa}"])]
    txt["Nivel"], txt["Diferencia"] = t["Nivel"], t["Diferencia"]
    return md_tabla(txt), t


def fig_acf(s: dict) -> dict:
    x = s["infl_m"]
    fig, axes = plt.subplots(2, 2, figsize=(15, 8.5))
    for row, (serie, nombre) in enumerate([(x, "Inflación mensual (nivel)"), (x.diff().dropna(), "Inflación mensual (1ra diferencia)")]):
        for col, (fn, tipo) in enumerate([(plot_acf, "ACF"), (plot_pacf, "PACF")]):
            a = axes[row, col]
            kw = {"method": "ywm"} if tipo == "PACF" else {}
            fn(serie, ax=a, lags=24, zero=False, color=style.BLUE, vlines_kwargs={"colors": style.BLUE}, title=None, **kw)
            for coll in a.collections:
                if isinstance(coll, plt.matplotlib.collections.PolyCollection):
                    coll.set_facecolor(style.BLUE)
                    coll.set_alpha(0.12)
            a.set_title(f"{tipo}: {nombre}", fontsize=12.5)
            a.set_xlabel("Rezago (meses)")
            a.set_xticks([1, 3, 6, 9, 12, 15, 18, 21, 24])
    fig.subplots_adjust(hspace=0.4)
    style.source(fig, f"Fuente: INDEC. Muestra {per(x.index[0], 'M')} a {per(x.index[-1], 'M')} (N = {len(x)}). "
                      "Banda sombreada: intervalo de confianza del 95% (Bartlett para la ACF).")
    style.save(fig, FIG / "D10_acf_pacf_inflacion.png")
    lb = acorr_ljungbox(x, lags=[6, 12, 24])
    lbd = acorr_ljungbox(x.diff().dropna(), lags=[6, 12, 24])
    return {"lb": lb, "lbd": lbd}


def estacionalidad(s: dict) -> dict:
    """Factores estacionales (descomposición clásica con media móvil centrada) y un test de
    Kruskal-Wallis sobre la serie sin tendencia: H0 = todos los meses tienen la misma distribución."""
    inf = s["infl_m"].loc["2016-06-01":].dropna()
    gasto = np.log(s["gasto_real"].dropna())
    pib = np.log(s["pib_real"])
    emae = s["d_emae"].dropna().loc["2016-06-01":]
    out = {}
    for k, serie, period, unidad in [("Inflación mensual", inf, 12, "pp"), ("Gasto primario real", gasto, 12, "%"),
                                     ("PBI real (sin desestacionalizar)", pib, 4, "%"),
                                     ("EMAE desestacionalizado (var. mensual)", emae, 12, "pp")]:
        dec = seasonal_decompose(serie, model="additive", period=period)
        sin_tend = (serie - dec.trend).dropna()
        # La devaluación de dic-2023 y su arrastre no son estacionalidad: con ellos adentro, diciembre
        # sale como el mes "más inflacionario" del año solo por un dato. Se excluye esa ventana.
        sin_tend = sin_tend.drop(sin_tend.loc[EXCLUIR_SHOCK[0]:EXCLUIR_SHOCK[1]].index)
        clave = sin_tend.index.month if period == 12 else sin_tend.index.quarter
        grupos = [sin_tend[clave == c].to_numpy() for c in sorted(set(clave))]
        kw = stats.kruskal(*grupos)
        fac = sin_tend.groupby(clave).mean()
        fac = fac - fac.mean()                      # factores que suman cero, como en la descomposición clásica
        if unidad == "%":
            fac = 100 * (np.exp(fac) - 1)
        out[k] = {"factores": fac, "H": kw.statistic, "p": kw.pvalue, "unidad": unidad, "period": period}

    fig, axes = plt.subplots(1, 3, figsize=(17, 5))
    for a, k in zip(axes, ["Inflación mensual", "Gasto primario real", "PBI real (sin desestacionalizar)"]):
        fac = out[k]["factores"]
        etiquetas = base.MESES if out[k]["period"] == 12 else ["T1", "T2", "T3", "T4"]
        a.bar(etiquetas, fac, color=[style.BLUE if v >= 0 else style.ORANGE for v in fac], width=0.7)
        a.axhline(0, color=style.INK_2, lw=0.8)
        a.grid(axis="x", visible=False)
        a.set_title(k, fontsize=12.5)
        unidad = "puntos porcentuales" if out[k]["unidad"] == "pp" else "% sobre la tendencia"
        style.subtitle(a, f"Factor estacional ({unidad}). Kruskal-Wallis p = {num(out[k]['p'], 3)}")
    style.source(fig, "Fuente: INDEC y Secretaría de Hacienda. Descomposición aditiva clásica (media móvil centrada); "
                      "gasto y PBI en logaritmos. El pico del gasto en junio y diciembre es el aguinaldo.")
    style.save(fig, FIG / "D11_estacionalidad.png")
    return out


def chow(y: np.ndarray, X: np.ndarray, k: int) -> float:
    """Estadístico F de Chow para un quiebre en todos los coeficientes después de la observación k."""
    def ssr(yy: np.ndarray, XX: np.ndarray) -> float:
        b = np.linalg.lstsq(XX, yy, rcond=None)[0]
        r = yy - XX @ b
        return float(r @ r)
    q, n = X.shape[1], len(y)
    s_r, s_u = ssr(y, X), ssr(y[:k], X[:k]) + ssr(y[k:], X[k:])
    return ((s_r - s_u) / q) / (s_u / (n - 2 * q))


def quiebres(s: dict) -> dict:
    """QLR (sup-F) sobre un AR(1) de la inflación mensual, Chow en fechas conocidas y Zivot-Andrews."""
    x = s["infl_m"]
    y, ylag = x.iloc[1:].to_numpy(), x.shift(1).iloc[1:].to_numpy()
    fechas = x.index[1:]
    X = np.column_stack([np.ones_like(ylag), ylag])
    n = len(y)
    ks = range(int(0.15 * n), int(0.85 * n))
    F = pd.Series({fechas[k]: chow(y, X, k) for k in ks})
    out = {"F": F, "qlr_fecha": F.idxmax(), "qlr": F.max()}

    # Chow en fechas elegidas a priori (no hay problema de búsqueda: valen los valores críticos F habituales)
    chows = []
    for name, (serie, ar) in {"Inflación mensual, AR(1)": (x, True), "Var. mensual del EMAE (media)": (s["d_emae"].loc["2016-06-01":], False),
                              "Var. mensual salario real privado (media)": (s["d_sal_priv_reg"], False),
                              "Depreciación mensual oficial, AR(1)": (s["dep_oficial"].loc["2016-06-01":], True)}.items():
        serie = serie.dropna()
        yy = serie.iloc[1:].to_numpy() if ar else serie.to_numpy()
        idx = serie.index[1:] if ar else serie.index
        XX = np.column_stack([np.ones(len(yy)), serie.shift(1).iloc[1:].to_numpy()]) if ar else np.ones((len(yy), 1))
        for fecha in ["2023-12-01", "2025-04-01"]:
            k = int(idx.searchsorted(pd.Timestamp(fecha)))
            fstat = chow(yy, XX, k)
            p = 1 - stats.f.cdf(fstat, XX.shape[1], len(yy) - 2 * XX.shape[1])
            chows.append({"Serie": name, "Fecha del quiebre": base.mes(pd.Timestamp(fecha)), "F": fstat, "p": p})
    out["chow"] = pd.DataFrame(chows)

    za = []
    for name, serie in {"Inflación mensual": x, "log salario real privado registrado": np.log(s["sal_priv_reg"]),
                        "log EMAE": np.log(s["emae"].loc["2016-06-01":]), "log tipo de cambio real": np.log(s["tcr"])}.items():
        serie = serie.dropna()
        stat, p, cv, lag, bp = zivot_andrews(serie, regression="c", autolag="AIC")
        za.append({"Serie": name, "ZA": stat, "p": p, "VC 5%": cv["5%"], "Quiebre": base.mes(serie.index[bp])})
    out["za"] = pd.DataFrame(za)

    # Media por tramo, para la figura
    fig, (a, b) = plt.subplots(1, 2, figsize=(16, 5.4))
    a.bar(x.index, x, width=25, color=style.BASELINE)
    tramos = [x.index[0], pd.Timestamp("2023-12-01"), pd.Timestamp("2025-04-01"), x.index[-1] + pd.DateOffset(months=1)]
    for d0, d1, color in zip(tramos[:-1], tramos[1:], [style.AQUA, style.ORANGE, style.BLUE]):
        tramo = x[(x.index >= d0) & (x.index < d1)]
        a.hlines(tramo.mean(), d0, d1, color=color, lw=2.5)
        a.annotate(f"media {num(tramo.mean(), 1)}%", xy=(d0 + (d1 - d0) / 2, tramo.mean()), xytext=(0, 6), textcoords="offset points",
                   ha="center", fontsize=9, color=color, fontweight="bold")
    for d in tramos[1:3]:
        a.axvline(d, color=style.INK_2, lw=0.8, ls="--")
    a.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
    a.set_title("Inflación mensual y media por tramo")
    style.subtitle(a, "Tramos: hasta nov-23 · dic-23 a mar-25 · desde la salida del cepo (abr-25)")
    a.xaxis.set_major_locator(mdates.YearLocator(2))
    a.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    b.plot(F.index, F, color=style.INK)
    for (lab, cv), ls in zip(QLR_CRIT.items(), [":", "--", "-."]):
        b.axhline(cv, color=style.RED, lw=0.9, ls=ls, label=f"Valor crítico {lab} ({num(cv, 2)})")
    b.annotate(f"máximo: {base.mes(out['qlr_fecha'])}, F = {num(out['qlr'], 1)}", xy=(out["qlr_fecha"], out["qlr"]),
               xytext=(-10, 0), textcoords="offset points", ha="right", va="center", fontsize=9.5, fontweight="bold")
    b.set_ylim(0, out["qlr"] * 1.1)
    b.set_title("Test de quiebre de Quandt-Andrews (QLR)")
    style.subtitle(b, "F de Chow para cada fecha candidata, AR(1) de la inflación, 15% de recorte")
    b.legend(loc="upper left", fontsize=9)
    b.xaxis.set_major_locator(mdates.YearLocator(2))
    b.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    style.source(fig, "Fuente: INDEC. Valores críticos del QLR para q = 2: Andrews (1993), en Stock y Watson, tabla 14.5.")
    style.save(fig, FIG / "D12_quiebres_inflacion.png")
    return out


# ---------------------------------------------------------------- documento

VARIABLES = [  # clave, frecuencia, decimales
    ("infl_m", "M", 2), ("infl_a", "M", 1), ("sal_priv_reg", "M", 1), ("d_sal_priv_reg", "M", 2), ("sal_publico", "M", 1),
    ("d_sal_publico", "M", 2), ("sal_no_reg", "M", 1), ("d_sal_no_reg", "M", 2), ("smvm", "M", 1), ("emae", "M", 1),
    ("dn_sal_priv_reg", "M", 2), ("dn_sal_publico", "M", 2), ("dn_sal_no_reg", "M", 2), ("dn_smvm", "M", 2),
    ("d_emae", "M", 2), ("g_pib", "Q", 1), ("g_ibif", "Q", 1), ("tasa_inv", "Q", 1), ("gasto_pib", "M", 1),
    ("d_gasto_real", "M", 1), ("res_primario", "M", 2), ("res_financiero", "M", 2), ("sub_energia_pib", "Q", 2),
    ("dep_oficial", "M", 2), ("tcr", "M", 1), ("riesgo_pais", "D", 0), ("r_adr", "D", 2), ("r_bonos", "D", 2),
    ("pobreza", "S", 1), ("desocupacion", "Q", 1)]


def render(plantilla: str, valores: dict[str, str]) -> str:
    faltan = sorted(set(re.findall(r"\{\{(\w+)\}\}", plantilla)) - set(valores))
    if faltan:
        raise KeyError(f"La plantilla usa claves que el script no calcula: {faltan}")
    return re.sub(r"\{\{(\w+)\}\}", lambda mt: valores[mt.group(1)], plantilla)


def main() -> None:
    style.apply()
    plt.rcParams["axes.titlepad"] = 24
    d = cargar()
    s = d["s"]
    v: dict[str, str] = {}
    desc = {}
    for k, freq, dec in VARIABLES:
        v[f"desc_{k}"], desc[k] = tabla_descriptiva(s[k], freq, dec)
    desc["infl_m"].index.name = None

    fig_series_precios(s)
    fig_series_actividad(s)
    fig_series_mercados(s)
    frec = fig_histogramas(s)
    for g, t in frec.items():
        v[f"frec_{g}"] = fmt_frecuencias(t)
    n = {g: int(t["Frec. absoluta"].sum()) for g, t in frec.items()}
    v["sturges"] = ", ".join(f"{g} {num(1 + 3.322 * np.log10(nn), 1)}" for g, nn in n.items())
    for g, t in frec.items():
        v[f"menos2_{g}"] = num(t.loc[t.index[:2], "Frec. relativa (%)"].sum(), 0)      # meses con inflación < 2%
        v[f"mas5_{g}"] = num(t.loc[t.index[5:], "Frec. relativa (%)"].sum(), 0)        # meses con inflación >= 5%

    var = variacion_por_gobierno(s)
    fig_barras(s, desc, var)
    vt = var.copy()
    for c, dd in [("Años", 1), ("Acumulada (%)", 1), ("Anualizada (%)", 1)]:
        vt[c] = [num(x, dd) for x in vt[c]]
    vt["Variable"] = [f"{a}{'' if c else ' *'}" for a, c in zip(vt["Variable"], var["completo"])]
    v["tabla_variacion"] = md_tabla(vt.drop(columns="completo"), index=False)

    nr = nominal_vs_real(s)
    fig_nominal(s, nr)
    nt = nr.drop(columns="completo").copy()
    for c in [c for c in nt.columns if "(%)" in c]:
        nt[c] = [num(x, 1) for x in nt[c]]
    nt["Salario"] = [f"{a}{'' if c else ' *'}" for a, c in zip(nt["Salario"], nr["completo"])]
    v["tabla_nominal_real"] = md_tabla(nt, index=False)
    for _, r in nr.iterrows():
        key = {n: k for k, n in SALARIOS.items()}[r["Salario"]]
        for c, tag in [("Nominal anual (%)", "nom"), ("Inflación anual (%)", "inf"), ("Real anual (%)", "real"),
                       ("Nominal acum. (%)", "nomac"), ("Real acum. (%)", "realac")]:
            v[f"nr_{key}_{r['Gobierno']}_{tag}"] = num(r[c], 1)

    gasto = composicion_gasto(d["f"], d["energia"])
    dem = composicion_demanda(d["dem_n"])
    fig_tortas(gasto, dem)
    gt = gasto.map(lambda x: num(x, 1))
    gt["Cambio (pp)"] = [f"{x:+.1f}".replace(".", ",") for x in gasto[2025] - gasto[2023]]
    gt.index.name = "Rubro (% del gasto primario)"
    v["tabla_gasto"] = md_tabla(gt)
    dt = dem.map(lambda x: num(x, 1))
    dt.index.name = "Componente (% del PBI, precios corrientes)"
    v["tabla_demanda"] = md_tabla(dt)
    fig_boxplots(s)

    ur_txt, ur = raiz_unitaria(s)
    v["tabla_raiz"] = ur_txt
    acf = fig_acf(s)
    lb = pd.DataFrame({"Rezagos": [6, 12, 24], "Q nivel": acf["lb"]["lb_stat"].to_numpy(), "p nivel": acf["lb"]["lb_pvalue"].to_numpy(),
                       "Q diferencia": acf["lbd"]["lb_stat"].to_numpy(), "p diferencia": acf["lbd"]["lb_pvalue"].to_numpy()})
    v["tabla_ljungbox"] = md_tabla(lb.assign(**{c: [num(x, 1 if c.startswith("Q") else 4) for x in lb[c]]
                                                for c in lb.columns if c != "Rezagos"}), index=False)
    est = estacionalidad(s)
    v["tabla_estacionalidad"] = md_tabla(pd.DataFrame(
        {"Serie": list(est), "Kruskal-Wallis H": [num(e["H"], 1) for e in est.values()],
         "p-valor": [num(e["p"], 4) for e in est.values()],
         "Mes/trimestre de mayor factor": [(base.MESES if e["period"] == 12 else ["T1", "T2", "T3", "T4"])[int(e["factores"].argmax())]
                                           for e in est.values()],
         "Factor máximo": [f"{num(e['factores'].max(), 2)} {e['unidad']}" for e in est.values()]}), index=False)
    for k, short in [("Inflación mensual", "infl"), ("Gasto primario real", "gasto"), ("PBI real (sin desestacionalizar)", "pib")]:
        fac = est[k]["factores"]
        v[f"est_{short}_max"], v[f"est_{short}_min"] = num(fac.max(), 1), num(fac.min(), 1)
        v[f"est_{short}_p"] = num(est[k]["p"], 3)
    qb = quiebres(s)
    v["qlr_fecha"], v["qlr"] = base.mes(qb["qlr_fecha"]), num(qb["qlr"], 1)
    v["tabla_chow"] = md_tabla(qb["chow"].assign(F=[num(x, 2) for x in qb["chow"]["F"]],
                                                 p=[num(x, 4) for x in qb["chow"]["p"]]), index=False)
    v["tabla_za"] = md_tabla(qb["za"].assign(ZA=[num(x, 2) for x in qb["za"]["ZA"]], p=[num(x, 3) for x in qb["za"]["p"]],
                                             **{"VC 5%": [num(x, 2) for x in qb["za"]["VC 5%"]]}), index=False)

    # Números citados en el texto
    def med(k: str, g: str, c: str = "Media", dd: int = 1) -> str:
        return num(desc[k].loc[g, c], dd)
    for k, dd in [("infl_m", 2), ("d_sal_priv_reg", 2), ("d_sal_publico", 2), ("d_sal_no_reg", 2), ("g_pib", 1), ("g_ibif", 1),
                  ("res_primario", 2), ("res_financiero", 2), ("gasto_pib", 1), ("sub_energia_pib", 2), ("tasa_inv", 1),
                  ("dep_oficial", 2), ("riesgo_pais", 0), ("r_adr", 2), ("r_bonos", 2), ("pobreza", 1),
                  ("desocupacion", 1), ("d_emae", 2), ("infl_a", 1), ("tcr", 1), ("d_gasto_real", 1), ("smvm", 1), ("emae", 1),
                  ("sal_priv_reg", 1), ("sal_publico", 1), ("sal_no_reg", 1), ("dn_sal_priv_reg", 2), ("dn_sal_publico", 2),
                  ("dn_sal_no_reg", 2), ("dn_smvm", 2)]:
        for g in ORDEN:
            if g in desc[k].index:
                for c, tag in [("Media", "media"), ("Mediana", "mediana"), ("Desvío", "desvio"), ("CV (%)", "cv"),
                               ("Asimetría", "asim"), ("Curtosis", "curt"), ("Mín", "min"), ("Máx", "max")]:
                    v[f"{k}_{g}_{tag}"] = med(k, g, c, 2 if tag in ("asim", "curt") else dd)
    v["ultimo_ipc"] = base.mes(s["infl_m"].index[-1])
    with open(HERE / "plantilla.md", encoding="utf-8") as fh:
        doc = render(fh.read(), v)
    (HERE / "ANALISIS_DESCRIPTIVO.md").write_text(doc, encoding="utf-8")
    print(f"Escrito {HERE / 'ANALISIS_DESCRIPTIVO.md'} y {len(list(FIG.glob('*.png')))} figuras en {FIG}")


if __name__ == "__main__":
    main()
