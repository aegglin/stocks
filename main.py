import random

import pandas as pd
import requests

from nasdaq import nasdaq_100
from secret_data import ALPHA_VANTAGE_API_KEY


def query_time_series_intraday_api(symbol, interval="60min", adjusted="true"):
    key = ALPHA_VANTAGE_API_KEY

    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&adjusted={adjusted}&apikey={key}"
    r = requests.get(url)
    data = r.json()

    # log.info(json.dumps(data, indent=4))

    return data


def clean_data(data, symbol, interval):

    time_series = data[symbol][f"Time Series ({interval})"]
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

    stocks_df = stocks_df.reset_index(names='datetime')
    stocks_df['datetime'] = pd.to_datetime(stocks_df['datetime'])

    stocks_df['Date'] = stocks_df['datetime'].dt.date
    stocks_df['Time'] = stocks_df['datetime'].dt.time

    # Update types
    # stocks_df.index = pd.to_datetime(stocks_df.index)
    cols = ['open', 'high', 'low', 'close', 'volume']
    stocks_df[cols] = stocks_df[cols].astype(float)

    stocks_df = stocks_df.rename(columns= {'open':'Open', 'high':'High', 'low':'Low', 'close':'Close', 'volume': 'Volume'})
    stocks_df['StockSymbol'] = symbol

    return stocks_df


def main():

    chosen_symbols = random.choices(
        nasdaq_100, k=10
    )  # temporarily use one symbol to test
    stock_data = {
        symbol: query_time_series_intraday_api(symbol) for symbol in chosen_symbols
    }

    stocks_df = pd.DataFrame()
    for symbol in chosen_symbols:
        symbol_df = clean_data(stock_data, symbol, "60min")
        stocks_df = pd.concat([stocks_df, symbol_df])
    
    stocks_df = stocks_df.reset_index()

    stocks_df.to_csv('result.csv')
if __name__ == "__main__":
    main()
