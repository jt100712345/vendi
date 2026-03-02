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

Create a new repository on GitHub and add all the project files.

### 2. Streamlit Cloud Deployment (Recommended)

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository from the list
5. Set the "Main file path" to `dashboard.py`
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

1. **Probability Gauge**: Real-time $P(\text{Up})$ vs $P(\text{Down})$ probabilities from the transformer model
2. **Live Order Book**: Heatmap visualization of current order book with reciprocity logic
3. **Performance Metrics**: Live P&L, win rate, drawdown, and contract statistics
4. **Settlement Watch**: Countdown to expiration and BRTI average tracking
5. **Recent Trades**: Timeline of executed trades with details
6. **System Health**: API and model status indicators

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
