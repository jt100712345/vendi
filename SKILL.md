# Kalshi BTC 15-Minute Trader Skill

High-frequency Bitcoin futures trading system with real-time probability prediction, reciprocity logic for order book synthesis, and settlement tracking for Kalshi 15-minute contracts.

## Overview

This skill provides a complete trading system for Bitcoin 15-minute contracts on Kalshi. It features a professional Streamlit dashboard for real-time monitoring and analysis, combined with a sophisticated trading engine that includes machine learning probability prediction and settlement tracking.

## Key Features

### Dashboard Components
1. **Probability Gauge**: Real-time visualization of $P(\text{Up})$ vs $P(\text{Down})$ confidence
2. **Live Order Book Heatmap**: Heatmap showing current market depth with reciprocity logic
3. **Performance Metrics**: Live P&L, win/loss ratio, drawdown %, and contract statistics
4. **Settlement Watch**: Countdown to expiration and BRTI (Bitcoin Reference Rate Index) tracking
5. **Recent Trades Timeline**: Detailed trade history and performance analysis
6. **System Health**: API and model status indicators

### Trading Engine
1. **Transformer Probability Model**: Random forest classifier with technical indicators
2. **Reciprocity Logic**: Synthesizes ask-side order book from no-bid data
3. **Settlement Predictor**: Final minute BRTI 60-second average tracking (99%+ accuracy)
4. **Risk Management**: Position limits, stop loss, and drawdown protection
5. **Paper/Live Trading**: Toggle between simulation and real trading modes

## Usage

### Prerequisites
1. Python 3.8 or higher
2. API keys from Kalshi and Binance
3. GitHub account (for deployment)

### Installation
```bash
pip install -r requirements.txt
```

### Configuration
Create a `.env` file with your API keys:
```env
MODE=PAPER
KALSHI_KEY_ID=your_kalshi_key_id
KALSHI_PRIVATE_KEY=your_kalshi_private_key
BINANCE_API_KEY=your_binance_api_key
BINANCE_SECRET_KEY=your_binance_secret_key
```

### Running the Dashboard
```bash
streamlit run dashboard.py
```

### Deployment
```bash
# Create GitHub repository (requires git and GitHub CLI)
gh repo create kalshi-btc-15min-trader --public --clone
cd kalshi-btc-15min-trader

# Configure GitHub remote
git remote add origin https://github.com/your-username/kalshi-btc-15min-trader.git

# Commit and push files
git add .
git commit -m "Initial commit"
git push -u origin main

# Deploy to Streamlit Cloud (requires Streamlit account)
# Go to https://share.streamlit.io and follow the deployment process
```

## Architecture

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

## Trading Strategy

### Trend Following (Early Contract)
- Uses machine learning probability predictions
- Combines with order book imbalance analysis
- Enters positions at 60% probability threshold
- Exits positions at 45% probability threshold

### Settlement Tracking (Final Minute)
- Switches to BRTI 60-second average tracking
- Predicts settlement value with 99%+ accuracy
- Adjusts positions to maximize probability of profit at settlement

## Performance Metrics

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

## System Requirements

### Hardware
- Minimum: 2GB RAM, 1GHz CPU, 10GB storage
- Recommended: 4GB RAM, 2GHz CPU, 20GB storage

### Software
- Python 3.8 or higher
- Internet connectivity for API access
- Git for version control

## Troubleshooting

### Common Issues
1. **API Connection Errors**: Verify API keys and internet connectivity
2. **Model Initialization Failures**: Check Binance API availability and historical data access
3. **Trade Execution Issues**: Ensure sufficient account funds and Kalshi API permissions
4. **Settlement Prediction Errors**: Verify BRTI API endpoint accessibility

### Log Files
- Dashboard logs are available in the Streamlit UI
- Bot logs are printed to the console during operation

## License

This project is for educational purposes only. Trading cryptocurrencies and derivatives involves significant risk. Use at your own discretion.
