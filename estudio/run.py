"""La economía de Milei en datos: salario real, inflación, actividad, inversión, cuentas
públicas, dólar y activos argentinos, de diciembre de 2023 al último dato disponible.

Reproduce todas las figuras y la tabla de resultados (estudio/results.md):
    uv run python estudio/run.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import pandas as pd
from tabulate import tabulate

from quantkit import style
from quantkit.bonos import total_return
from quantkit.data import (load_bcra, load_data912, load_dolares, load_inflacion, load_prices, load_riesgo_pais,
                           load_series)

HERE = Path(__file__).parent
FIG = HERE / "figures"

ASUNCION = pd.Timestamp("2023-12-10")
BASE_M = pd.Timestamp("2023-11-01")   # último mes completo del gobierno anterior: base 100 de todo índice real
BASE_D = "2023-12-08"                  # último cierre antes de asumir (feriado en Buenos Aires: BYMA usa el 7/12)
DESDE = "2017-01-01"                   # contexto: se ve también el gobierno de Macri y el de Fernández
REZAGO_NO_REG = 5                      # el dato de no registrados de cada mes describe los salarios de 5 meses antes

MENSUAL = {"ipc": "148.3_INIVELNAL_DICI_M_26", "ipc_nucleo": "148.3_INUCLEONAL_DICI_M_19",
           "ipc_regulados": "148.3_IREGULANAL_DICI_M_22", "sal_total": "149.1_TL_INDIIOS_OCTU_0_21",
           "sal_priv_reg": "149.1_SOR_PRIADO_OCTU_0_25", "sal_publico": "149.1_SOR_PUBICO_OCTU_0_14",
           "sal_no_reg": "149.1_SOR_PRIADO_OCTU_0_28", "smvm": "57.1_SMVMM_0_M_34", "jub_minima": "58.1_MP_0_M_13",
           "emae": "143.3_NO_PR_2004_A_31"}
# Sector Público Nacional no financiero, base caja (Informe Mensual de Ingresos y Gastos, IMIG), millones de $.
FISCAL = {"res_primario": "452.3_RESULTADO_RIO_0_M_18_54", "intereses": "452.3_INTERESES_TOS_0_M_15_62",
          "ing_primarios": "379.9_ING_PRIMAR017__36_12", "sup_primario_spn": "379.9_SUPERAVIT_017__23_94",
          "jubilaciones": "452.2_JUBILACIONVAS_0_T_36_18", "asignaciones": "452.2_ASIGNACIONIJO_0_T_26_67",
          "pnc": "452.2_PENSIONES_VAS_0_T_26_164", "sub_transporte": "452.2_TRANSPORTERTE_0_T_10_32",
          "salarios_pub": "452.2_SALARIOSIOS_0_T_8_22", "transf_prov_otras": "452.2_TRANSFERENRAS_0_T_42_55",
          "cap_transporte": "452.3_CAPITAL_TRION_0_M_25_82", "cap_energia": "452.2_CAPITAL_ENION_0_T_22_35",
          "cap_vivienda": "452.3_CAPITAL_VIION_0_M_23_52", "cap_prov_otras": "452.3_CAPITAL_OTIAS_0_M_38_72",
          "cap_prov_transporte": "452.3_CAPITAL_TRIAS_0_M_43_35", "cap_prov_vivienda": "452.3_CAPITAL_VIIAS_0_M_41_41",
          "cap_edu": "452.3_CAPITAL_EDION_0_M_24_92", "cap_agua": "452.3_CAPITAL_AGION_0_M_41_40",
          "cap_prov_energia": "452.3_CAPITAL_ENIAS_0_M_40_18", "fondo_sojero": "452.3_FONDO_FEDERIO_0_M_23_90"}
TRIMESTRAL = {"pib_real": "4.2_OGP_2004_T_17", "ibif_real": "4.2_DGIT_2004_T_25", "pib_nominal": "4.4_OGP_2004_T_17",
              "desocupacion": "42.3_EPH_PUNTUATAL_0_M_30"}
SUBSIDIO_ENERGIA = {"sub_energia": "452.2_ENERGIAGIA_0_T_7_79"}   # solo existe trimestral
RUBROS = {"Jubilaciones y pensiones": "jubilaciones", "Asignaciones (AUH y familiares)": "asignaciones",
          "Pensiones no contributivas": "pnc", "Salarios del Estado nacional": "salarios_pub",
          "Subsidios a la energía": "sub_energia", "Subsidios al transporte": "sub_transporte",
          "Transferencias a provincias": "transf_prov_otras", "Obra pública (gasto de capital)": "capital"}
AR = ["GGAL", "BMA", "BBAR", "SUPV", "YPF", "PAM", "TGS", "CEPU", "EDN", "TEO", "CRESY", "LOMA", "IRS"]
BONOS = ["GD30D", "GD35D", "GD41D"]
EVENTOS = {"2023-12-10": "Asume Milei", "2025-04-14": "Salida del cepo", "2025-09-08": "Derrota en PBA",
           "2025-10-27": "Legislativas", "2026-10-26": "Lula reelecto"}
# INDEC, EPH 31 aglomerados, % de personas bajo la línea de pobreza (comunicados semestrales).
POBREZA = {"2016S2": 30.3, "2017S1": 28.6, "2017S2": 25.7, "2018S1": 27.3, "2018S2": 32.0, "2019S1": 35.4,
           "2019S2": 35.5, "2020S1": 40.9, "2020S2": 42.0, "2021S1": 40.6, "2021S2": 37.3, "2022S1": 36.5,
           "2022S2": 39.2, "2023S1": 40.1, "2023S2": 41.7, "2024S1": 52.9, "2024S2": 38.1, "2025S1": 31.6,
           "2025S2": 28.2, "2026S1": 32.3}
FUENTE = "Fuente: INDEC, Secretaría de Hacienda y Ministerio de Trabajo (datos.gob.ar)."


# ---------------------------------------------------------------- transformaciones

def ipc_extendido(ipc: pd.Series) -> pd.Series:
    """IPC nacional (dic-2016 = 100) estirado con las variaciones mensuales del INDEC que
    todavía no están cargadas en datos.gob.ar (ArgentinaDatos publica el dato el mismo día)."""
    ipc = ipc.dropna().copy()
    var = load_inflacion()
    var.index = var.index.to_period("M").to_timestamp()
    for d in var.index[var.index > ipc.index[-1]]:
        ipc.loc[d] = ipc.iloc[-1] * (1 + var.loc[d] / 100)
    return ipc


def real(nominal: pd.Series, ipc: pd.Series, base: pd.Timestamp = BASE_M) -> pd.Series:
    """Poder de compra: el valor nominal deflactado por el IPC, con ``base`` = 100."""
    r = (nominal / ipc).dropna()
    return 100 * r / r.loc[base]


def anual(q: pd.Series) -> pd.Series:
    """Valor anual de una serie trimestral de cuentas nacionales, solo años completos.

    El INDEC publica cada trimestre a tasa anual, así que el año es el promedio de los
    cuatro trimestres y no la suma (sumarlos daría un PBI cuatro veces más grande)."""
    g = q.dropna().groupby(q.dropna().index.year)
    return g.mean()[g.count() == 4]


def semestre(q: pd.Series, year: int) -> float:
    """Variación interanual del primer semestre de ``year``, en %."""
    h = lambda y: q.loc[f"{y}-01-01":f"{y}-06-30"].sum()  # noqa: E731
    return 100 * (h(year) / h(year - 1) - 1)


MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]


def mes(d: pd.Timestamp) -> str:
    """'abr-24': el locale de matplotlib escribe los meses en inglés."""
    return f"{MESES[d.month - 1]}-{d:%y}"


def asof(s: pd.Series, d: str | pd.Timestamp) -> float:
    return float(s.dropna().loc[:d].iloc[-1])


# ---------------------------------------------------------------- helpers de gráfico

def milei(ax: plt.Axes, label: bool = True) -> None:
    ax.axvspan(ASUNCION, pd.Timestamp("2027-01-01"), color=style.BLUE, alpha=0.06, lw=0)
    ax.axvline(ASUNCION, color=style.BLUE, lw=1, ls="--", alpha=0.6)
    if label:
        ax.annotate("Milei", xy=(ASUNCION, 1), xycoords=("data", "axes fraction"), xytext=(4, -4),
                    textcoords="offset points", va="top", fontsize=9, color=style.BLUE)


def fin(ax: plt.Axes, s: pd.Series, color: str, fmt: str = "{:.0f}", dx: int = 4) -> None:
    """Etiqueta del último valor al final de la línea."""
    s = s.dropna()
    ax.annotate(fmt.format(s.iloc[-1]), xy=(s.index[-1], s.iloc[-1]), xytext=(dx, 0), textcoords="offset points",
                va="center", fontsize=9.5, color=color, fontweight="bold")


def fechas(ax: plt.Axes, years: int = 1) -> None:
    ax.xaxis.set_major_locator(mdates.YearLocator(years))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))


def barras_anuales(ax: plt.Axes, s: pd.Series, milei_desde: str = "2024", fmt: str = "{:+.1f}") -> None:
    colors = [style.BLUE if str(k) >= milei_desde else style.BASELINE for k in s.index]
    bars = ax.bar([str(k) for k in s.index], s.to_numpy(), color=colors, width=0.7)
    for b, v in zip(bars, s.to_numpy()):
        ax.annotate(fmt.format(v), xy=(b.get_x() + b.get_width() / 2, v), xytext=(0, 3 if v >= 0 else -3),
                    textcoords="offset points", ha="center", va="bottom" if v >= 0 else "top", fontsize=8.5,
                    color=style.INK_2)
    ax.axhline(0, color=style.INK_2, lw=0.8)
    ax.grid(axis="x", visible=False)


# ---------------------------------------------------------------- figuras

def fig_inflacion(var: pd.Series, ipc: pd.Series, m: pd.DataFrame) -> dict:
    v = var.loc[DESDE:]
    yoy = 100 * ipc.pct_change(12).loc[DESDE:]
    fig, (a, b) = plt.subplots(1, 2, figsize=(14, 5))
    a.bar(v.index, v, width=25, color=[style.BLUE if d >= ASUNCION else style.BASELINE for d in v.index])
    pico = v.loc["2023-12-01":"2023-12-31"]
    a.annotate(f"Dic-23: {pico.iloc[0]:.1f}%", xy=(pico.index[0], pico.iloc[0]), xytext=(-110, -10),
               textcoords="offset points", fontsize=9.5, color=style.INK, arrowprops={"arrowstyle": "-", "color": style.MUTED})
    a.annotate(f"{mes(v.index[-1])}: {v.iloc[-1]:.1f}%", xy=(v.index[-1], v.iloc[-1]), xytext=(-40, 40),
               textcoords="offset points", fontsize=9.5, color=style.BLUE, fontweight="bold",
               arrowprops={"arrowstyle": "-", "color": style.BLUE})
    a.set_title("Inflación mensual")
    style.subtitle(a, "IPC nacional, variación % mensual")
    a.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
    milei(a)
    fechas(a)
    nucleo = 100 * m["ipc_nucleo"].pct_change(12).loc[DESDE:]
    reg = 100 * m["ipc_regulados"].pct_change(12).loc[DESDE:]
    b.plot(yoy.index, yoy, color=style.INK, label="Nivel general")
    b.plot(nucleo.index, nucleo, color=style.ORANGE, lw=1.4, label="Núcleo")
    b.plot(reg.index, reg, color=style.AQUA, lw=1.4, label="Regulados (tarifas)")
    fin(b, yoy, style.INK, "{:.0f}%")
    b.set_yscale("log")
    b.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"{x:.0f}%"))
    b.set_yticks([10, 20, 30, 50, 100, 200, 300])
    b.set_title("Inflación interanual")
    style.subtitle(b, "Variación % contra el mismo mes del año anterior (escala logarítmica)")
    b.legend(loc="upper left")
    milei(b, label=False)
    fechas(b)
    style.source(fig, f"{FUENTE} Último dato: {v.index[-1]:%m/%Y}.")
    style.save(fig, FIG / "01_inflacion.png")
    return {"pico_mensual": pico.iloc[0], "ultima_mensual": v.iloc[-1], "ultima_fecha": v.index[-1],
            "yoy_pico": yoy.max(), "yoy_pico_fecha": yoy.idxmax(), "yoy_ultima": yoy.iloc[-1],
            "regulados_vs_nucleo": (m["ipc_regulados"].dropna().iloc[-1] / m["ipc_regulados"].loc[BASE_M])
            / (m["ipc_nucleo"].dropna().iloc[-1] / m["ipc_nucleo"].loc[BASE_M]) - 1}


def fig_salarios(m: pd.DataFrame, ipc: pd.Series) -> dict:
    series = {"Privado registrado": ("sal_priv_reg", style.BLUE), "Público": ("sal_publico", style.ORANGE),
              "No registrado*": ("sal_no_reg", style.MUTED)}
    otros = {"Salario mínimo": ("smvm", style.VIOLET), "Jubilación mínima (sin bono)": ("jub_minima", style.RED)}
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.2), sharey=True)
    out = {}
    for ax, grupo, titulo, sub in [
        (axes[0], series, "Salario real", "Índice de salarios del INDEC deflactado por el IPC, nov-2023 = 100"),
        (axes[1], otros, "Salario mínimo y jubilación mínima reales", "Deflactados por el IPC, nov-2023 = 100"),
    ]:
        for name, (col, color) in grupo.items():
            nominal = m[col].shift(-REZAGO_NO_REG) if col == "sal_no_reg" else m[col]
            r = real(nominal, ipc).loc[DESDE:]
            r = r.loc[: ipc.index[-1]]
            ax.plot(r.index, r, color=color, label=name, lw=2.2 if color != style.MUTED else 1.6)
            fin(ax, r, color)
            out[col] = r
        ax.axhline(100, color=style.INK_2, lw=0.8)
        ax.set_title(titulo)
        style.subtitle(ax, sub)
        ax.legend(loc="lower left")
        milei(ax)
        fechas(ax)
    style.source(fig, f"{FUENTE} *El salario no registrado se publica con 5 meses de rezago: se ubica en el mes al que corresponde. "
                      "La jubilación mínima no incluye el bono de $70.000, congelado desde marzo de 2024.")
    style.save(fig, FIG / "02_salario_real.png")
    return {k: (v.dropna().index[-1], v.dropna().iloc[-1], v.loc["2024-01-01":].min(), v.loc["2024-01-01":].idxmin(),
                v.loc["2017-01-01":"2017-12-31"].mean()) for k, v in out.items()}


def fig_actividad(m: pd.DataFrame, q: pd.DataFrame) -> dict:
    emae = 100 * m["emae"] / m["emae"].loc[BASE_M]
    emae = emae.loc[DESDE:].dropna()
    pib = anual(q["pib_real"])
    g = (100 * pib.pct_change()).loc[2017:]
    g.loc["S1-26"] = semestre(q["pib_real"], 2026)
    g.index = [str(k) for k in g.index]
    fig, (a, b) = plt.subplots(1, 2, figsize=(14, 5), gridspec_kw={"width_ratios": [1.4, 1]})
    a.plot(emae.index, emae, color=style.INK)
    a.axhline(100, color=style.INK_2, lw=0.8)
    fin(a, emae, style.INK)
    piso = emae.loc["2024-01-01":].idxmin()
    a.annotate(f"Piso {mes(piso)}: {emae.loc[piso]:.0f}", xy=(piso, emae.loc[piso]), xytext=(-20, -28),
               textcoords="offset points", fontsize=9.5, ha="center", arrowprops={"arrowstyle": "-", "color": style.MUTED})
    a.set_title("Actividad económica mensual")
    style.subtitle(a, "EMAE desestacionalizado, nov-2023 = 100")
    milei(a)
    fechas(a)
    barras_anuales(b, g, milei_desde="2024")
    b.set_title("Crecimiento del PBI")
    style.subtitle(b, "Variación % anual, a precios constantes (S1-26: primer semestre interanual)")
    b.tick_params(axis="x", rotation=45)
    style.source(fig, f"{FUENTE} Último dato: EMAE {emae.index[-1]:%m/%Y}, PBI {q['pib_real'].dropna().index[-1]:%m/%Y} (trimestre).")
    style.save(fig, FIG / "03_actividad.png")
    return {"emae_ultimo": emae.iloc[-1], "emae_fecha": emae.index[-1], "emae_piso": emae.loc[piso], "emae_piso_fecha": piso,
            "emae_max_previo": emae.loc[:"2023-11-30"].max(), "pib": g}


def fig_inversion(q: pd.DataFrame) -> dict:
    r4 = q[["pib_real", "ibif_real"]].dropna().rolling(4).sum().dropna()
    idx = 100 * r4 / r4.loc["2023-01-01":"2023-12-31"].iloc[-1]
    ib = anual(q["ibif_real"])
    g = (100 * ib.pct_change()).loc[2017:]
    g.loc["S1-26"] = semestre(q["ibif_real"], 2026)
    g.index = [str(k) for k in g.index]
    tasa = 100 * r4["ibif_real"] / r4["pib_real"]
    fig, (a, b) = plt.subplots(1, 2, figsize=(14, 5), gridspec_kw={"width_ratios": [1.4, 1]})
    a.plot(idx.index, idx["ibif_real"], color=style.GREEN, label="Inversión (IBIF)")
    a.plot(idx.index, idx["pib_real"], color=style.INK, lw=1.5, label="PBI")
    fin(a, idx["ibif_real"], style.GREEN)
    fin(a, idx["pib_real"], style.INK)
    a.axhline(100, color=style.INK_2, lw=0.8)
    a.set_title("Inversión y PBI")
    style.subtitle(a, "Suma móvil de 4 trimestres a precios constantes, 2023 = 100")
    a.legend(loc="lower left")
    milei(a)
    fechas(a)
    a.set_xlim(pd.Timestamp(DESDE), None)
    barras_anuales(b, g, milei_desde="2024")
    b.set_title("Crecimiento de la inversión")
    style.subtitle(b, "Inversión bruta interna fija, variación % anual real")
    b.tick_params(axis="x", rotation=45)
    style.source(fig, f"{FUENTE} Último dato: {q['ibif_real'].dropna().index[-1]:%m/%Y} (trimestre).")
    style.save(fig, FIG / "04_inversion.png")
    return {"ibif": g, "tasa_inv_2023": tasa.loc["2023-10-01"], "tasa_inv_ultima": tasa.iloc[-1],
            "tasa_inv_fecha": tasa.index[-1]}


def fig_fiscal(f: pd.DataFrame, q: pd.DataFrame) -> dict:
    f = f.assign(res_financiero=f["res_primario"] - f["intereses"])
    meses = f["res_primario"].dropna()
    ult = meses.index[-1]
    full = f.loc[:"2025-12-31", ["res_primario", "res_financiero"]].resample("YE").sum()
    full.index = full.index.year
    pib = anual(q["pib_nominal"])
    pct = 100 * full.div(pib, axis=0).dropna()
    # 2026: últimos 12 meses de resultado sobre los últimos 4 trimestres de PBI nominal
    u12 = f.loc[ult - pd.DateOffset(months=11):ult, ["res_primario", "res_financiero"]].sum()
    pibu4 = q["pib_nominal"].dropna().iloc[-4:].mean()
    pct.loc[f"12m a {ult:%m/%y}"] = 100 * u12 / pibu4
    pct.index = [str(k) for k in pct.index]
    fig, ax = plt.subplots(figsize=(12, 5))
    x = np.arange(len(pct))
    w = 0.38
    for i, (col, name, color) in enumerate([("res_primario", "Resultado primario", style.BLUE),
                                            ("res_financiero", "Resultado financiero (después de intereses)", style.ORANGE)]):
        bars = ax.bar(x + (i - 0.5) * w, pct[col], width=w, color=color, label=name)
        for bar, v in zip(bars, pct[col]):
            ax.annotate(f"{v:+.1f}", xy=(bar.get_x() + w / 2, v), xytext=(0, 3 if v >= 0 else -3), textcoords="offset points",
                        ha="center", va="bottom" if v >= 0 else "top", fontsize=8, color=style.INK_2)
    ax.set_xticks(x, pct.index)
    ax.axhline(0, color=style.INK_2, lw=0.8)
    ax.axvspan(list(pct.index).index("2024") - 0.5, len(pct) - 0.5, color=style.BLUE, alpha=0.06, lw=0)
    ax.grid(axis="x", visible=False)
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda v, _: f"{v:.0f}%"))
    ax.set_title("Equilibrio fiscal: del déficit al superávit")
    style.subtitle(ax, "Sector Público Nacional no financiero, base caja, % del PBI")
    ax.legend(loc="lower left")
    style.source(fig, f"Fuente: Secretaría de Hacienda (IMIG) e INDEC. Último dato: {ult:%m/%Y}.")
    style.save(fig, FIG / "05_equilibrio_fiscal.png")
    return {"pct": pct}


def fig_gasto(f: pd.DataFrame, energia: pd.Series, ipc: pd.Series) -> dict:
    ult = f["ing_primarios"].dropna().index[-1]
    gasto = f["ing_primarios"] - f["sup_primario_spn"]
    reales = pd.DataFrame({"Gasto primario": gasto / ipc, "Ingresos primarios": f["ing_primarios"] / ipc}).dropna()
    mismo = reales[reales.index.month <= ult.month]
    anuales = mismo.groupby(mismo.index.year).sum().loc[2017:]
    anuales = 100 * anuales / anuales.loc[2023]
    fig, ax = plt.subplots(figsize=(12, 5))
    x = np.arange(len(anuales))
    w = 0.38
    for i, (col, color) in enumerate([("Gasto primario", style.BLUE), ("Ingresos primarios", style.MUTED)]):
        bars = ax.bar(x + (i - 0.5) * w, anuales[col], width=w, color=color, label=col)
        for bar, v in zip(bars, anuales[col]):
            ax.annotate(f"{v:.0f}", xy=(bar.get_x() + w / 2, v), xytext=(0, 3), textcoords="offset points",
                        ha="center", va="bottom", fontsize=8, color=style.INK_2)
    ax.set_xticks(x, anuales.index.astype(str))
    ax.axhline(100, color=style.INK_2, lw=0.8)
    ax.set_ylim(0, anuales.to_numpy().max() * 1.12)
    ax.grid(axis="x", visible=False)
    ax.set_title("Gasto e ingresos del Estado nacional en términos reales")
    style.subtitle(ax, f"Enero a {MESES[ult.month - 1]} de cada año, deflactado por el IPC, 2023 = 100")
    ax.legend(loc="upper right", ncols=2)
    style.source(fig, f"Fuente: Secretaría de Hacienda (Sector Público Nacional, base caja) e INDEC. Último dato: {ult:%m/%Y}.")
    style.save(fig, FIG / "06_gasto_real.png")

    # Dónde se hizo el ajuste: 2025 contra 2023, años completos, en pesos constantes
    cap = [c for c in f.columns if c.startswith("cap_")] + ["fondo_sojero"]
    comp = f.assign(capital=f[cap].sum(axis=1, min_count=1))
    real_m = comp.div(ipc, axis=0)
    by_year = real_m.loc["2023-01-01":"2025-12-31"].groupby(real_m.loc["2023-01-01":"2025-12-31"].index.year).sum()
    ipc_q = ipc.resample("QS").mean()
    e = (energia / ipc_q).dropna()
    by_year["sub_energia"] = e.groupby(e.index.year).sum().reindex(by_year.index)
    by_year["gasto"] = (gasto / ipc).loc["2023-01-01":"2025-12-31"].groupby(lambda d: d.year).sum()
    rubros = pd.DataFrame({"var": {k: 100 * (by_year.loc[2025, c] / by_year.loc[2023, c] - 1) for k, c in RUBROS.items()},
                           "aporte": {k: 100 * (by_year.loc[2025, c] - by_year.loc[2023, c]) / by_year.loc[2023, "gasto"]
                                      for k, c in RUBROS.items()}}).sort_values("aporte")
    total = 100 * (by_year.loc[2025, "gasto"] / by_year.loc[2023, "gasto"] - 1)
    fig, (a, b) = plt.subplots(1, 2, figsize=(14, 5.4), sharey=True)
    y = np.arange(len(rubros))
    for ax, col, titulo, sub, fmt in [
        (a, "var", "Cuánto cayó cada rubro", "Variación % real del gasto, 2025 contra 2023", "{:+.0f}%"),
        (b, "aporte", "Cuánto aportó al ajuste", "Puntos % del gasto primario de 2023", "{:+.1f}"),
    ]:
        vals = rubros[col]
        ax.barh(y, vals, color=[style.RED if v < 0 else style.GREEN for v in vals], height=0.65)
        for yi, v in zip(y, vals):
            ax.annotate(fmt.format(v), xy=(v, yi), xytext=(-4 if v < 0 else 4, 0), textcoords="offset points",
                        ha="right" if v < 0 else "left", va="center", fontsize=9, color=style.INK)
        ax.axvline(0, color=style.INK_2, lw=0.8)
        ax.grid(axis="y", visible=False)
        ax.set_title(titulo)
        style.subtitle(ax, sub)
        lo, hi = vals.min(), max(vals.max(), 0)
        ax.set_xlim(lo * 1.3, hi + (hi - lo) * 0.15 + 1)
    a.set_yticks(y, rubros.index)
    style.source(fig, f"Fuente: Secretaría de Hacienda (IMIG) e INDEC. Gasto primario total: {total:+.0f}% real. "
                      "Cada rubro deflactado mes a mes por el IPC (energía, por trimestre).")
    style.save(fig, FIG / "07_ajuste_por_rubro.png")
    return {"gasto_idx": anuales, "rubros": rubros, "gasto_total_2025_vs_2023": total, "ult_fiscal": ult}


def fig_mercados(rp: pd.Series, p: pd.DataFrame, b: pd.DataFrame) -> dict:
    fig, axes = plt.subplots(1, 3, figsize=(17, 5))
    a = axes[0]
    r = rp.loc["2019-01-01":]
    a.plot(r.index, r, color=style.INK, lw=1.6)
    a.set_yscale("log")
    a.set_yticks([500, 700, 1000, 2000, 3000, 5000])
    a.yaxis.set_major_formatter(mtick.FuncFormatter(lambda v, _: f"{v:,.0f}".replace(",", ".")))
    a.minorticks_off()
    pre = asof(rp, BASE_D)
    minimo = rp.loc[BASE_D:].idxmin()
    a.annotate(f"Asume: {pre:,.0f}".replace(",", "."), xy=(pd.Timestamp(BASE_D), pre), xytext=(25, 45),
               textcoords="offset points", fontsize=9, arrowprops={"arrowstyle": "-", "color": style.MUTED})
    a.annotate(f"Mínimo {minimo:%d/%m/%y}: {rp.loc[minimo]:,.0f}".replace(",", "."), xy=(minimo, rp.loc[minimo]),
               xytext=(-10, -5), textcoords="offset points", fontsize=9, ha="right", va="center",
               arrowprops={"arrowstyle": "-", "color": style.MUTED})
    a.set_ylim(300, None)
    fin(a, r, style.INK)
    a.set_title("Riesgo país")
    style.subtitle(a, "Spread EMBI de JP Morgan, puntos básicos (escala log)")
    milei(a)
    fechas(a)

    base = p.loc[:BASE_D].ffill().iloc[-1]
    px = p.loc["2023-06-01":].ffill()
    canasta = 100 * (px[AR] / base[AR]).mean(axis=1)
    a = axes[1]
    a.plot(canasta.index, canasta, color=style.BLUE, label="13 ADRs argentinos")
    for t, color, name in [("SPY", style.MUTED, "S&P 500"), ("EEM", style.YELLOW, "Emergentes (EEM)")]:
        s = 100 * px[t] / base[t]
        a.plot(s.index, s, color=color, lw=1.4, label=name)
        if t == "SPY":
            fin(a, s, color, dx=4)
    fin(a, canasta, style.BLUE)
    a.axhline(100, color=style.INK_2, lw=0.8)
    a.set_yscale("log")
    a.set_yticks([50, 100, 200, 300, 400])
    a.yaxis.set_major_formatter(mtick.ScalarFormatter())
    a.minorticks_off()
    a.set_title("Acciones argentinas en dólares")
    style.subtitle(a, "Canasta equiponderada de ADRs, 8/12/2023 = 100 (escala log)")
    a.legend(loc="upper left")
    milei(a, label=False)
    a.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 7]))
    a.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y"))

    tr, _ = total_return(b.rename(columns=lambda c: c[:-1]).loc["2023-06-01":])
    a = axes[2]
    out = {}
    for t, color in zip(tr.columns, [style.AQUA, style.VIOLET, style.ORANGE]):
        s = tr[t].loc[tr.index > BASE_D].fillna(0).cumsum()
        lvl = 100 * np.exp(s)
        pre_lvl = 100 * np.exp(-tr[t].loc["2023-06-01":BASE_D].iloc[::-1].fillna(0).cumsum())
        full = pd.concat([pre_lvl.iloc[::-1].shift(1).dropna(), pd.Series([100.0], index=[pd.Timestamp(BASE_D)]), lvl])
        full = full[~full.index.duplicated(keep="last")].sort_index()
        a.plot(full.index, full, color=color, label=f"{t}D")
        fin(a, full, color)
        out[t] = full
    a.axhline(100, color=style.INK_2, lw=0.8)
    a.set_title("Bonos soberanos en dólares")
    style.subtitle(a, "Retorno total (precio + cupones + amortizaciones), 7/12/2023 = 100")
    a.legend(loc="upper left")
    milei(a, label=False)
    a.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 7]))
    a.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y"))
    style.source(fig, "Fuente: JP Morgan vía ArgentinaDatos, Yahoo Finance y BYMA vía data912. Último dato: 30/10/2026.")
    style.save(fig, FIG / "08_mercados.png")
    pico = canasta.loc[BASE_D:].idxmax()
    return {"rp_asume": pre, "rp_min": rp.loc[minimo], "rp_min_fecha": minimo, "rp_ultimo": rp.iloc[-1],
            "adr_ultimo": canasta.iloc[-1], "adr_pico": canasta.loc[pico], "adr_pico_fecha": pico,
            "spy_ultimo": 100 * px["SPY"].iloc[-1] / base["SPY"], "bonos": {k: v.iloc[-1] for k, v in out.items()}}


def fig_dolar(dol: pd.DataFrame, ipc: pd.Series, reservas: pd.Series) -> dict:
    mens = dol.resample("MS").mean()
    # Los dos contra el oficial de nov-2023: así se ve también la brecha que había al asumir
    tcr = 100 * mens[["oficial", "CCL"]].div(ipc, axis=0) / (mens["oficial"] / ipc).loc[BASE_M]
    tcr = tcr.dropna().loc["2019-01-01":]
    brecha = 100 * (dol["CCL"] / dol["oficial"] - 1)
    brecha = brecha.dropna().loc["2019-01-01":].rolling(5).mean()
    fig, axes = plt.subplots(1, 3, figsize=(17, 5))
    a = axes[0]
    for c, color, name in [("oficial", style.BLUE, "Oficial"), ("CCL", style.ORANGE, "Contado con liquidación")]:
        a.plot(tcr.index, tcr[c], color=color, label=name)
        fin(a, tcr[c], color)
    a.axhline(100, color=style.INK_2, lw=0.8)
    a.set_title("Dólar real")
    style.subtitle(a, "Promedio mensual deflactado por el IPC, oficial de nov-2023 = 100")
    a.legend(loc="upper right")
    milei(a)
    fechas(a)
    a = axes[1]
    a.plot(brecha.index, brecha, color=style.INK, lw=1.4)
    a.axhline(0, color=style.INK_2, lw=0.8)
    fin(a, brecha, style.INK, "{:.0f}%")
    a.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
    a.set_title("Brecha cambiaria")
    style.subtitle(a, "CCL sobre el oficial mayorista, %, media de 5 ruedas")
    milei(a, label=False)
    fechas(a)
    a = axes[2]
    rv = reservas.loc["2019-01-01":] / 1000
    a.plot(rv.index, rv, color=style.GREEN, lw=1.6)
    fin(a, rv, style.GREEN, "{:.1f}")
    a.set_title("Reservas brutas del BCRA")
    style.subtitle(a, "Miles de millones de dólares")
    milei(a, label=False)
    fechas(a)
    style.source(fig, "Fuente: BCRA (Com. A 3500 y reservas), ArgentinaDatos (CCL) e INDEC. El dólar real no descuenta la "
                      "inflación de EEUU (~3% anual).")
    style.save(fig, FIG / "09_dolar_reservas.png")
    return {"tcr_oficial_pico": tcr["oficial"].loc["2023-12-01":].max(), "tcr_oficial_ultimo": tcr["oficial"].iloc[-1],
            "tcr_fecha": tcr.index[-1], "brecha_nov23": brecha.loc["2023-11-01":"2023-11-30"].mean(),
            "brecha_ultima": brecha.iloc[-1], "reservas_asume": asof(reservas, BASE_D) / 1000,
            "reservas_ultimo": reservas.iloc[-1] / 1000}


def fig_social(q: pd.DataFrame) -> dict:
    pob = pd.Series({pd.Timestamp(f"{k[:4]}-{'04' if k[-1] == '1' else '10'}-01"): v for k, v in POBREZA.items()})
    des = 100 * q["desocupacion"].dropna().loc["2017-01-01":]
    des.index = des.index + pd.DateOffset(months=1, days=14)   # mitad del trimestre
    fig, (a, b) = plt.subplots(1, 2, figsize=(14, 5))
    a.plot(pob.index, pob, color=style.RED, marker="o", ms=4)
    for d in [pd.Timestamp("2023-10-01"), pd.Timestamp("2024-04-01"), pob.index[-2], pob.index[-1]]:
        a.annotate(f"{pob.loc[d]:.1f}%", xy=(d, pob.loc[d]), xytext=(0, 8), textcoords="offset points", ha="center",
                   fontsize=9, color=style.INK, fontweight="bold")
    a.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
    a.set_ylim(20, 58)
    a.set_title("Pobreza")
    style.subtitle(a, "% de personas bajo la línea de pobreza, por semestre (EPH, 31 aglomerados)")
    milei(a)
    fechas(a)
    b.plot(des.index, des, color=style.VIOLET, marker="o", ms=3.5)
    fin(b, des, style.VIOLET, "{:.1f}%")
    b.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
    b.set_title("Desocupación")
    style.subtitle(b, "% de la población económicamente activa, por trimestre")
    milei(b, label=False)
    fechas(b)
    style.source(fig, "Fuente: INDEC, Encuesta Permanente de Hogares.")
    style.save(fig, FIG / "10_pobreza_desempleo.png")
    return {"pobreza": pob, "desocupacion": des}


def main() -> None:
    style.apply()
    plt.rcParams["axes.titlepad"] = 24       # deja lugar al subtítulo debajo del título
    m = load_series(MENSUAL)
    f = load_series(FISCAL)
    q = load_series(TRIMESTRAL)
    energia = load_series(SUBSIDIO_ENERGIA)["sub_energia"]
    ipc = ipc_extendido(m["ipc"])
    var = load_inflacion()
    var.index = var.index.to_period("M").to_timestamp()

    infl = fig_inflacion(var, ipc, m)
    sal = fig_salarios(m, ipc)
    act = fig_actividad(m, q)
    inv = fig_inversion(q)
    fis = fig_fiscal(f, q)
    gas = fig_gasto(f, energia, ipc)
    p = load_prices(AR + ["SPY", "EEM", "EWZ", "^MERV"], start="2019-01-01", how="all")
    mer = fig_mercados(load_riesgo_pais(), p, load_data912(BONOS))
    dol = fig_dolar(load_dolares(), ipc, load_bcra(1, "reservas"))
    soc = fig_social(q)

    nombres = {"sal_priv_reg": "Salario real privado registrado", "sal_publico": "Salario real público",
               "sal_no_reg": "Salario real no registrado", "smvm": "Salario mínimo real",
               "jub_minima": "Jubilación mínima real (sin bono)"}
    rows = [["Inflación mensual", f"{infl['pico_mensual']:.1f}% (dic-23)",
             f"{infl['ultima_mensual']:.1f}% ({infl['ultima_fecha']:%m/%y})"],
            ["Inflación interanual", f"{infl['yoy_pico']:.0f}% (pico {infl['yoy_pico_fecha']:%m/%y})",
             f"{infl['yoy_ultima']:.1f}%"]]
    for k, name in nombres.items():
        d, v, lo, dlo, avg17 = sal[k]
        rows.append([name, "100 (nov-23)", f"{v:.1f} ({d:%m/%y}); piso {lo:.1f} en {dlo:%m/%y}; 2017 = {avg17:.0f}"])
    rows += [["Actividad (EMAE)", "100 (nov-23)",
              f"{act['emae_ultimo']:.1f} ({act['emae_fecha']:%m/%y}); piso {act['emae_piso']:.1f} en {act['emae_piso_fecha']:%m/%y}"],
             ["Crecimiento del PBI", f"2023: {act['pib'].loc['2023']:+.1f}%",
              f"2024: {act['pib'].loc['2024']:+.1f}%; 2025: {act['pib'].loc['2025']:+.1f}%; S1-26: {act['pib'].loc['S1-26']:+.1f}%"],
             ["Inversión (IBIF)", f"2023: {inv['ibif'].loc['2023']:+.1f}%",
              f"2024: {inv['ibif'].loc['2024']:+.1f}%; 2025: {inv['ibif'].loc['2025']:+.1f}%; S1-26: {inv['ibif'].loc['S1-26']:+.1f}%"],
             ["Resultado primario (% PBI)", f"2023: {fis['pct'].loc['2023', 'res_primario']:+.1f}%",
              f"2024: {fis['pct'].loc['2024', 'res_primario']:+.1f}%; 2025: {fis['pct'].loc['2025', 'res_primario']:+.1f}%; "
              f"{fis['pct'].index[-1]}: {fis['pct'].iloc[-1]['res_primario']:+.1f}%"],
             ["Resultado financiero (% PBI)", f"2023: {fis['pct'].loc['2023', 'res_financiero']:+.1f}%",
              f"2024: {fis['pct'].loc['2024', 'res_financiero']:+.1f}%; 2025: {fis['pct'].loc['2025', 'res_financiero']:+.1f}%; "
              f"{fis['pct'].index[-1]}: {fis['pct'].iloc[-1]['res_financiero']:+.1f}%"],
             ["Gasto primario real", "2023 = 100", f"2025: {gas['gasto_total_2025_vs_2023']:+.1f}% contra 2023"],
             ["Riesgo país", f"{mer['rp_asume']:.0f} pb",
              f"mínimo {mer['rp_min']:.0f} ({mer['rp_min_fecha']:%d/%m/%y}); hoy {mer['rp_ultimo']:.0f}"],
             ["ADRs argentinos (USD)", "100", f"{mer['adr_ultimo']:.0f} (pico {mer['adr_pico']:.0f} el {mer['adr_pico_fecha']:%d/%m/%y}); "
              f"S&P 500: {mer['spy_ultimo']:.0f}"],
             ["Bonos (retorno total USD)", "100", "; ".join(f"{k}D: {v:.0f}" for k, v in mer["bonos"].items())],
             ["Dólar oficial real", "100 (nov-23)", f"pico {dol['tcr_oficial_pico']:.0f}; {dol['tcr_oficial_ultimo']:.0f} ({dol['tcr_fecha']:%m/%y})"],
             ["Brecha cambiaria", f"{dol['brecha_nov23']:.0f}% (nov-23)", f"{dol['brecha_ultima']:.0f}%"],
             ["Reservas brutas BCRA", f"US$ {dol['reservas_asume']:.1f} mil M", f"US$ {dol['reservas_ultimo']:.1f} mil M"],
             ["Pobreza (personas)", "41.7% (S2-23)", f"52.9% (S1-24); 28.2% (S2-25); {POBREZA['2026S1']:.1f}% (S1-26)"],
             ["Desocupación", f"{soc['desocupacion'].loc['2023-10-01':'2023-12-31'].iloc[0]:.1f}% (T4-23)",
              f"{soc['desocupacion'].iloc[-1]:.1f}% (T{soc['desocupacion'].index[-1].quarter}-{soc['desocupacion'].index[-1]:%y})"]]
    tabla = tabulate(rows, headers=["Indicador", "Al asumir", "Después"], tablefmt="github")
    rub = tabulate(gas["rubros"].round(1).reset_index().values.tolist(), headers=["Rubro", "Var. real %", "Aporte (pp)"],
                   tablefmt="github")
    pib = tabulate([[k, f"{v:+.1f}"] for k, v in act["pib"].items()], headers=["Año", "PBI %"], tablefmt="github")
    out = (f"# Resultados\n\nGenerado por `estudio/run.py`.\n\n## Tablero\n\n{tabla}\n\n"
           f"Regulados vs núcleo desde nov-23: {100 * infl['regulados_vs_nucleo']:+.0f}% (corrección de tarifas).\n"
           f"Tasa de inversión (IBIF/PBI, precios 2004, 4T): {inv['tasa_inv_2023']:.1f}% en 2023 → "
           f"{inv['tasa_inv_ultima']:.1f}% ({inv['tasa_inv_fecha']:%m/%y}).\n\n"
           f"## Ajuste por rubro, 2025 vs 2023\n\n{rub}\n\n## PBI\n\n{pib}\n\n"
           f"## Resultado fiscal (% PBI)\n\n{fis['pct'].round(2).to_markdown()}\n\n"
           f"## Gasto real (ene-{gas['ult_fiscal']:%m}, 2023 = 100)\n\n{gas['gasto_idx'].round(1).to_markdown()}\n")
    (HERE / "results.md").write_text(out)
    print(out)


if __name__ == "__main__":
    main()
