import streamlit as st
from news import get_news, summarize_articles
from chart import  get_chart_data

def main():
    st.set_page_config(page_title="News and Symbol Analysis", 
                       page_icon="📰",
                       layout="wide")
    
    st.title("🌍 Global News and Symbol Analysis")
    st.markdown("---")
    
    # Initialize session state variables if they don't exist
    if 'current_symbol' not in st.session_state:
        st.session_state.current_symbol = None
    if 'articles' not in st.session_state:
        st.session_state.articles = []
    if 'charts_generated' not in st.session_state:
        st.session_state.charts_generated = False
    
    # Create two columns for the layout
    col1, col2 = st.columns([1, 1])
    
    # Left column for inputs and news
    with col1:
        previous_symbol = st.session_state.current_symbol
        symbol = st.selectbox(
            "Select a symbol to analyze:",
            [
                "AUDCAD", "AUDCHF", "AUDJPY", "AUDNZD", "AUDUSD",
                "CADCHF", "CADJPY", "CHFJPY", "EURAUD", "EURCAD",
                "EURCHF", "EURGBP", "EURJPY", "EURNZD", "EURUSD",
                "GBPAUD", "GBPCAD", "GBPCHF", "GBPJPY", "GBPNZD",
                "GBPUSD", "NZDCAD", "NZDCHF", "NZDJPY", "NZDUSD",
                "USDCAD", "USDCHF", "USDJPY", "BTCUSD"
            ]
        )
        
        # Check if symbol has changed
        if symbol != previous_symbol:
            st.session_state.current_symbol = symbol
            st.session_state.articles = []
            st.session_state.charts_generated = False
        
        # Add LLM model selection with a key to ensure it's properly tracked
        llm_model = st.selectbox(
            "Select LLM Model:",
            [
                "google/gemma-3-27b-it:free",
                "qwen/qwen2.5-vl-32b-instruct:free", 
                "google/gemini-2.0-pro-exp-02-05:free",
                "mistralai/mistral-small-3.1-24b-instruct:free",
                "meta-llama/llama-3.2-11b-vision-instruct:free"
            ],
            index=0,
            key="model_selector"  # Add a key to ensure state is tracked properly
        )
        
        # Explicitly store the selected model in session state
        st.session_state.selected_model = llm_model
        
        load_charts = st.button("Load Charts")
        search_button = st.button("Search News")
    
    # Right column for chart (loads only when button is clicked)
    with col2:
        if load_charts and not st.session_state.charts_generated:
            with st.spinner('Loading charts...'):
                # Map to Chart-IMG timeframes
                timeframes = {
                    'M5': '5m',
                    'H1': '1h',
                    'D1': '1D'
                }
                
                for mt5_timeframe, chart_timeframe in timeframes.items():
                    get_chart_data(symbol, chart_timeframe)
                
                st.session_state.charts_generated = True
        elif st.session_state.charts_generated:
            st.info(f"Charts for {symbol} are already loaded. Select a different symbol to generate new charts.")
    
    # Handle news search when button is clicked
    if search_button:
        if symbol:
            try:
                with col1:
                    # Only fetch new articles if we don't already have them for this symbol
                    if not st.session_state.articles:
                        with st.spinner('Fetching news...'):
                            st.session_state.articles = get_news(symbol)
                    
                    articles = st.session_state.articles
                    if not articles:
                        st.warning("No news found for this topic.")
                    else:
                        st.success(f"Found {len(articles)} articles!")
                        
                        # Explicitly log the model being used
                        st.info(f"Selected model: {llm_model}")
                        
                        # Summarize all articles with the selected model
                        with st.spinner(f'Analyzing news with {llm_model}...'):
                            # Explicitly pass the model from session state to ensure it's the current selection
                            selected_model = st.session_state.selected_model
                            summary = summarize_articles(articles, symbol, selected_model)
                            st.markdown("### AI Summary and Trading Decision")
                            st.write(summary)
                        
                        st.markdown("### Recent News Articles")
                        for article in articles:
                            with st.expander(f"📰 {article['title']}"):
                                st.write(f"**Published:** {article.get('date', 'N/A')}")
                                st.write(f"**Source:** {article.get('source', 'N/A')}")
                                st.write(f"**Summary:** {article.get('body', 'No summary available')}")
                                st.markdown(f"[Read Full Article]({article.get('url', '#')})")
            
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please select a symbol to search for.")

if __name__ == "__main__":
    main()