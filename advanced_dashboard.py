import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import requests
import json
from streamlit_extras.stylable_container import stylable_container

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="Kalshi BTC 15-Minute Trader - Visual Command Center",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'refresh_count' not in st.session_state:
    st.session_state.refresh_count = 0
if 'last_update' not in st.session_state:
    st.session_state.last_update = datetime.now()
if 'simulated_data' not in st.session_state:
    st.session_state.simulated_data = {
        'p_up': 0.62,
        'p_down': 0.38,
        'brti_avg': 44248.32,
        'prediction': 44251.80,
        'time_remaining': 45,
        'btc_price': 44250.00,
        'price_change': 25.50
    }

# Custom CSS with modern styling
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        color: white;
    }
    
    /* Metric card styling */
    .stMetric {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }
    
    .stMetric:hover {
        background: rgba(255, 255, 255, 0.08);
        border-color: rgba(255, 255, 255, 0.2);
        transform: translateY(-2px);
    }
    
    .stMetric .metric-value {
        color: #00ff88;
        font-size: 28px;
        font-weight: 700;
    }
    
    .stMetric .metric-label {
        color: #8888ff;
        font-size: 14px;
        font-weight: 500;
    }
    
    /* Status indicators */
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 10px;
    }
    
    .status-live {
        background-color: #00ff88;
        animation: pulse 2s infinite;
        box-shadow: 0 0 10px rgba(0, 255, 136, 0.5);
    }
    
    .status-paper {
        background-color: #ffaa00;
        box-shadow: 0 0 10px rgba(255, 170, 0, 0.5);
    }
    
    @keyframes pulse {
        0% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.6; transform: scale(1.1); }
        100% { opacity: 1; transform: scale(1); }
    }
    
    /* Chart container styling */
    .chart-container {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 20px;
    }
    
    /* Header styling */
    .header-section {
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.1) 0%, rgba(136, 136, 255, 0.1) 100%);
        border-radius: 16px;
        padding: 30px;
        margin-bottom: 30px;
        border: 1px solid rgba(0, 255, 136, 0.2);
    }
    
    /* Section title styling */
    .section-title {
        color: #8888ff;
        font-size: 20px;
        font-weight: 600;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(0, 255, 136, 0.3);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(0, 255, 136, 0.5);
    }
    </style>
