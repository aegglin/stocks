
import json
import random

import matplotlib.pyplot as plt
import pandas as pd
import requests

from api_keys import ALPHA_VANTAGE_API_KEY
from nasdaq import nasdaq_100
from log import get_log

log = get_log()

def query_time_series_intraday_api(symbol, interval="60min", adjusted="true"):
    function = "TIME_SERIES_INTRADAY"
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

    # Update types
    stocks_df.index = pd.to_datetime(stocks_df.index)
    cols = ['open', 'high', 'low', 'close', 'volume']
    stocks_df[cols] = stocks_df[cols].astype(float)

    return stocks_df


def show_graphs(df, symbol):
    
    fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(15, 7))
    ax1, ax2, ax3, ax4 = ax.flatten()

    ax1.set_title(f'{symbol} Price at Open')
    ax1.set_xlabel('$x$ -- Date')
    ax1.set_ylabel('$y$ -- Price at Open')
    ax1.tick_params("x", rotation=45)
    ax1.plot(df.index, df['open'])

    ax2.set_title(f'{symbol} High Price')
    ax2.set_xlabel('$x$ -- Date')
    ax2.set_ylabel('$y$ -- High Price')
    ax2.tick_params("x", rotation=45)
    ax2.yaxis.tick_right()
    ax2.plot(df.index, df['high'])

    ax3.set_title(f'{symbol} Low Price')
    ax3.set_xlabel('$x$ -- Date')
    ax3.set_ylabel('$y$ -- Low Price')
    ax3.tick_params("x", rotation=45)
    ax3.plot(df.index, df['low'])

    ax4.set_title(f'{symbol} Price at Close')
    ax4.set_xlabel('$x$ -- Date')
    ax4.set_ylabel('$y$ -- Price at Close')
    ax4.tick_params("x", rotation=45)
    ax4.yaxis.tick_right()
    ax4.plot(df.index, df['close'])


    fig.tight_layout()

    plt.show()

def main():

    chosen_symbols = random.choices(
        nasdaq_100, k=1
    )  # temporarily use one symbol to test
    stock_data = {
        symbol: query_time_series_intraday_api(symbol) for symbol in chosen_symbols
    }

    stocks_df = clean_data(stock_data, chosen_symbols[0], "60min")
    # log.info(stocks_df.head())

    show_graphs(stocks_df, chosen_symbols[0])


if __name__ == "__main__":
    main()
