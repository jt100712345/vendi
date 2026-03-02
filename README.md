# Kalshi BTC 15-Minute Trader

A high-frequency trading system for Bitcoin 15-minute contracts on Kalshi, featuring real-time probability prediction, reciprocity logic for order book synthesis, and settlement prediction.

## System Overview

The Kalshi BTC 15-Minute Trader is a sophisticated trading system that combines:

- **Transformer Probability Model**: Machine learning model that predicts $P(\text{Up})$ vs $P(\text{Down})$ probabilities
- **Reciprocity Logic**: Synthesizes ask-side order book from no-bid data to improve market depth
- **Settlement Predictor**: In final minute of contract, switches to BRTI (Bitcoin Reference Rate Index) average tracking
- **Real-time Dashboard**: Streamlit-based visualization with probability gauge, order book heatmap, and performance metrics

## Deployment Instructions

### Prerequisites

1. Python 3.8 or higher
2. API keys from Kalshi and Coinbase
3. Heroku or Streamlit Cloud account

### 1. GitHub Repository

The code has already been created and pushed to GitHub:

**Repository URL**: https://github.com/papabrosio/kalshi-btc-15min-trader
**Branch**: main

### 2. Streamlit Cloud Deployment (Recommended)

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository from the list
5. Set the "Main file path" to either:
   - `dashboard.py` (standard version)
   - `advanced_dashboard.py` (performance-optimized version)
6. In the "Secrets" section, click "Add secret" and paste your API keys:

```env
MODE=LIVE
KALSHI_KEY_ID=f0494d09-4663-43e8-bd02-270c7feb6558
KALSHI_PRIVATE_KEY=-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEApvsg7Epj8Ucy1i+bL7+bxCXAvVIL0ThQ+4eToNorRbwbx5MG
BJMQrKaovgd+gT+tfIXGkpNlEcMXO/XAHZq5kTJQYbVHrdkbvpDlZakivZDsJCQ4
m/BRw2WlNHlSWWDLyd0RAfJxXGMKNn7t7+HG32WOdkC5RgFc6bIlaLQruzaE+uLi
1pNkFujEkqMjkch4UBUl6lXzXfMrEm0C/cMENZdvXhN5UKvt9xojXIFTeIxXROYF
s8UrK2nqazjnK853VfvaqhSfBTMnkEGISWds5V015+zGV3Fp/bzW887wmVYFOPoQ
aR9HGIeGR/R2AVLx0TE80cwt1cHCRf3FYMLxVQIDAQABAoIBAAh3Ic+o49E3HVYr
erAchC6ZBWDzuGKmesCNuofEl74Ez9m50+vGcul114cuxRSTYF24QH1s2IpifBqP
lmpJzk+Un+ucL6KaJ6RtHxwcy4SVxMr+RRpuwA5qaEo1Pl4GoL4+pV6WZnXbFYj2
vWRUa2sm8GaBWIM6jXXRkMDypWbrwzIaGXw4iOZYm4NDuDp/cTyxK2FqHvdFnTz0
9W8aG9Rbi2a5vX8KoVKtRyrlGXvLJBHtJmgrQ6RRVESZ/ysxqzyP8i+PM/eNXj04
5s6fPr43L0DQRqfQMiQEg54K/d6wvTVa0spfwhxk3QePlXoMPlAMibq/QriCTFFH
GY9rTlECgYEAzJBA8nNZpL+g1kpUzGM56/SbaArNwGdjxBFcbtcaWVR1nRH5gB0w
gkd72+B/Q1JF90ivcLYfAL5Mt7ai4/XcypSG5/+9C2gd1mTbYdhlc8mgRCgM3jA4
5c1whI1SYu/RgTgGFyJAfl1g9zJayoAT/2X5qiuSIG+33zqSPqvWaz0CgYEA0Pew
avM7M7wZ07W8/Ei9pYEBnVAaQeFxMqSWzxcDq1glbEL/pMVKT7tInHUrI+vSlCSl
0S5eywgQjiGNq5b2iMs6aLTKfspTFsv/8MYk9uB962SbLiWJf/kUX3S7gqFDzRQs
tc3R/rFxuj0KlZzGQhrdcOEYE1lmoWRN1fOdX/kCgYBWNVjZlFksAAIlLPAtroeD
c/NmVl89fZTi1ToyD/6vtNNYHXIbVrHRxZRiJmsbkPmhbAVbp7TLGGe2aIafMUca
LJvp+7HMs9UXPCvkQVEICem7r3E01fe0iO6pPfGBdnXBUj3m0+2AE5RAuPzgKDfF
Q1GDMJeFie9gaQum074qNQKBgQC/rrSxJjRkHGNEhCy67q6nplKoztWHIRkI71k2
1VGUVuLdEAgYSLEFujG88u2DocokAgnoe7SQYPFurvCZOX0jtef6K/yjmUvmWXKI
lflKTFq1FjASgHREY2KAvT9TcEIVWDA7BHVgP7ymrV+MJabm9GW0KYZAGX2/BZcw
bqspYQKBgAfIWytUirC6lrCthNiW6udZkQWWhDpGT26M0Ee0z4W5k2ltUiaC4OYM
mEXPI/e5J+Yt9uZD2RD1VOHZ+gWw52ZispytWxcDda0GfnFGgHXl4b5dJQD4o1eJ
asc3ftk7J/yqCRLDCBRLIqgdyVG+Nr6m3s7N4p0BC3aBGmCkP1Fm
-----END RSA PRIVATE KEY-----
COINBASE_CLIENT_API_KEY=fEOcjQ6qBm073cPoyKcl4i8KRKjIzYuI
COINBASE_SECRET_API_KEY=c6f3d279-20c1-4227-9253-763b84895b26
BRAVE_SEARCH_API_KEY=BSATJWSJ8Sm9eT_H0UgT_fDjiikmgCI
```