""", unsafe_allow_html=True)

# Header section with enhanced styling
with stylable_container(
    key="header_container",
    css_styles="""
    {
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.1) 0%, rgba(136, 136, 255, 0.1) 100%);
        border-radius: 16px;
        padding: 30px;
        margin-bottom: 30px;
        border: 1px solid rgba(0, 255, 136, 0.2);
    }
    """
):
    st.markdown("## 📈 Kalshi BTC 15-Minute Trader")
    st.markdown("### Visual Command Center - Real-time Trading Intelligence")
    
    # Status indicator with enhanced styling
    mode = os.getenv("MODE", "PAPER")
    status_color = "status-live" if mode == "LIVE" else "status-paper"
    status_text = "LIVE TRADING" if mode == "LIVE" else "PAPER TRADING"
    st.markdown(f"""
        <div style="display: flex; align-items: center; margin-top: 20px;">
            <span class="status-indicator {status_color}"></span>
            <span style="font-size: 20px; font-weight: bold;">{status_text}</span>
        </div>
    """, unsafe_allow_html=True)

# Create main layout with columns
col1, col2, col3 = st.columns([1, 1, 1], gap="large")

# 1. Probability Gauge (Transformer P(Up) vs P(Down))
with col1:
    with stylable_container(
        key="gauge_container",
        css_styles="""
        {
            background: rgba(255, 255, 255, 0.03);
            border-radius: 12px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            height: 100%;
        }
        """
    ):
        st.markdown("## 🎯 Probability Gauge")
        
        # Get data from session state for performance
        p_up = st.session_state.simulated_data['p_up']
        p_down = st.session_state.simulated_data['p_down']
        
        # Create gauge chart with enhanced styling
        with st.fragment(key="gauge_fragment"):
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = p_up * 100,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "P(Up) Probability", 'font': {'size': 20, 'color': 'white'}},
                delta = {'reference': 50, 'increasing': {'color': "#00ff88"}, 'decreasing': {'color': "#ff4444"}},
                gauge = {
                    'axis': {'range': [0, 100], 'tickwidth': 2, 'tickcolor': "white", 'nticks': 11},
                    'bar': {'color': "#00ff88" if p_up > 0.5 else "#ff4444"},
                    'bgcolor': "rgba(255, 255, 255, 0.1)",
                    'borderwidth': 2,
                    'bordercolor': "rgba(255, 255, 255, 0.2)",
                    'steps': [
                        {'range': [0, 50], 'color': "rgba(255, 68, 68, 0.3)"},
                        {'range': [50, 100], 'color': "rgba(0, 255, 136, 0.3)"}
                    ],
                    'threshold': {
                        'line': {'color': "white", 'width': 4},
                        'thickness': 0.75,
                        'value': 50
                    }
                }
            ))
            
            fig_gauge.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font={'color': 'white'},
                height=300
            )
            
            st.plotly_chart(fig_gauge, use_container_width=True)
        
        # Probability details with st.fragment
        st.markdown("### Probability Distribution")
        prob_data = pd.DataFrame({
            "Direction": ["Up", "Down"],
            "Probability": [p_up, p_down],
            "Color": ["#00ff88", "#ff4444"]
        })
        
        with st.fragment(key="prob_chart_fragment"):
            fig_prob = go.Figure(data=[go.Bar(
                x=prob_data["Direction"],
                y=prob_data["Probability"],
                marker_color=prob_data["Color"],
                text=[f"{p*100:.1f}%" for p in prob_data["Probability"]],
                textposition='auto'
            )])
            
            fig_prob.update_layout(
                yaxis=dict(range=[0, 1], tickformat='.0%'),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font={'color': 'white'},
                height=200
            )
            
            st.plotly_chart(fig_prob, use_container_width=True)

# 2. Performance Metrics
with col2:
    with stylable_container(
        key="metrics_container",
        css_styles="""
        {
            background: rgba(255, 255, 255, 0.03);
            border-radius: 12px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            height: 100%;
        }
        """
    ):
        st.markdown("## 📊 Performance Metrics")
        
        # Simulated metrics (replace with actual data)
        metrics = {
            "Live P&L": "$1,284.50",
            "Win/Loss Ratio": "1.84:1",
            "Drawdown %": "-2.3%",
            "Contracts Traded": "452",
            "Win Rate": "61.2%",
            "Avg. Profit/Trade": "$2.84"
        }
        
        # Metric cards with enhanced styling
        metric_cols = st.columns(2)
        for i, (label, value) in enumerate(metrics.items()):
            with metric_cols[i % 2]:
                st.markdown(f"""
                    <div class="stMetric">
                        <div class="metric-label">{label}</div>
                        <div class="metric-value">{value}</div>
                    </div>
                """, unsafe_allow_html=True)
        
        # Fortress Risk Status with enhanced styling
        st.markdown("### 🏰 Fortress Risk Status")
        drawdown = -2.3
        risk_level = "Low"
        risk_color = "#00ff88"
        
        if drawdown < -5:
            risk_level = "Medium"
            risk_color = "#ffaa00"
        if drawdown < -10:
            risk_level = "High"
            risk_color = "#ff4444"
        
        st.markdown(f"""
            <div style="background: rgba(255, 255, 255, 0.05); border-radius: 10px; padding: 15px; border: 1px solid {risk_color}; margin-top: 20px;">
                <div style="color: {risk_color}; font-size: 24px; font-weight: bold;">{risk_level} Risk</div>
                <div style="color: white; font-size: 14px; margin-top: 5px;">Drawdown: {drawdown}%</div>
            </div>
        """, unsafe_allow_html=True)

# 3. Live Order Book Heatmap
with col3:
    with stylable_container(
        key="orderbook_container",
        css_styles="""
        {
            background: rgba(255, 255, 255, 0.03);
            border-radius: 12px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            height: 100%;
        }
        """
    ):
        st.markdown("## 📚 Live Order Book")
        
        # Simulated order book data (replace with actual API call)
        levels = 10
        ask_prices = [44250 + i * 5 for i in range(levels)]
        bid_prices = [44245 - i * 5 for i in range(levels)]
        ask_sizes = [100 - i * 5 for i in range(levels)]
        bid_sizes = [100 - i * 5 for i in range(levels)]
        
        order_book_data = pd.DataFrame({
            "Price": ask_prices + bid_prices,
            "Size": ask_sizes + bid_sizes,
            "Type": ["Ask"] * levels + ["Bid"] * levels
        })
        
        # Create heatmap with enhanced styling
        with st.fragment(key="orderbook_fragment"):
            fig_order = go.Figure(data=go.Heatmap(
                z=order_book_data["Size"],
                x=order_book_data["Type"],
                y=order_book_data["Price"],
                colorscale="RdYlGn",
                colorbar=dict(title="Size"),
                zsmooth="best"
            ))
            
            fig_order.update_layout(
                yaxis=dict(autorange='reversed'),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font={'color': 'white'},
                height=400
            )
            
            st.plotly_chart(fig_order, use_container_width=True)
        
        # Current price with enhanced styling
        st.markdown("### Current Price")
        with st.fragment(key="price_metric_fragment"):
            st.metric(
                "BTC Price", 
                f"${st.session_state.simulated_data['btc_price']:.2f}", 
                delta=f"+{st.session_state.simulated_data['price_change']:.2f}", 
                delta_color="normal"
            )

# 4. Settlement Watch with enhanced styling
with stylable_container(
    key="settlement_container",
    css_styles="""
    {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin-top: 30px;
    }
    """
):
    st.markdown("## ⏱️ Settlement Watch")
    
    settle_cols = st.columns([1, 1, 1], gap="medium")
    
    with settle_cols[0]:
        st.markdown("### Countdown to Settlement")
        with st.fragment(key="countdown_fragment"):
            st.metric(
                "Time Remaining", 
                f"{st.session_state.simulated_data['time_remaining']}s", 
                delta="-5s", 
                delta_color="inverse"
            )
    
    with settle_cols[1]:
        st.markdown("### BRTI Running Average")
        with st.fragment(key="brti_fragment"):
            st.metric(
                "BRTI Average", 
                f"${st.session_state.simulated_data['brti_avg']:.2f}", 
                delta="+12.45", 
                delta_color="normal"
            )
    
    with settle_cols[2]:
        st.markdown("### Settlement Predictor")
        with st.fragment(key="prediction_fragment"):
            st.metric(
                "Predicted Settlement", 
                f"${st.session_state.simulated_data['prediction']:.2f}", 
                delta="+3.48", 
                delta_color="normal"
            )

# 5. Recent Trades Timeline with enhanced styling
with stylable_container(
    key="trades_container",
    css_styles="""
    {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin-top: 30px;
    }
    """
):
    st.markdown("## 📜 Recent Trades")
    
    # Simulated trade data
    trades = [
        {"time": "14:45:23", "contract": "BTC-1445", "direction": "Buy", "price": 44250, "size": 10, "pnl": "+12.50"},
        {"time": "14:44:15", "contract": "BTC-1445", "direction": "Sell", "price": 44245, "size": 8, "pnl": "-8.20"},
        {"time": "14:43:08", "contract": "BTC-1445", "direction": "Buy", "price": 44240, "size": 15, "pnl": "+24.75"},
        {"time": "14:42:10", "contract": "BTC-1445", "direction": "Sell", "price": 44235, "size": 12, "pnl": "-15.60"},
        {"time": "14:41:30", "contract": "BTC-1445", "direction": "Buy", "price": 44230, "size": 10, "pnl": "+10.50"}
    ]
    
    trade_df = pd.DataFrame(trades)
    
    with st.fragment(key="trades_fragment"):
        st.dataframe(
            trade_df.style.apply(
                lambda x: [
                    "color: #00ff88" if v == "Buy" else "color: #ff4444" if v == "Sell" else "color: white"
                    for v in x
                ] if x.name == "direction" else [
                    "color: #00ff88" if float(v.strip('+')) > 0 else "color: #ff4444"
                    for v in x
                ] if x.name == "pnl" else ["color: white" for v in x]
            ),
            use_container_width=True
        )

# 6. System Health with enhanced styling
with stylable_container(
    key="health_container",
    css_styles="""
    {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin-top: 30px;
    }
    """
):
    st.markdown("## 🔧 System Health")
    
    health_cols = st.columns(3, gap="medium")
    
    with health_cols[0]:
        st.markdown("### API Status")
        api_status = "✅ Connected"
        st.markdown(f"<div style='color: #00ff88; font-size: 20px; font-weight: bold;'>{api_status}</div>", unsafe_allow_html=True)
    
    with health_cols[1]:
        st.markdown("### Model Status")
        model_status = "✅ Active"
        st.markdown(f"<div style='color: #00ff88; font-size: 20px; font-weight: bold;'>{model_status}</div>", unsafe_allow_html=True)
    
    with health_cols[2]:
        st.markdown("### Risk Controls")
        risk_status = "✅ All Systems Green"
        st.markdown(f"<div style='color: #00ff88; font-size: 20px; font-weight: bold;'>{risk_status}</div>", unsafe_allow_html=True)

# Performance optimized refresh mechanism
with st.sidebar:
    st.markdown("### ⚡ Performance Controls")
    auto_refresh = st.checkbox("Enable Auto-refresh", value=True)
    refresh_interval = st.slider("Refresh Interval (seconds)", 1, 30, 5)
    
    if st.button("Refresh Now"):
        st.session_state.refresh_count += 1
        st.session_state.last_update = datetime.now()
    
    st.caption(f"Refresh count: {st.session_state.refresh_count}")

# Auto-refresh logic using st.session_state
if auto_refresh:
    with st.fragment(key="auto_refresh"):
        st.markdown(f"Last update: {st.session_state.last_update.strftime('%H:%M:%S.%f')[:-3]}")
        
        # Auto-refresh every N seconds
        time_since_update = (datetime.now() - st.session_state.last_update).total_seconds()
        if time_since_update >= refresh_interval:
            st.session_state.refresh_count += 1
            st.session_state.last_update = datetime.now()
            
            # Update simulated data for demonstration
            st.session_state.simulated_data['p_up'] += (0.01 if st.session_state.refresh_count % 2 == 0 else -0.01)
            st.session_state.simulated_data['p_up'] = max(0.3, min(0.7, st.session_state.simulated_data['p_up']))
            st.session_state.simulated_data['p_down'] = 1 - st.session_state.simulated_data['p_up']
            
            st.session_state.simulated_data['time_remaining'] = max(0, st.session_state.simulated_data['time_remaining'] - refresh_interval)
            if st.session_state.simulated_data['time_remaining'] <= 0:
                st.session_state.simulated_data['time_remaining'] = 900  # Reset to 15 minutes
            
            st.session_state.simulated_data['btc_price'] += (0.5 if st.session_state.refresh_count % 2 == 0 else -0.5)
            st.session_state.simulated_data['brti_avg'] += (0.3 if st.session_state.refresh_count % 2 == 0 else -0.3)
            st.session_state.simulated_data['prediction'] += (0.2 if st.session_state.refresh_count % 2 == 0 else -0.2)
            
            st.rerun()

# Performance monitoring
st.markdown("---")
with stylable_container(
    key="performance_container",
    css_styles="""
    {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin-top: 30px;
    }
    """
):
    st.markdown("## 📈 Performance Monitoring")
    st.write(f"**Session Uptime:** {st.session_state.refresh_count * refresh_interval:.1f} seconds")
    st.write(f"**Refresh Rate:** {1/refresh_interval:.2f} Hz")
    st.write(f"**Data Points Processed:** {st.session_state.refresh_count * 100}")
