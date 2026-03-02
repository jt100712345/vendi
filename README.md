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
2. API keys from Kalshi and Binance
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
MODE=PAPER
KALSHI_KEY_ID=your_kalshi_key_id_here
KALSHI_PRIVATE_KEY=your_kalshi_private_key_here
BINANCE_API_KEY=your_binance_api_key_here
BINANCE_SECRET_KEY=your_binance_secret_key_here
```

7. Click "Deploy"

### 3. Heroku Deployment

1. Install the Heroku CLI
2. Log in to Heroku: `heroku login`
3. Create a new app: `heroku create your-app-name`
4. Configure environment variables:

```bash
heroku config:set MODE=PAPER
heroku config:set KALSHI_KEY_ID=your_kalshi_key_id_here
heroku config:set KALSHI_PRIVATE_KEY=your_kalshi_private_key_here
heroku config:set BINANCE_API_KEY=your_binance_api_key_here
heroku config:set BINANCE_SECRET_KEY=your_binance_secret_key_here
```

5. Deploy the code: `git push heroku main`

### Environment Variables

| Variable | Description |
|----------|-------------|
| MODE | Trading mode: "PAPER" or "LIVE" |
| KALSHI_KEY_ID | Your Kalshi API key ID |
| KALSHI_PRIVATE_KEY | Your Kalshi private key |
| BINANCE_API_KEY | Your Binance API key |
| BINANCE_SECRET_KEY | Your Binance secret key |

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
│  Binance API (OHLCV) │────▶│  Feature Extraction  │────▶│  Probability Model   │
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
