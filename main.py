import random

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import requests
from scipy.stats.stats import pearsonr
from sklearn import linear_model
from sqlalchemy import select


from log import get_log
from models import StockSymbol, StockPrice, Date
from nasdaq import nasdaq_100
from secret_data import ALPHA_VANTAGE_API_KEY
from stocks_db import Connection


"""
    Ideas:
         - Add more logging throughout
         - Break up into multiple files/classes
         - Update README.md

         col names: 
         StockPriceId
            ,Symbol
            ,Date
            ,Time
            ,HighPrice
            ,LowPrice
            ,OpenPrice
            ,ClosePrice
            ,Volume
            ,DateId
            ,StockSymbolId
"""

log = get_log()

def query_time_series_intraday_api(symbol, interval="60min", adjusted="true"):
    key = ALPHA_VANTAGE_API_KEY

    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&adjusted={adjusted}&apikey={key}"
    r = requests.get(url)
    data = r.json()

    # log.info(json.dumps(data, indent=4))

    return data

def linear_regression(symbol, start_date, end_date, cols):
    query = f"""SELECT *
FROM Stocks.Ref.StockPrices
WHERE Symbol='{symbol}'
    AND [Date] BETWEEN '{start_date}' AND '{end_date}';
    """

    connection = Connection()
    result = connection._sa_execute(query)
    
    x_col = cols[0]
    y_col = cols[1]

    # Put data in the format that fit() expects
    y = result[y_col].values[:, np.newaxis] # reshape ((-1, 1)) also will make this into one column and len(y) rows 
    x = result[x_col].values

    corr, p = pearsonr(x, y)
    log.info(f"Corr is: {corr}, p is: {p}")

    model = linear_model.LinearRegression()
    model.fit(x, y)
    r_sq = model.score(x, y)
    log.info(f"coefficient of determination: {r_sq}")
    log.info(f"intercept: {model.intercept_}") # scalar
    log.info(f"slope: {model.coef_}") # sarray

    plt.scatter(x, y, color='g')
    plt.plot(x, model.predict(x), color='k')

    plt.show()

def multiple_linear_regression(symbol, start_date, end_date, cols):
    query = f"""SELECT *
FROM Stocks.Ref.StockPrices
WHERE Symbol='{symbol}'
    AND [Date] BETWEEN '{start_date}' AND '{end_date}';
    """

    connection = Connection()
    result = connection._sa_execute(query)
    
    x_col = cols[0]
    y_cols = cols[1]

    # Put data in the format that fit() expects
    y = result[y_cols].values.reshape ((-1, 1))
    x = result[x_col].values

    corr, p = pearsonr(x, y)
    log.info(f"Corr is: {corr}, p is: {p}")

    model = linear_model.LinearRegression()
    model.fit(x, y)
    r_sq = model.score(x, y)

    log.info(f"coefficient of determination: {r_sq}")
    log.info(f"intercept: {model.intercept_}") # scalar
    log.info(f"slope: {model.coef_}") # sarray

    plt.scatter(x, y, color='g')
    plt.plot(x, model.predict(x), color='k')

    plt.show()


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


def graph_symbol_matplotlib(symbol, df):
    
    fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(15, 7))
    ax1, ax2, ax3, ax4 = ax.flatten()

    # Configure the first graph
    ax1.set_title(f'{symbol} Price at Open')
    ax1.set_xlabel('$x$ -- Date')
    ax1.set_xlim(xmin=df.index.min(), xmax=df.index.max())
    ax1.set_ylabel('$y$ -- Price at Open')
    ax1.set_ylim(ymin=df['open'].min(), ymax=df['open'].max())
    ax1.tick_params("x", rotation=45)
    ax1.plot(df.index, df['open'], color='#FD8A8A', linewidth=3)
    ax1.grid()

    # Configure the second graph
    ax2.set_title(f'{symbol} High Price')
    ax2.set_xlabel('$x$ -- Date')
    ax2.set_xlim(xmin=df.index.min(), xmax=df.index.max())
    ax2.set_ylabel('$y$ -- High Price')
    ax2.set_ylim(ymin=df['high'].min(), ymax=df['high'].max())
    ax2.tick_params("x", rotation=45)
    ax2.yaxis.tick_right()
    ax2.plot(df.index, df['high'], color='#F1F7B5', linewidth=3)
    ax2.grid()

    # Configure the third graph
    ax3.set_title(f'{symbol} Low Price')
    ax3.set_xlabel('$x$ -- Date')
    ax3.set_xlim(xmin=df.index.min(), xmax=df.index.max())
    ax3.set_ylabel('$y$ -- Low Price')
    ax3.set_ylim(ymin=df['low'].min(), ymax=df['low'].max())
    ax3.tick_params("x", rotation=45)
    ax3.plot(df.index, df['low'], color='#ABD1D1', linewidth=3)
    ax3.grid()

    # Configure the fourth graph
    ax4.set_title(f'{symbol} Price at Close')
    ax4.set_xlabel('$x$ -- Date')
    ax4.set_xlim(xmin=df.index.min(), xmax=df.index.max())
    ax4.set_ylabel('$y$ -- Price at Close')
    ax4.set_ylim(ymin=df['close'].min(), ymax=df['close'].max())
    ax4.tick_params("x", rotation=45)
    ax4.yaxis.tick_right()
    ax4.plot(df.index, df['close'], color='#9EA1D4', linewidth=3)
    ax4.grid()

    fig.tight_layout()

    plt.show()


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

    connection = Connection()
    with connection._session as session:
        for _, row in stocks_df.iterrows():
            date_id_stmt = select(Date.DateId)
            date_id_stmt = date_id_stmt.where(Date.Date == row['Date'])
            date_id = session.execute(date_id_stmt).scalar_one()

            symbol_id_stmt = select(StockSymbol.StockSymbolId)
            symbol_id_stmt = symbol_id_stmt.where(StockSymbol.Symbol == row['StockSymbol'])
            symbol_id = session.execute(symbol_id_stmt).scalar_one()

            stock_price = StockPrice(DateId=date_id, Time=row['Time'], StockSymbolId=symbol_id, HighPrice=row['High'], LowPrice=row['Low'], OpenPrice=row['Open'], ClosePrice=row['Close'], Volume=row['Volume']) 

            session.add(stock_price)
        session.commit()
    
if __name__ == "__main__":
    main()
