import requests
import streamlit as st
from datetime import datetime
import os

# Get API key from Streamlit secrets
API_KEY = st.secrets["api_keys"]["CHART_IMG_API_KEY"]

def get_chart_data(symbol, timeframe, bars=100):
    """
    Fetch chart data using Chart-IMG API
    """
    endpoint = "https://api.chart-img.com/v1/tradingview/advanced-chart"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    
    params = {
        "symbol": symbol,
        "interval": timeframe,
        "studies": ["RSI", "MA:20", "MA:50"],
        "height": 600,
        "width": 800,
        "theme": "dark"
    }
    
    try:
        response = requests.get(endpoint, headers=headers, params=params)
        if response.status_code == 200:
            # Save the chart image
            filename = f'{symbol}_{timeframe}.png'
            with open(filename, 'wb') as f:
                f.write(response.content)
            
            # Display the chart - using only parameters that work in older Streamlit versions
            return st.image(filename, width=800)
        else:
            st.error(f"API request failed with status code: {response.status_code}")
            return None
            
    except Exception as e:
        st.error(f"Error fetching chart data: {str(e)}")
        return None

def main():
    st.title("Trading Chart Analysis")
    
    # Sidebar inputs
    symbol = st.sidebar.text_input("Symbol", value="BTCUSD")
    timeframe_options = {
        "1 minute": "1m",
        "5 minutes": "5m",
        "15 minutes": "15m",
        "1 hour": "1h",
        "4 hours": "4h",
        "1 day": "1D"
    }
    timeframe = st.sidebar.selectbox("Timeframe", list(timeframe_options.keys()))
    
    if st.sidebar.button("Generate Chart"):
        get_chart_data(symbol, timeframe_options[timeframe])

if __name__ == "__main__":
    main()