7. Click "Deploy"

### 3. Heroku Deployment

1. Install the Heroku CLI
2. Log in to Heroku: `heroku login`
3. Create a new app: `heroku create your-app-name`
4. Configure environment variables:

```bash
heroku config:set MODE=LIVE
heroku config:set KALSHI_KEY_ID=f0494d09-4663-43e8-bd02-270c7feb6558
heroku config:set KALSHI_PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEApvsg7Epj8Ucy1i+bL7+bxCXAvVIL0ThQ+4eToNorRbwbx5MG
BJMQrKaovgd+gT+tfIXGkpNlEcMXO/XAHZq5kTJQYbVHrdkbvpDlZakivZDsJCQ4
m/BRw2WlNHlSWWDLyd0RAfJxXGMKNn7t7+HG32WOdkC5RgFc6bIlaLQruzaE+uLi
1pNkFujEkqMjkch4UBUl6lXzXfMrEm0C/cMENZdvXhN5UKvt9xojXIFTeIxXROYF
s8UrK2nqazjnK853VfvaqhSfBTMnkEGISWds5V015+zGV3Fp/bzW887wmVYFOPoQ
aR9HGIeGR/R2AVLx0TE80cwt1cHCRf3FYMLxVQIDAQABAoIBAAh3Ic+o49E3HVYr
erAchC6ZBWDzuGKmesCNuofEl74Ez9m50+vGcul114cuxRSTYF24QH1s2IpifBqP
lmpJzk+Un+ucL6KaJ6RtHxwcy4SVxMr+RRpuwA5qaEo1Pl4GoL4+pV6WZnXbFYj2
vWRUa2sm8GaBWIM6jXXRkMDypWbrwzIaGXw4iOZYm4NDuDp/cTyxK2FqHvdFnTz0
9W8aG9Rbi2a5vX8KoVKtRyrlGXvLJBHtJmgrQ6RRVESZ/ysxqzyP8i+PM/eNXj04
5s6fPr43L0DQRqfQMiQEg54K/d6wvTVa0spfwhxk3QePlXoMPlAMibq/QriCTFFH
GY9rTlECgYEAzJBA8nNZpL+g1kpUzGM56/SbaArNwGdjxBFcbtcaWVR1nRH5gB0w
gkd72+B/Q1JF90ivcLYfAL5Mt7ai4/XcypSG5/+9C2gd1mTbYdhlc8mgRCgM3jA4
5c1whI1SYu/RgTgGFyJAfl1g9zJayoAT/2X5qiuSIG+33zqSPqvWaz0CgYEA0Pew
avM7M7wZ07W8/Ei9pYEBnVAaQeFxMqSWzxcDq1glbEL/pMVKT7tInHUrI+vSlCSl
0S5eywgQjiGNq5b2iMs6aLTKfspTFsv/8MYk9uB962SbLiWJf/kUX3S7gqFDzRQs
tc3R/rFxuj0KlZzGQhrdcOEYE1lmoWRN1fOdX/kCgYBWNVjZlFksAAIlLPAtroeD
c/NmVl89fZTi1ToyD/6vtNNYHXIbVrHRxZRiJmsbkPmhbAVbp7TLGGe2aIafMUca
LJvp+7HMs9UXPCvkQVEICem7r3E01fe0iO6pPfGBdnXBUj3m0+2AE5RAuPzgKDfF
Q1GDMJeFie9gaQum074qNQKBgQC/rrSxJjRkHGNEhCy67q6nplKoztWHIRkI71k2
1VGUVuLdEAgYSLEFujG88u2DocokAgnoe7SQYPFurvCZOX0jtef6K/yjmUvmWXKI
lflKTFq1FjASgHREY2KAvT9TcEIVWDA7BHVgP7ymrV+MJabm9GW0KYZAGX2/BZcw
bqspYQKBgAfIWytUirC6lrCthNiW6udZkQWWhDpGT26M0Ee0z4W5k2ltUiaC4OYM
mEXPI/e5J+Yt9uZD2RD1VOHZ+gWw52ZispytWxcDda0GfnFGgHXl4b5dJQD4o1eJ
asc3ftk7J/yqCRLDCBRLIqgdyVG+Nr6m3s7N4p0BC3aBGmCkP1Fm
-----END RSA PRIVATE KEY-----"
heroku config:set COINBASE_CLIENT_API_KEY=fEOcjQ6qBm073cPoyKcl4i8KRKjIzYuI
heroku config:set COINBASE_SECRET_API_KEY=c6f3d279-20c1-4227-9253-763b84895b26
heroku config:set BRAVE_SEARCH_API_KEY=BSATJWSJ8Sm9eT_H0UgT_fDjiikmgCI
```

