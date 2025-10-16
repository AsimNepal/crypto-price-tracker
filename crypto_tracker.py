# -------------------------------
# 🪙 CRYPTO PRICE TRACKER
# Author: Asim Nepal
# Description:
#   A Python script that fetches and displays live cryptocurrency data
#   using the CoinGecko API. Supports user input, error handling,
#   and optional live updates.
# -------------------------------

import requests
from prettytable import PrettyTable
import time
import sys

# -------------------------------
# Function: fetch_crypto_data
# Purpose : Fetch cryptocurrency market data from CoinGecko API
# -------------------------------
def fetch_crypto_data(vs_currency='usd', per_page=10):
    """Fetch top cryptocurrencies by market cap from CoinGecko API."""
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': vs_currency,       # Currency to display (e.g., usd, eur)
        'order': 'market_cap_desc',       # Sort by market capitalization
        'per_page': per_page,             # Number of coins to fetch
        'page': 1,                        # Page number
        'sparkline': 'false'              # Disable sparkline data
    }

    try:
        # Send a GET request to the CoinGecko API
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  # Raise exception for bad responses
        return response.json()       # Return parsed JSON data
    except requests.RequestException as e:
        print(f"⚠️ Error fetching data: {e}")
        return []                    # Return empty list if error occurs

# -------------------------------
# Function: display_crypto_table
# Purpose : Display formatted cryptocurrency data in a table
# -------------------------------
def display_crypto_table(data, vs_currency='usd'):
    """Display cryptocurrency data using PrettyTable."""
    table = PrettyTable()
    table.field_names = [
        "Rank", 
        "Name", 
        f"Price ({vs_currency.upper()})", 
        "Market Cap (USD)", 
        "24h Change (%)"
    ]

    # Add each coin's data as a row in the table
    for coin in data:
        table.add_row([
            coin['market_cap_rank'],                       # Rank of coin
            coin['name'],                                  # Coin name
            f"${coin['current_price']:,}",                 # Current price
            f"${coin['market_cap']:,}",                    # Market cap
            f"{coin['price_change_percentage_24h']:.2f}%"  # 24-hour change
        ])

    print(table)

# -------------------------------
# Function: main
# Purpose : Main program logic – handles user input & updates
# -------------------------------
def main():
    print("\n🔹 Welcome to the Crypto Price Tracker 🔹")

    # Ask user for preferred currency (default = USD)
    vs_currency = input("Enter currency (e.g., usd, eur, inr): ").lower() or "usd"

    # Ask user how many top coins to display
    try:
        per_page = int(input("How many top coins to display (1–50)? ") or 10)
    except ValueError:
        per_page = 10

    # Ask user if they want auto-refresh enabled
    auto_refresh = input("Enable live updates? (y/n): ").lower().startswith('y')

    # Infinite loop for live updates (breaks if auto_refresh is False)
    while True:
        data = fetch_crypto_data(vs_currency, per_page)
        if data:
            print("\n" + "=" * 65)
            display_crypto_table(data, vs_currency)
            print("=" * 65 + "\n")

        # If user didn’t enable auto-refresh, exit after one display
        if not auto_refresh:
            break

        # Wait 60 seconds before refreshing the data
        print("🔄 Refreshing in 60 seconds... (Press Ctrl + C to stop)\n")
        time.sleep(60)

        # Clear terminal for cleaner updates (works on most systems)
        sys.stdout.write("\033c")

# -------------------------------
# Entry point of the program
# -------------------------------
if __name__ == "__main__":
    main()
