import pandas as pd

#Created dataframe
df = pd.read_csv("S&P 500 constituent dividend info")

#Sort df by Dividend Yield
df = df.sort_values(by="Dividend Yield", ascending=False)

#Get the tier 2 stock by dividend yield
tier2_dividend_df = df[99:201]

#Calculate the
tier2_dividend_df = tier2_dividend_df.sort_values(by="Market Capitalization", ascending=False)
total_market_capitalization = tier2_dividend_df["Market Capitalization"].sum()

def get_weight(market_cap):
    return f"{market_cap/total_market_capitalization*100}%"

tier2_dividend_df['Weight'] = tier2_dividend_df['Market Capitalization'].apply(get_weight)
