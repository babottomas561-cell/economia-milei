"""Cash flows and total return of the Argentine Globales (2020 restructuring).

Prices on BYMA are quoted per 100 of ORIGINAL face value, so after an amortization the
price falls by the amount paid without anyone losing money. A price-only index would
show the GD30 losing a third of its value under Milei just because it paid back capital.
Total return adds each payment back on the day the bond goes ex.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

# Annual coupon rate (%) for the accrual year that starts on 9 July of each year (prospectus step-ups).
COUPONS = {
    "GD30": {2020: 0.125, 2021: 0.5, 2022: 0.5, 2023: 0.75, 2024: 0.75, 2025: 0.75, 2026: 0.75},
    "GD35": {2020: 0.125, 2021: 1.125, 2022: 1.5, 2023: 3.625, 2024: 4.125, 2025: 4.125, 2026: 4.125},
    "GD41": {2020: 0.125, 2021: 2.5, 2022: 3.5, 2023: 3.5, 2024: 3.5, 2025: 3.5, 2026: 3.5},
}
# Amortization (% of original face value) by payment date. GD35 and GD41 start after 2027.
AMORT = {"GD30": {pd.Timestamp("2024-07-09"): 4.0,
                  **{pd.Timestamp(year=y, month=m, day=9): 8.0 for y in range(2025, 2031) for m in (1, 7)}},
         "GD35": {}, "GD41": {}}


def cash_flows(bond: str, end: str = "2026-12-31") -> pd.Series:
    """Coupon plus amortization paid on each 9 January / 9 July, per 100 original face value.

    Both payments of calendar year y accrue inside the coupon year that began on 9 July of
    y - 1, so they use that year's rate. The coupon is paid on the face value outstanding
    before that date's amortization."""
    out, residual = {}, 100.0
    for y in range(2021, pd.Timestamp(end).year + 1):
        for m in (1, 7):
            d = pd.Timestamp(year=y, month=m, day=9)
            amort = AMORT[bond].get(d, 0.0)
            out[d] = residual * COUPONS[bond][y - 1] / 100 / 2 + amort
            residual -= amort
    return pd.Series(out, name=bond)


def ex_dates(prices: pd.DataFrame, flows: pd.DataFrame, lookback: int = 5) -> pd.Series:
    """The trading day each payment detached from the price.

    The ex-date moved with BYMA's settlement cycle (T+2 to T+1 in 2024) and with local
    holidays (9 July is one), so it is found in the data: among the ``lookback`` trading
    days up to the payment, the one where adding the payment back leaves the smallest
    returns across all bonds."""
    rets, prev = prices.pct_change(), prices.shift()
    out = {}
    for d in flows.index:
        pos = prices.index.searchsorted(d, side="right")      # trading days up to the payment date
        window = prices.index[max(pos - lookback, 1):pos]
        cost = {t: float(((rets.loc[t] + flows.loc[d] / prev.loc[t]) ** 2).sum()) for t in window}
        out[d] = min(cost, key=cost.get)
    return pd.Series(out, name="ex")


def total_return(prices: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Daily log total return of each bond, plus a table that checks every payment.

    On the ex-date the return is (price + payment) / previous price. If a schedule were
    wrong, that adjusted return would stand out from an ordinary day, so the check table
    reports the raw price change next to the payment and the adjusted return."""
    px = prices.dropna(how="all").ffill()          # un día sin operaciones repite el último precio
    flows = pd.DataFrame({b: cash_flows(b) for b in px.columns})
    flows = flows.loc[(flows.index > px.index[0]) & (flows.index <= px.index[-1])]
    exd = ex_dates(px, flows)
    paid = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    for pay, t in exd.items():
        paid.loc[t] = flows.loc[pay].to_numpy()
    tr = np.log((px + paid) / px.shift())
    check = pd.DataFrame({"ex": exd})
    for b in px.columns:
        check[f"{b} pago"] = flows[b]
        check[f"{b} cambio de precio"] = [px[b].loc[t] - px[b].shift().loc[t] for t in exd]
        check[f"{b} ajustado %"] = [tr[b].loc[t] * 100 for t in exd]
    return tr, check
