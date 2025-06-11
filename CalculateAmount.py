from GetCDR import matched_cdr_us_stocks_df
import pandas as pd

total_investment = float(input())

amount = total_investment/len(matched_cdr_us_stocks_df)
print(amount)