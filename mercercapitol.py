import requests
import pandas as pd
from datetime import datetime
import plotly.express as px
import streamlit as st

# Define the amount of Bitcoin holdings
btc_holdings = 0.20160304

def fetch_historical_data(coin_id='bitcoin', vs_currency='usd', days='max'):
    """Fetch historical price data for a given coin from CoinGecko."""
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {
        'vs_currency': vs_currency,
        'days': days
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    # Convert to DataFrame
    prices = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
    
    # Convert timestamp to datetime
    prices['date'] = pd.to_datetime(prices['timestamp'], unit='ms')
    
    # Set date as index
    prices.set_index('date', inplace=True)
    
    # Resample to monthly and calculate average
    monthly_prices = prices['price'].resample('M').mean().reset_index()
    
    return monthly_prices

def fetch_current_price(coin_id='bitcoin', vs_currency='usd'):
    """Fetch the current live price of a given coin from CoinGecko."""
    url = f"https://api.coingecko.com/api/v3/simple/price"
    params = {
        'ids': coin_id,
        'vs_currencies': vs_currency
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data[coin_id][vs_currency]

# Fetch current live price of Bitcoin
current_price = fetch_current_price()

# Fetch historical Bitcoin data
historical_data = fetch_historical_data()
print (historical_data)



# Calculate the value of your holdings for each month
historical_data['holdings_value'] = historical_data['price'] * btc_holdings

# Creating a line chart for average price and holdings value
fig = px.line(historical_data, x='date', y='price', title='Bitcoin Price and Holdings Value Over Time')
fig.add_scatter(x=historical_data['date'], y=historical_data['holdings_value'], mode='lines', name='Holdings Value')


# Creating a line chart
fig = px.line(historical_data, x='date', y='price', title='Average Monthly Bitcoin Price Since 2011')

# Streamlit app layout
st.title('Bitcoin Price Analysis')
st.write('This graph shows the average price of Bitcoin since 2011 per month, with the most current month showing the actual live price.')
st.plotly_chart(fig)