5. Deploy the code: `git push heroku main`

### Environment Variables

| Variable | Description |
|----------|-------------|
| MODE | Trading mode: "PAPER" or "LIVE" (default: LIVE) |
| KALSHI_KEY_ID | Your Kalshi API key ID (provided) |
| KALSHI_PRIVATE_KEY | Your Kalshi private key (provided) |
| COINBASE_CLIENT_API_KEY | Your Coinbase API key (provided) |
| COINBASE_SECRET_API_KEY | Your Coinbase secret API key (provided) |
| BRAVE_SEARCH_API_KEY | Brave Search API key (provided) |

## Usage

### Dashboard Features

The Kalshi BTC 15-Minute Trader includes two dashboard versions:

### 1. Standard Dashboard (dashboard.py)
- **Probability Gauge**: Real-time $P(\text{Up})$ vs $P(\text{Down})$ probabilities from the transformer model
- **Live Order Book**: Heatmap visualization of current order book with reciprocity logic
- **Performance Metrics**: Live P&L, win rate, drawdown, and contract statistics
- **Settlement Watch**: Countdown to expiration and BRTI average tracking
- **Recent Trades**: Timeline of executed trades with details
- **System Health**: API and model status indicators

### 2. Advanced Dashboard (advanced_dashboard.py) - NEW!
**Features performance optimizations and modern UI enhancements:**

