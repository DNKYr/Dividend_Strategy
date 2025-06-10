# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import pandas as pd
from bs4 import BeautifulSoup
import requests
import yfinance as yf

#Get market components

#Web Scalping Wikipedia
def get_wikipedia_table(URL, table_class_name = None, table_id = None, table_index = 1):
    try:
        response = requests.get(URL)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"fetching error URL: {URL} : {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    tables = soup.find_all('table', class_='wikitable')  # Wikipedia tables often have 'wikitable' class

    if not tables:
        print("There are no tables")
        return None

    target_table = None
    if table_id:
        target_table = soup.find('table', id=table_id)
        if not target_table:
            print(f"No table found with id='{table_id}'.")
            return None
    elif table_class_name:
        target_table = soup.find('table', class_=table_class_name)
        if not target_table:
            print(f"No table found with class='{table_class_name}'.")
            return None
    elif tables and 0 <= table_index < len(tables):
        target_table = tables[table_index]
    else:
        print(f"Table at index {table_index} not found.")
        return None

    if not target_table:
        print("Could not identify the target table.")
        return None

    # Extract table headers
    headers = []
    # Find headers (<th>) within the first row (<tr>) of the table head (<thead>) if present
    # Or just find all <th> if no thead
    if target_table.find('thead'):
        header_row = target_table.find('thead').find('tr')
    else:
        header_row = target_table.find('tr')  # Assume first row is header if no thead

    if header_row:
        for th in header_row.find_all(['th', 'td']):  # Sometimes headers are <td>
            headers.append(th.get_text(strip=True))
    else:
        print("Could not find table headers.")
        return None

    # Extract table rows and data
    data = []
    # Find all data rows (<tr>) in the table body (<tbody>) if present, otherwise directly in table
    rows = target_table.find('tbody').find_all('tr') if target_table.find('tbody') else target_table.find_all('tr')[
                                                                                        1:]  # Skip header row

    for row in rows:
        cols = row.find_all(['td', 'th'])  # Get all cells, including potential row headers (<th>) in data rows
        cols = [ele.get_text(strip=True) for ele in cols]
        if cols:  # Ensure row is not empty
            data.append(cols)

    # Clean up headers if there are multi-level headers or odd formatting
    # This is a basic cleanup, more complex tables might need specialized parsing
    if headers and len(headers) != len(data[0]):
        # This is a common issue with complex Wikipedia tables where the number of
        # headers doesn't match the number of cells per row due to colspan/rowspan.
        # For simplicity, we'll try to use the number of columns in the first data row.
        # For S&P 500, we'll try to ensure we have the correct columns.
        print(
            "Warning: Number of headers does not match number of columns in data rows. Adjusting headers if possible.")
        # For S&P 500, we know the typical columns: Symbol, Security, GICS Sector, GICS Sub-Industry, Headquarters, Date added, CIK, Founded
        expected_headers = ['Symbol', 'Security', 'GICS Sector', 'GICS Sub-Industry', 'Headquarters', 'Date added',
                            'CIK', 'Founded']
        if len(data) > 0 and len(data[0]) == len(expected_headers):
            headers = expected_headers
        else:
            # Fallback: create generic headers if a mismatch is still there
            headers = [f'Column {i + 1}' for i in range(len(data[0]))]

    # Create a Pandas DataFrame
    try:
        df = pd.DataFrame(data, columns=headers[:len(data[0])])  # Slice headers to match actual column count
        # Clean up the 'Symbol' column if it contains extra characters (e.g., footnotes)
        if 'Symbol' in df.columns:
            df['Symbol'] = df['Symbol'].str.replace(r'\[.*?\]', '', regex=True).str.strip()
        return df
    except ValueError as e:
        print(f"Error creating DataFrame: {e}")
        print(f"Headers: {headers}")
        if data:
            print(f"First row data: {data[0]}")
        return None

#SP500 component info
SP500_Url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"


SP500_df = get_wikipedia_table(SP500_Url, None,None, 0)

#Parsing the original table into its component
SP500_symbol_df = SP500_df[1:]["Symbol"]

stock_dividend_info = []
for symbol in SP500_symbol_df:
    info = yf.Ticker(symbol).info
    dividend_yield = info.get('dividendYield')
    stock_dividend_info.append((symbol, dividend_yield))

df = pd.DataFrame(stock_dividend_info)
print(df)

file_name = "S&P 500 constituent dividend info"

df.to_csv(file_name, index=False)



