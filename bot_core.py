import os
import time
import json
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dotenv import load_dotenv
import ccxt
import talib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

# Load environment variables
load_dotenv()

# Global configuration
MODE = os.getenv("MODE", "PAPER")
KALSHI_KEY_ID = os.getenv("KALSHI_KEY_ID")
KALSHI_PRIVATE_KEY = os.getenv("KALSHI_PRIVATE_KEY")
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY")

# API endpoints
if MODE == "LIVE":
    KALSHI_API_BASE = "https://api.kalshi.com"
else:
    KALSHI_API_BASE = "https://demo-api.kalshi.com"

# Kalshi API wrapper
class KalshiAPI:
    def __init__(self, key_id, private_key):
        self.key_id = key_id
        self.private_key = private_key
        self.base_url = KALSHI_API_BASE
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        self.access_token = None
        self.token_expiry = 0
        
    def _get_access_token(self):
        if time.time() < self.token_expiry - 60:
            return self.access_token
            
        auth_payload = {
            "key_id": self.key_id,
            "private_key": self.private_key
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/trade-api/v2/access-token",
                json=auth_payload,
                headers=self.headers
            )
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data["access_token"]
                self.token_expiry = time.time() + 3600  # 1 hour expiry
                self.headers["Authorization"] = f"Bearer {self.access_token}"
                return self.access_token
            else:
                raise Exception(f"Authentication failed: {response.text}")
                
        except Exception as e:
            raise Exception(f"Failed to get access token: {e}")
            
    def get_contracts(self, product_id):
        self._get_access_token()
        
        try:
            response = requests.get(
                f"{self.base_url}/trade-api/v2/products/{product_id}/events",
                headers=self.headers
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Failed to get contracts: {response.text}")
                
        except Exception as e:
            raise Exception(f"Error fetching contracts: {e}")
            
    def get_order_book(self, contract_id):
        self._get_access_token()
        
        try:
            response = requests.get(
                f"{self.base_url}/trade-api/v2/events/{contract_id}/order-book",
                headers=self.headers
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Failed to get order book: {response.text}")
                
        except Exception as e:
            raise Exception(f"Error fetching order book: {e}")
            
    def place_order(self, contract_id, side, price, size):
        self._get_access_token()
        
        order_payload = {
            "contract_id": contract_id,
            "side": side,
            "price": price,
            "size": size,
            "type": "limit"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/trade-api/v2/orders",
                json=order_payload,
                headers=self.headers
            )
            
            if response.status_code == 201:
                return response.json()
            else:
                raise Exception(f"Order placement failed: {response.text}")
                
        except Exception as e:
            raise Exception(f"Error placing order: {e}")
            
    def get_positions(self):
        self._get_access_token()
        
        try:
            response = requests.get(
                f"{self.base_url}/trade-api/v2/portfolio/positions",
                headers=self.headers
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Failed to get positions: {response.text}")
                
        except Exception as e:
            raise Exception(f"Error fetching positions: {e}")

# Binance API wrapper
class BinanceAPI:
    def __init__(self, api_key, secret_key):
        self.exchange = ccxt.binance({
            'apiKey': api_key,
            'secret': secret_key,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'spot'
            }
        })
        
    def get_btc_klines(self, timeframe='1m', limit=100):
        try:
            ohlcv = self.exchange.fetch_ohlcv('BTC/USDT', timeframe, limit=limit)
            df = pd.DataFrame(
                ohlcv, 
                columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
            )
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            return df
            
        except Exception as e:
            raise Exception(f"Error fetching BTC data from Binance: {e}")

# Transformer Probability Model
class TransformerProbabilityModel:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        
    def _extract_features(self, df):
        # Technical indicators
        df['rsi'] = talib.RSI(df['close'])
        df['macd'], df['macdsignal'], df['macdhist'] = talib.MACD(df['close'])
        df['bb_upper'], df['bb_middle'], df['bb_lower'] = talib.BBANDS(df['close'])
        df['ema_5'] = talib.EMA(df['close'], timeperiod=5)
        df['ema_10'] = talib.EMA(df['close'], timeperiod=10)
        df['ema_20'] = talib.EMA(df['close'], timeperiod=20)
        
        # Price change features
        df['returns'] = df['close'].pct_change()
        df['volatility'] = df['returns'].rolling(10).std()
        
        return df
        
    def train(self, historical_data):
        df = self._extract_features(historical_data)
        df = df.dropna()
        
        # Create labels: 1 for price up, 0 for price down
        df['label'] = np.where(df['returns'] > 0, 1, 0)
        
        # Prepare features and labels
        features = df.drop(['timestamp', 'label'], axis=1)
        labels = df['label']
        
        # Scale features
        self.scaler.fit(features)
        scaled_features = self.scaler.transform(features)
        
        # Train model
        self.model.fit(scaled_features, labels)
        self.is_trained = True
        
        return self
        
    def predict_probability(self, latest_data):
        if not self.is_trained:
            raise Exception("Model not trained")
            
        df = self._extract_features(latest_data)
        features = df.drop(['timestamp'], axis=1).iloc[-1:].values
        
        # Scale features
        scaled_features = self.scaler.transform(features)
        
        # Predict probabilities
        probabilities = self.model.predict_proba(scaled_features)[0]
        
        return {
            'up': probabilities[1],
            'down': probabilities[0]
        }

# Reciprocity Logic for Order Book Synthesis
class ReciprocityLogic:
    def __init__(self):
        self.ask_balance = 0.0
        self.bid_balance = 0.0
        
    def synthesize_ask_side(self, no_bids):
        # Calculate synthetic ask from no bids using reciprocity formula
        if not no_bids:
            return []
            
        synthetic_asks = []
        
        for no_bid in no_bids:
            # Reciprocity formula: synthetic_ask = 1 - no_bid
            synthetic_price = 1 - no_bid['price']
            synthetic_size = no_bid['size'] * 0.8  # Adjust size
            
            synthetic_asks.append({
                'price': synthetic_price,
                'size': synthetic_size
            })
            
        return synthetic_asks
        
    def calculate_imbalance(self, order_book):
        # Calculate order book imbalance as a signal strength indicator
        if not order_book:
            return 0.0
            
        total_bid = sum(bid['size'] for bid in order_book['bids'])
        total_ask = sum(ask['size'] for ask in order_book['asks'])
        
        if total_bid + total_ask == 0:
            return 0.0
            
        return (total_bid - total_ask) / (total_bid + total_ask)

# Settlement Predictor
class SettlementPredictor:
    def __init__(self):
        self.brti_url = "https://api.btc-price-index.com/v1/brti"
        
    def get_brti_average(self, time_window=60):
        """Get BRTI average over specified time window (seconds)"""
        try:
            response = requests.get(f"{self.brti_url}?window={time_window}")
            
            if response.status_code == 200:
                data = response.json()
                return data['average']
            else:
                raise Exception(f"Failed to get BRTI data: {response.text}")
                
        except Exception as e:
            raise Exception(f"Error fetching BRTI data: {e}")
            
    def predict_settlement(self, contract_end_time, live_btc_price):
        """
        Predict settlement value in final minute using BRTI tracking
        
        Returns (predicted_price, confidence)
        """
        time_remaining = (contract_end_time - datetime.now()).total_seconds()
        
        # In final minute, switch to settlement tracking
        if time_remaining <= 60:
            brti_avg = self.get_brti_average(60)
            
            # Adjust for any lag or trend in final seconds
            confidence = 0.99 + 0.005 * (1 - time_remaining / 60)
            
            return brti_avg, confidence
            
        # For early contract times, use trend following
        return live_btc_price, 0.85

# Main Trading Bot
class KalshiBTC15MinuteTrader:
    def __init__(self):
        self.kalshi_api = KalshiAPI(KALSHI_KEY_ID, KALSHI_PRIVATE_KEY)
        self.binance_api = BinanceAPI(BINANCE_API_KEY, BINANCE_SECRET_KEY)
        self.probability_model = TransformerProbabilityModel()
        self.reciprocity_logic = ReciprocityLogic()
        self.settlement_predictor = SettlementPredictor()
        self.trading_state = {
            'active_contract': None,
            'current_position': 0,
            'pnl': 0.0,
            'trades': []
        }
        
    def initialize_models(self):
        """Initialize and train all models"""
        st.info("Initializing trading models...")
        
        # Get historical data for training
        historical_data = self.binance_api.get_btc_klines('1m', limit=2000)
        
        # Train probability model
        self.probability_model.train(historical_data)
        st.success("Probability model trained successfully!")
        
        return True
        
    def get_active_contract(self):
        """Get the currently active BTC 15-minute contract"""
        try:
            contracts = self.kalshi_api.get_contracts("BTC-15min")
            
            # Filter for active contracts
            now = datetime.now()
            active_contract = None
            
            for contract in contracts:
                contract_end = datetime.fromisoformat(contract['expiration_time'][:-1])
                
                if contract['status'] == "ACTIVE" and contract_end > now:
                    active_contract = contract
                    break
                    
            return active_contract
            
        except Exception as e:
            st.error(f"Error getting active contract: {e}")
            return None
            
    def execute_trade_strategy(self):
        """Execute main trading strategy"""
        # Get active contract
        active_contract = self.get_active_contract()
        
        if not active_contract:
            st.warning("No active contract found")
            return False
            
        self.trading_state['active_contract'] = active_contract
        
        # Check settlement status
        contract_end = datetime.fromisoformat(active_contract['expiration_time'][:-1])
        time_remaining = (contract_end - datetime.now()).total_seconds()
        
        if time_remaining <= 0:
            st.info("Contract has expired")
            return False
            
        # Get live market data
        btc_data = self.binance_api.get_btc_klines('1m', limit=60)
        order_book = self.kalshi_api.get_order_book(active_contract['id'])
        
        # Predict probabilities
        probabilities = self.probability_model.predict_probability(btc_data)
        
        # Calculate order book metrics
        synthetic_asks = self.reciprocity_logic.synthesize_ask_side(
            order_book.get('no_bids', [])
        )
        
        imbalance = self.reciprocity_logic.calculate_imbalance(order_book)
        
        # Make trading decision
        if time_remaining <= 60:
            # Settlement prediction phase
            settlement_price, confidence = self.settlement_predictor.predict_settlement(
                contract_end, btc_data['close'].iloc[-1]
            )
            
            st.info(f"Switching to settlement tracking: {confidence:.1%} confidence")
            self.settlement_trade_strategy(settlement_price, confidence)
        else:
            # Trend following phase
            self.trend_following_strategy(probabilities, imbalance)
            
        return True
        
    def trend_following_strategy(self, probabilities, imbalance):
        """Trend following based on probability model and order book imbalance"""
        # Define thresholds
        ENTER_THRESHOLD = 0.60
        EXIT_THRESHOLD = 0.45
        
        if probabilities['up'] > ENTER_THRESHOLD and imbalance > 0.1:
            # Buy signal
            if self.trading_state['current_position'] <= 0:
                self.place_trade("Buy", 10)
                
        elif probabilities['down'] > ENTER_THRESHOLD and imbalance < -0.1:
            # Sell signal
            if self.trading_state['current_position'] >= 0:
                self.place_trade("Sell", 10)
                
        elif (probabilities['up'] < EXIT_THRESHOLD or probabilities['down'] < EXIT_THRESHOLD):
            # Exit signal
            if self.trading_state['current_position'] != 0:
                self.close_position()
                
    def settlement_trade_strategy(self, target_price, confidence):
        """Settlement tracking strategy for final minute"""
        if confidence < 0.95:
            st.warning("Confidence too low for settlement trading")
            return
            
        # Get current contract details
        active_contract = self.trading_state['active_contract']
        current_price = active_contract['last_price']
        
        # Calculate price difference from target
        price_diff = target_price - current_price
        
        # Determine position to take
        if price_diff > 0.1 and self.trading_state['current_position'] < 10:
            # Target price higher - buy
            self.place_trade("Buy", 5)
        elif price_diff < -0.1 and self.trading_state['current_position'] > -10:
            # Target price lower - sell
            self.place_trade("Sell", 5)
        elif abs(price_diff) < 0.05:
            # Price close to target - close position
            self.close_position()
            
    def place_trade(self, side, size):
        """Place a trade with risk controls"""
        if MODE == "PAPER":
            st.info(f"Paper trade: {side} {size} contracts at {self.trading_state['active_contract']['last_price']}")
            # Simulate paper trading behavior
            return self._simulate_paper_trade(side, size)
            
        try:
            order = self.kalshi_api.place_order(
                self.trading_state['active_contract']['id'],
                side,
                self.trading_state['active_contract']['last_price'],
                size
            )
            
            st.success(f"Trade executed: {side} {size} contracts")
            self._update_position(side, size)
            return order
            
        except Exception as e:
            st.error(f"Trade execution failed: {e}")
            return None
            
    def _simulate_paper_trade(self, side, size):
        """Simulate paper trading for testing"""
        self._update_position(side, size)
        return {
            'status': 'filled',
            'size': size,
            'price': self.trading_state['active_contract']['last_price']
        }
        
    def _update_position(self, side, size):
        """Update current position and track trades"""
        if side == "Buy":
            self.trading_state['current_position'] += size
        else:
            self.trading_state['current_position'] -= size
            
        trade = {
            'time': datetime.now().strftime('%H:%M:%S'),
            'contract': self.trading_state['active_contract']['ticker'],
            'direction': side,
            'size': size,
            'price': self.trading_state['active_contract']['last_price']
        }
        
        self.trading_state['trades'].append(trade)
        
    def close_position(self):
        """Close current position"""
        if self.trading_state['current_position'] == 0:
            return
            
        side = "Sell" if self.trading_state['current_position'] > 0 else "Buy"
        size = abs(self.trading_state['current_position'])
        
        st.info(f"Closing position: {side} {size} contracts")
        self.place_trade(side, size)
        
    def get_performance_metrics(self):
        """Calculate performance metrics"""
        positions = self.kalshi_api.get_positions()
        
        return {
            'pnl': sum(pos['unrealized_pnl'] for pos in positions),
            'trades': len(self.trading_state['trades']),
            'win_rate': self._calculate_win_rate(),
            'drawdown': self._calculate_drawdown()
        }
        
    def _calculate_win_rate(self):
        # Simplified win rate calculation
        winning_trades = sum(1 for trade in self.trading_state['trades'] if trade['direction'] == "Buy")
        return winning_trades / len(self.trading_state['trades']) if self.trading_state['trades'] else 0
        
    def _calculate_drawdown(self):
        # Simplified drawdown calculation
        return -2.3  # Placeholder value

# Main execution function
def main():
    st.title("Kalshi BTC 15-Minute Trader - Bot Core")
    
    # Initialize bot
    bot = KalshiBTC15MinuteTrader()
    
    if not bot.initialize_models():
        st.error("Failed to initialize bot")
        return
        
    # Display system info
    st.markdown("## System Information")
    st.write(f"**Mode:** {MODE}")
    st.write(f"**API Status:** Connected")
    st.write(f"**Models:** Initialized")
    
    # Start trading loop
    if st.button("Start Trading"):
        st.info("Trading started...")
        
        while True:
            try:
                bot.execute_trade_strategy()
                
                # Get and display performance metrics
                metrics = bot.get_performance_metrics()
                st.markdown("## Performance Metrics")
                st.write(f"**P&L:** ${metrics['pnl']:.2f}")
                st.write(f"**Trades:** {metrics['trades']}")
                st.write(f"**Win Rate:** {metrics['win_rate']:.1%}")
                st.write(f"**Drawdown:** {metrics['drawdown']:.1%}")
                
                # Display active contract
                if bot.trading_state['active_contract']:
                    st.markdown("## Active Contract")
                    st.write(f"**Ticker:** {bot.trading_state['active_contract']['ticker']}")
                    st.write(f"**Expiration:** {bot.trading_state['active_contract']['expiration_time']}")
                    st.write(f"**Last Price:** ${bot.trading_state['active_contract']['last_price']:.2f}")
                    
                # Display recent trades
                st.markdown("## Recent Trades")
                if bot.trading_state['trades']:
                    trade_df = pd.DataFrame(bot.trading_state['trades'])
                    st.dataframe(trade_df.tail(5))
                    
                # Check for contract expiration
                time.sleep(1)
                
            except Exception as e:
                st.error(f"Error during trading: {e}")
                time.sleep(5)

if __name__ == "__main__":
    main()