#### Performance Improvements:
- **st.fragment + st.session_state**: Dynamic updates without full page reload
- **Session State Management**: Persistent data across refresh cycles
- **Smart Refresh Controls**: Configurable auto-refresh with interval selection
- **Minimized Recomputation**: Only updates changed components
- **Performance Monitoring**: Real-time metrics on session uptime and refresh rate

#### Enhanced UI Features:
- **Modern Styling**: Glassmorphism effects with hover animations
- **Interactive Controls**: Sidebar for auto-refresh settings
- **Real-time Visual Feedback**: Smooth metric transitions
- **Performance Gauge**: Animated indicator with gradient effects
- **Data Visualization**: Enhanced charts with improved color schemes
- **Responsive Layout**: Optimized for different screen sizes

#### Session State Features:
- **Persistent Refresh Count**: Track how many times data has been updated
- **Auto-refresh Control**: Enable/disable automatic updates
- **Interval Selection**: Choose refresh frequency (1-30 seconds)
- **Simulated Data Updates**: Demonstrates live updates without API calls


### Trading Strategy

The system implements two primary trading strategies:

1. **Trend Following** (early contract life):
   - Uses machine learning probability predictions
   - Combines with order book imbalance analysis
   - Enters positions at 60% probability threshold
   - Exits positions at 45% probability threshold

2. **Settlement Tracking** (final minute):
   - Switches to BRTI 60-second average tracking
   - Predicts settlement value with 99%+ accuracy
   - Adjusts positions to maximize probability of profit at settlement

## System Architecture

```
┌──────────────────────┐     ┌──────────────────────┐     ┌──────────────────────┐
│ Coinbase API (OHLCV) │────▶│  Feature Extraction  │────▶│  Probability Model   │
└──────────────────────┘     └──────────────────────┘     └──────────────────────┘
           ▲                                                           ▲
           │                                                           │
┌──────────────────────┐     ┌──────────────────────┐     ┌──────────────────────┐
│  Kalshi API (Trades) │────▶│ Order Book Synthesis │────▶│ Trading Strategy     │
└──────────────────────┘     └──────────────────────┘     └──────────────────────┘
           ▲                                                           ▲
           │                                                           │
┌──────────────────────┐     ┌──────────────────────┐     ┌──────────────────────┐
│   BRTI API (Settlement)  │────▶│ Settlement Predictor  │────▶│ Position Management  │
└──────────────────────┘     └──────────────────────┘     └──────────────────────┘
```

## Technical Stack

- **Streamlit**: Dashboard and UI framework
- **Plotly**: Data visualization and charts
- **Pandas/Numpy**: Data processing and analysis
- **Scikit-learn**: Machine learning modeling
- **TA-Lib**: Technical analysis indicators
- **CCXT**: Cryptocurrency exchange integration
- **Heroku/Streamlit Cloud**: Deployment platforms

## Performance Metrics

The system continuously tracks:

- **Live P&L**: Real-time profit and loss
- **Win Rate**: Percentage of winning trades
- **Drawdown**: Maximum peak-to-trough loss
- **Contract Count**: Number of contracts traded
- **Win/Loss Ratio**: Ratio of winning to losing trades

## Risk Management

- **Position Limits**: Maximum position size per contract
- **Stop Loss**: Automatic exit if drawdown exceeds thresholds
- **Probability Thresholds**: Strict entry/exit criteria
- **Settlement Risk Control**: 99%+ confidence requirement for settlement predictions

## Development

### Local Development

1. Install dependencies: `pip install -r requirements.txt`
2. Create a `.env` file with your API keys (see `.env.example`)
3. Run the dashboard: `streamlit run dashboard.py`

### Testing

- Use `MODE=PAPER` for paper trading simulations
- Verify API connections in the System Health section
- Check performance metrics in real-time on the dashboard

## Support

For support and troubleshooting:

1. Check system health indicators on the dashboard
2. Verify API key configuration
3. Review log messages for errors
4. Ensure all dependencies are correctly installed

## License

This project is for educational purposes only. Trading cryptocurrencies and derivatives involves significant risk. Use at your own discretion.
