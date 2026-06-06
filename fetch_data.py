from pathlib import Path

import yfinance as yf

BASE_DIR = Path(__file__).parent
MARKET_DATA_PATH = BASE_DIR / "market_data.csv"

stocks = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "ICICIBANK.NS",
    "SBIN.NS",
    "TATAPOWER.NS",
    "SUNPHARMA.NS",
    "ADANIPOWER.NS",
    "TATAMOTORS.NS",
]


def generate_csv(risk, amount, horizon="MEDIUM"):
    with open(MARKET_DATA_PATH, "w") as f:
        f.write(
            f"{risk},{amount},{horizon}\n"
        )

        f.write(
            "Stock,CurrentPrice,Growth,Volatility\n"
        )

        for stock in stocks:

            df = yf.download(
                stock,
                period="6mo",
                progress=False
            )

            if df.empty:
                continue

            close_prices = df["Close"].squeeze()
            current = float(close_prices.iloc[-1])
            growth = ((current - float(close_prices.iloc[0]))/float(close_prices.iloc[0])) * 100
            volatility = float(close_prices
                          .pct_change()
                          .std()*100)
            f.write(
                f"{stock},{current:.2f},{growth:.2f},{volatility:.2f}\n"
            )
