"""Take ONE snapshot of company data and build the ground truth from it.

Why: share prices change daily. The agent and the ground truth must use the same data, or correct answers will look wrong. Run this once, then never again (unless you deliberately want fresh data and a fresh ground truth).

Run:  python -m tools.snapshot
Makes:
  eval/snapshot.json      the data the agent will read
  eval/ground_truth.csv   the correct answers, to spot-check by hand
"""
import csv
import json
import time
from datetime import date
from pathlib import Path

from tools.data import get_company_data

TICKERS = {
    "JPM": "Banks", "BAC": "Banks", "GS": "Banks",
    "AAPL": "Tech", "MSFT": "Tech", "NVDA": "Tech",
    "KO": "Consumer", "PG": "Consumer", "WMT": "Consumer", "MCD": "Consumer",
}

EVAL = Path("eval")


def to_millions(x):
    return round(float(x) / 1e6, 1) if x is not None else None


def main():
    snapshot, rows = {}, []
    for ticker, sector in TICKERS.items():
        print(f"Fetching {ticker}...")
        d = get_company_data(ticker)
        snapshot[ticker] = d
        inc = d["income_statement"]
        revenue = to_millions(inc.get("Total Revenue"))
        net_income = to_millions(inc.get("Net Income"))
        margin = round(net_income / revenue * 100, 2) if revenue and net_income else None
        rows.append({
            "ticker": ticker,
            "sector": sector,
            "company": d["company"],
            "fiscal_year": d["fiscal_year_end"],
            "revenue_usd_m": revenue,
            "net_income_usd_m": net_income,
            "net_margin_pct": margin,
            "price_change_1y_pct": d["price_change_1y_pct"],
            "key_risk": "",
            "source_notes": f"yfinance snapshot {date.today()}",
        })
        time.sleep(1)  # be polite to Yahoo Finance

    (EVAL / "snapshot.json").write_text(json.dumps(snapshot, indent=2, default=str))
    with open(EVAL / "ground_truth.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)

    print("\nSaved eval/snapshot.json and eval/ground_truth.csv")
    for r in rows:
        if None in (r["revenue_usd_m"], r["net_income_usd_m"]):
            print(f"  Check {r['ticker']}: missing revenue or net income")


if __name__ == "__main__":
    main()
