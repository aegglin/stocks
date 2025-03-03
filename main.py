import json
import random
import requests

import pandas as pd

from secrets import ALPHA_VANTAGE_API_KEY


def query_time_series_intraday_api(symbol, interval="60min", adjusted="true"):
    function = "TIME_SERIES_INTRADAY"
    key = ALPHA_VANTAGE_API_KEY

    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&adjusted={adjusted}&apikey={key}"
    r = requests.get(url)
    data = r.json()

    print(json.dumps(data, indent=4))

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

    return pd.DataFrame(time_series)


def main():

    nasdaq_100 = [
        "AAPL",
        "NVDA",
        "MSFT",
        "AMZN",
        "GOOG",
        "GOOGL",
        "META",
        "AVGO",
        "TSLA",
        "COST",
        "NFLX",
        "TMUS",
        "ASML",
        "CSCO",
        "AZN",
        "LIN",
        "PLTR",
        "PEP",
        "ISRG",
        "ADBE",
        "TXN",
        "QCOM",
        "INTU",
        "AMD",
        "PDD",
        "BKNG",
        "AMGN",
        "ARM",
        "GILD",
        "HON",
        "AMAT",
        "CMCSA",
        "SBUX",
        "ADP",
        "PANW",
        "VRTX",
        "ADI",
        "APP",
        "MELI",
        "MU",
        "LRCX",
        "INTC",
        "KLAC",
        "CRWD",
        "ABNB",
        "CEG",
        "FTNT",
        "DASH",
        "CTAS",
        "MRVL",
        "MDLZ",
        "MAR",
        "ORLY",
        "REGN",
        "TEAM",
        "SNPS",
        "WDAY",
        "PYPL",
        "CDNS",
        "MSTR",
        "ROP",
        "CSX",
        "ADSK",
        "NXPI",
        "AEP",
        "CHTR",
        "PCAR",
        "CPRT",
        "PAYX",
        "MNST",
        "ROST",
        "KDP",
        "LULU",
        "FANG",
        "EXC",
        "AXON",
        "BKR",
        "FAST",
        "CTSH",
        "GEHC",
        "VRSK",
        "XEL",
        "CCEP",
        "DDOG",
        "ODFL",
        "IDXX",
        "TTWO",
        "KHC",
        "TTD",
        "DXCM",
        "EA",
        "MCHP",
        "CSGP",
        "ZS",
        "ANSS",
        "WBD",
        "CDW",
        "GFS",
        "ON",
        "BIIB",
    ]

    chosen_symbol = random.choices(
        nasdaq_100, k=1
    )  # temporarily use one symbol to test
    stock_data = {
        symbol: query_time_series_intraday_api(symbol) for symbol in chosen_symbol
    }

    stocks_df = clean_data(stock_data, chosen_symbol, "60min")

    # Transpose the dataframe so the dates are rows
    stocks_df = stocks_df.T
    print(stock_data.head())


if __name__ == "__main__":
    main()
