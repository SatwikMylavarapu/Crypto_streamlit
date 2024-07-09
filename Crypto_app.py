import streamlit as st
from PIL import Image
import pandas as pd
import base64
import requests
import plotly.express as px
import os

# Page layout
st.set_page_config(layout="wide")

# Custom CSS for sidebar styling
st.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        background: linear-gradient(to bottom, #3a7bd5, #3a6073);
        color: white;
    }
    .sidebar .sidebar-content .block-container {
        padding-top: 2rem;
    }
    .sidebar .sidebar-content .stSlider {
        color: black;
    }
    .css-1aumxhk {
        background-color: #f8f9fa;
    }
    .css-1wqnpfq {
        color: #FF0000;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
image_path = os.path.join(os.path.dirname(__file__), 'crypto.png')
image = Image.open(image_path)
st.image(image, width=500)
st.title('Crypto Price App')
st.markdown("""
This app retrieves cryptocurrency prices for the top 100 cryptocurrency from the **CoinMarketCap**!
""")

# About
expander_bar = st.expander("About")
expander_bar.markdown("""
* **Python libraries:** base64, pandas, streamlit, numpy, matplotlib, seaborn, requests, json, time
* **Data source:** [CoinMarketCap](http://coinmarketcap.com).
* **Credit:** Web scraper adapted from the Medium article *[Web Scraping Crypto Prices With Python](https://towardsdatascience.com/web-scraping-crypto-prices-with-python-41072ea5b5bf)* written by [Bryan Feng](https://medium.com/@bryanf).
""")

# Sidebar + Main panel
col1 = st.sidebar
col2, col3 = st.columns((2, 1))

# Sidebar
col1.header('Input Options')

# Currency price unit
currency_price_unit = col1.selectbox('Select currency for price', ('USD', 'BTC', 'ETH', 'SOL'))

# CoinMarketCap API key
api_key = 'a932d2b8-aa3f-4477-8915-ce8c024c5928'  # Your CoinMarketCap API key

# Web scraping of CoinMarketCap data
@st.cache_data
def load_data():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '1',
        'limit': '100',
        'convert': currency_price_unit
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }
    
    response = requests.get(url, headers=headers, params=parameters)
    data = response.json()['data']
    
    coin_name = []
    coin_symbol = []
    market_cap = []
    percent_change_1h = []
    percent_change_24h = []
    percent_change_7d = []
    price = []
    volume_24h = []

    for coin in data:
        coin_name.append(coin['name'])
        coin_symbol.append(coin['symbol'])
        price.append(coin['quote'][currency_price_unit]['price'])
        percent_change_1h.append(coin['quote'][currency_price_unit]['percent_change_1h'])
        percent_change_24h.append(coin['quote'][currency_price_unit]['percent_change_24h'])
        percent_change_7d.append(coin['quote'][currency_price_unit]['percent_change_7d'])
        market_cap.append(coin['quote'][currency_price_unit]['market_cap'])
        volume_24h.append(coin['quote'][currency_price_unit]['volume_24h'])

    df = pd.DataFrame(columns=['coin_name', 'coin_symbol', 'market_cap', 'percent_change_1h', 'percent_change_24h', 'percent_change_7d', 'price', 'volume_24h'])
    df['coin_name'] = coin_name
    df['coin_symbol'] = coin_symbol
    df['price'] = price
    df['percent_change_1h'] = percent_change_1h
    df['percent_change_24h'] = percent_change_24h
    df['percent_change_7d'] = percent_change_7d
    df['market_cap'] = market_cap
    df['volume_24h'] = volume_24h
    return df

df = load_data()

# Sidebar - Cryptocurrency selections
sorted_coin = sorted(df['coin_symbol'])
selected_coin = col1.multiselect('Cryptocurrency', sorted_coin, sorted_coin)

df_selected_coin = df[df['coin_symbol'].isin(selected_coin)]  # Filtering data

# Sidebar - Number of coins to display
num_coin = col1.slider('Display Top N Coins', 1, 100, 100)
df_coins = df_selected_coin[:num_coin]

# Sidebar - Percent change timeframe
percent_timeframe = col1.selectbox('Percent change time frame', ['7d', '24h', '1h'])
percent_dict = {"7d": 'percent_change_7d', "24h": 'percent_change_24h', "1h": 'percent_change_1h'}
selected_percent_timeframe = percent_dict[percent_timeframe]

# Sidebar - Sorting values
sort_values = col1.selectbox('Sort values?', ['Yes', 'No'])

col2.subheader('Price Data of Selected Cryptocurrency')
col2.write('Data Dimension: ' + str(df_selected_coin.shape[0]) + ' rows and ' + str(df_selected_coin.shape[1]) + ' columns.')
col2.dataframe(df_coins.style.set_properties(**{'background-color': 'black', 'color': 'white', 'border-color': 'red'}))

# Download CSV data
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="crypto.csv">Download CSV File</a>'
    return href

col2.markdown(filedownload(df_selected_coin), unsafe_allow_html=True)

# Preparing data for Bar plot of % Price change
col2.subheader('Price Change')
df_change = pd.concat([df_coins.coin_symbol, df_coins.percent_change_1h, df_coins.percent_change_24h, df_coins.percent_change_7d], axis=1)
df_change = df_change.set_index('coin_symbol')
df_change['positive_percent_change_1h'] = df_change['percent_change_1h'] > 0
df_change['positive_percent_change_24h'] = df_change['percent_change_24h'] > 0
df_change['positive_percent_change_7d'] = df_change['percent_change_7d'] > 0
col2.dataframe(df_change.style.applymap(lambda x: 'color: red' if x < 0 else 'color: green', subset=['percent_change_1h', 'percent_change_24h', 'percent_change_7d']))

# Conditional creation of interactive plots using Plotly
col3.subheader('Bar plot of % Price Change')

if percent_timeframe == '7d':
    if sort_values == 'Yes':
        df_change = df_change.sort_values(by=['percent_change_7d'])
    fig = px.bar(df_change, x=df_change.index, y='percent_change_7d', color='positive_percent_change_7d',
                 color_discrete_map={True: 'green', False: 'red'},
                 title='% Price Change over 7 days')
elif percent_timeframe == '24h':
    if sort_values == 'Yes':
        df_change = df_change.sort_values(by=['percent_change_24h'])
    fig = px.bar(df_change, x=df_change.index, y='percent_change_24h', color='positive_percent_change_24h',
                 color_discrete_map={True: 'green', False: 'red'},
                 title='% Price Change over 24 hours')
else:
    if sort_values == 'Yes':
        df_change = df_change.sort_values(by=['percent_change_1h'])
    fig = px.bar(df_change, x=df_change.index, y='percent_change_1h', color='positive_percent_change_1h',
                 color_discrete_map={True: 'green', False: 'red'},
                 title='% Price Change over 1 hour')

col3.plotly_chart(fig)

# Additional Plot: Pie chart for market cap
col3.subheader('Market Cap Distribution')
fig_pie = px.pie(df_coins, values='market_cap', names='coin_symbol', title='Market Cap Distribution of Selected Coins')
col3.plotly_chart(fig_pie)

# Additional Plot: Line chart for price trends
col3.subheader('Price Trends')
fig_line = px.line(df_coins, x='coin_symbol', y='price', title='Price Trends of Selected Coins')
col3.plotly_chart(fig_line)
