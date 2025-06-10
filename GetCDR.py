import pandas as pd
import openpyxl

Canada_CDR_df = pd.read_excel("CIBC_CDR_EN.xlsx")

Existent_CDR_df = Canada_CDR_df[:]["CDR Ticker"].to_frame()
Existent_CDR_df = Existent_CDR_df.rename(columns={"CDR Ticker": "Symbol"})

from GetTier2DividendSymbol import tier2_dividend_df

matched_cdr_us_stocks_df = pd.merge(
    Existent_CDR_df,                              # The DataFrame derived from your CDR Series
    tier2_dividend_df,         # Your American stocks DataFrame, with the renamed column
    on='Symbol',                         # The common column to merge on
    how='inner'                          # Specifies an inner join (intersection)
)
print(matched_cdr_us_stocks_df)

