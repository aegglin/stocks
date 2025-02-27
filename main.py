import json
import random
import requests

from secrets import ALPHA_VANTAGE_API_KEY

def query_time_series_intraday_api(symbol, interval='60min', adjusted='true'):
    function = 'TIME_SERIES_INTRADAY'
    key = ALPHA_VANTAGE_API_KEY
    
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&adjusted={adjusted}&apikey={key}"
    r = requests.get(url)
    data = r.json()

    print(json.dumps(data, indent=4))

    return data

def main():

    nasdaq_100 = ['AAPL',
        'NVDA',
        'MSFT',
        'AMZN',
        'GOOG',
        'GOOGL',
        'META',
        'AVGO',
        'TSLA',
        'COST',
        'NFLX',
        'TMUS',
        'ASML',
        'CSCO',
        'AZN',
        'LIN',
        'PLTR',
        'PEP',
        'ISRG',
        'ADBE',
        'TXN',
        'QCOM',
        'INTU',
        'AMD',
        'PDD',
        'BKNG',
        'AMGN',
        'ARM',
        'GILD',
        'HON',
        'AMAT',
        'CMCSA',
        'SBUX',
        'ADP',
        'PANW',
        'VRTX',
        'ADI',
        'APP',
        'MELI',
        'MU',
        'LRCX',
        'INTC',
        'KLAC',
        'CRWD',
        'ABNB',
        'CEG',
        'FTNT',
        'DASH',
        'CTAS',
        'MRVL',
        'MDLZ',
        'MAR',
        'ORLY',
        'REGN',
        'TEAM',
        'SNPS',
        'WDAY',
        'PYPL',
        'CDNS',
        'MSTR',
        'ROP',
        'CSX',
        'ADSK',
        'NXPI',
        'AEP',
        'CHTR',
        'PCAR',
        'CPRT',
        'PAYX',
        'MNST',
        'ROST',
        'KDP',
        'LULU',
        'FANG',
        'EXC',
        'AXON',
        'BKR',
        'FAST',
        'CTSH',
        'GEHC',
        'VRSK',
        'XEL',
        'CCEP',
        'DDOG',
        'ODFL',
        'IDXX',
        'TTWO',
        'KHC',
        'TTD',
        'DXCM',
        'EA',
        'MCHP',
        'CSGP',
        'ZS',
        'ANSS',
        'WBD',
        'CDW',
        'GFS',
        'ON',
        'BIIB',
    ]

    chosen_symbols = random.choices(nasdaq_100, k=20)
    stock_data = {symbol: query_time_series_intraday_api(symbol) for symbol in chosen_symbols}

if __name__ == '__main__':
    main()
