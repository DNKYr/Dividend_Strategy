import pandas as pd

df = pd.read_csv("S&P 500 constituent dividend info")

df = df.sort_values(by="Dividend Yield", ascending=False)

tier2_dividend_df = df[99:201]

tier2_dividend_df = tier2_dividend_df.sort_values(by="Market Capitalization", ascending=False)
total_market_capitalization = tier2_dividend_df["Market Capitalization"].sum()

