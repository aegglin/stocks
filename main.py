import random

import pandas as pd
import requests

from nasdaq import nasdaq_100
from secret_data import ALPHA_VANTAGE_API_KEY


def query_time_series_intramonth_api(symbol, interval="60min", adjusted="true", api="AlphaVantage"):
    """Query API for intramonth data."""
    key = ALPHA_VANTAGE_API_KEY
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={symbol}&interval={interval}&adjusted={adjusted}&apikey={key}"
    r = requests.get(url)
    data = r.json()

    return data


def clean_data(data, symbol):
    """Cleans and transforms the dataset for a given symbol."""
    time_series = data[symbol]['Monthly Time Series']
    for date, values in time_series.items():
        cleaned_dict = {}
        for stat_name, value in values.items():
            stat_name = (
                stat_name.replace("1. ", "")
                    .replace("2. ", "")
                    .replace("3. ", "")
                    .replace("4. ", "")
                    .replace("5. ", "")
            )
            cleaned_dict[stat_name] = value

        time_series[date] = cleaned_dict

        stocks_df = pd.DataFrame(time_series)
        # Transpose the dataframe so the dates are rows
        stocks_df = stocks_df.T

        stocks_df['Date'] = pd.to_datetime(stocks_df['datetime']).dt.date

        stocks_df = stocks_df.drop(columns=['datetime'])

        # Update types
        cols = ['open', 'high', 'low', 'close', 'volume']
        stocks_df[cols] = stocks_df[cols].astype(float)

        stocks_df = stocks_df.rename(columns= {'open':'Open', 'high':'High', 'low':'Low', 'close':'Close', 'volume': 'Volume'})
        stocks_df['StockSymbol'] = symbol

    return stocks_df


def main():
    """Main entry point."""
    chosen_symbols = random.choices(
        nasdaq_100, k=10
    )
    stock_data = {
        symbol: query_time_series_intramonth_api(symbol) for symbol in chosen_symbols
    }

    stocks_df = pd.DataFrame()
    for symbol in chosen_symbols:
        symbol_df = clean_data(stock_data, symbol)
        stocks_df = pd.concat([stocks_df, symbol_df])
    
    stocks_df = stocks_df.reset_index()
    stocks_df.to_csv('result.csv')
if __name__ == "__main__":
    main()
