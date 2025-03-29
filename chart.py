import requests
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import plotly.io as pio
import numpy as np
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import io
from PIL import Image
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("CHART_IMG_API_KEY", "U9PpfPfwJD7tqcBgaJXJj16Lg47gZcAB2oBiIEn1")

def get_symbol_data(symbol, timeframe, bars=100):
    """
    Fetch symbol data using chart-img API
    
    Parameters:
    symbol (str): The trading symbol to fetch
    timeframe (str): Timeframe in format like '5m', '1h', '1D'
    bars (int): Number of bars/candles to fetch
    
    Returns:
    pandas.DataFrame: DataFrame containing price data or None if error
    """
    # Create a basic dataframe structure to maintain compatibility
    df = pd.DataFrame({
        'time': pd.date_range(end=datetime.now(), periods=bars, freq=timeframe.replace('m', 'min').replace('h', 'H').replace('D', 'D')),
        'open': np.ones(bars),
        'high': np.ones(bars),
        'low': np.ones(bars),
        'close': np.ones(bars),
        'tick_volume': np.ones(bars)
    })
    
    return df

def plot_symbol_data(df, symbol, timeframe):
    """
    Plot symbol data using chart-img API
    
    Parameters:
    df (pandas.DataFrame): DataFrame containing price data (not used in this implementation)
    symbol (str): The trading symbol
    timeframe (str): Timeframe string for display purposes
    """
    # Convert timeframe to chart-img format if needed
    timeframe_mapping = {
        'M1': '1m',
        'M5': '5m',
        'M15': '15m',
        'M30': '30m',
        'H1': '1h',
        'H4': '4h',
        'D1': '1D',
        'W1': '1W'
    }
    
    chart_timeframe = timeframe_mapping.get(timeframe, timeframe)
    
    # Build the API URL
    endpoint = "https://api.chart-img.com/v1/tradingview/advanced-chart"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    
    params = {
        "symbol": symbol,
        "interval": chart_timeframe,
        "studies": ["RSI", "MACD", "MA:20", "MA:50"],
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
            st.image(filename, caption=f"{symbol} - {timeframe}", width=800)
            
        else:
            st.error(f"API request failed with status code: {response.status_code}")
            st.error(f"Response content: {response.text}")
    
    except Exception as e:
        st.error(f"Error fetching chart data: {str(e)}")

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
        "height": 800,
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