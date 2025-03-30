# News and Symbol Analysis App

## Setup Instructions

### API Keys and Secrets

This application uses several API keys that should be stored securely:

1. **Chart-IMG API Key** - For generating trading charts
2. **Google Gemini API Key** - For AI analysis with Google Search grounding
3. **Perplexity API Key** - For alternative news source

#### Local Development

For local development, create a `.streamlit/secrets.toml` file with the following structure:

```toml
[api_keys]
CHART_IMG_API_KEY = "your_chart_img_api_key"
GEMINI_API_KEY = "your_gemini_api_key"
PERPLEXITY_API_KEY = "your_perplexity_api_key"
```

This file should never be committed to your repository.

#### Deployment

When deploying to Streamlit Cloud:

1. Go to your app dashboard
2. Click on "⋮" (three dots) next to your app
3. Select "Settings"
4. Go to "Secrets" section
5. Paste the contents of your local `.streamlit/secrets.toml` file
6. Click "Save"

After saving your secrets, your app will be able to access them via `st.secrets`.

### Required Dependencies

Install all required dependencies with:

```bash
pip install -r requirements.txt
```

### Running the App

Run the app locally with:

```bash
streamlit run main.py
```
