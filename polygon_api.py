import requests
import json
import pandas as pd

from secrets import POLYGON_API_KEY

# Get data for a specific stock over a given range
r = requests.get(f'https://api.polygon.io/v2/aggs/ticker/AAPL/range/1/day/2021-07-22/2021-07-22?adjusted=true&sort=asc&limit=120&apiKey={POLYGON_API_KEY}')
response_data = r.json()

print(f'JSON is: {response_data}')
print(response_data.get('results'))
# c (close), h (highest), l (lowest), n (number of transactions), o (open), otc (OTC ticker or not), t (timestamp), v (trading volume), vw (volume weighted average price)


r = requests.get(f'https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/2022-10-14?adjusted=true&apiKey={POLYGON_API_KEY}')
response_data = r.json()
print(f'JSON is: {response_data}')
print(response_data.get('results'))

df = pd.DataFrame(response_data['results'])