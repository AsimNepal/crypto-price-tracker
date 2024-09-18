import requests
from prettytable import PrettyTable

# Fetch data from the CoinGecko API
url = "https://api.coingecko.com/api/v3/coins/markets"
params = {
    'vs_currency': 'usd',
    'order': 'market_cap_desc',
    'per_page': 5,
    'page': 1,
    'sparkline': 'false'
}

response = requests.get(url, params=params)
data = response.json()

# Create a table to display the data
table = PrettyTable()
table.field_names = ["Cryptocurrency", "Price (USD)", "Market Cap", "24h Change (%)"]

for coin in data:
    table.add_row([coin['name'], f"${coin['current_price']}", f"${coin['market_cap']:,}", f"{coin['price_change_percentage_24h']:.2f}%"])

print(table)
