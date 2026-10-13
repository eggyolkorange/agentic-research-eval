"""Data fetchers. Start here on day 1."""
import yfinance as yf


def get_company_data(ticker: str) -> dict:
    t = yf.Ticker(ticker)
    info = t.info
    income = t.income_stmt  # annual, most recent column first
    hist = t.history(period="1y")
    return {
        "ticker": ticker,
        "company": info.get("longName"),
        "sector": info.get("sector"),
        "income_statement": income.iloc[:, 0].dropna().to_dict() if not income.empty else {},
        "fiscal_year_end": str(income.columns[0].date()) if not income.empty else None,
        "price_change_1y_pct": round((hist["Close"].iloc[-1] / hist["Close"].iloc[0] - 1) * 100, 2) if len(hist) else None,
    }
    # TODO: add a SEC EDGAR fetch for the 10-K risk section


if __name__ == "__main__":
    for tk in ["JPM", "AAPL", "KO"]:
        d = get_company_data(tk)
        print(tk, d["company"], d["fiscal_year_end"], d["price_change_1y_pct"])
