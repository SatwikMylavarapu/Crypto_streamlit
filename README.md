# Crypto_streamlit
This is a Crypto price projection app made using streamlit in Python. Using the API key from the crypto Market APP.

# Crypto Price App

This Streamlit app retrieves and displays cryptocurrency prices for the top 100 cryptocurrencies from **CoinMarketCap**. It allows users to view the latest prices, market caps, and price changes over different time frames. The app provides interactive visualizations for better insights into cryptocurrency trends.

## Features

- Display current prices, market caps, and volume for the top 100 cryptocurrencies.
- Visualize percentage price changes over the past 1 hour, 24 hours, and 7 days.
- Interactive bar plots for price changes.
- Pie chart for market cap distribution of selected cryptocurrencies.
- Line chart for price trends of selected cryptocurrencies.
- Option to download the displayed data as a CSV file.

## Libraries Used

- Streamlit
- Pandas
- Plotly
- Requests
- PIL

## How to Run the App Locally

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/crypto_price_app.git
   cd crypto_price_app
   ```

2. **Create and activate a virtual environment (optional but recommended):**

python3 -m venv venv
source venv/bin/activate

3. **Install the required packages:**
   
pip install -r requirements.txt

4. **Run the app:**


streamlit run Your_app.py
