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

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="Kalshi BTC 15-Minute Trader - Visual Command Center",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        color: white;
    }
    .stMetric {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .stMetric .metric-value {
        color: #00ff88;
    }
    .stMetric .metric-label {
        color: #8888ff;
    }
    .gauge-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 300px;
    }
    .status-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 8px;
    }
    .status-live {
        background-color: #00ff88;
        animation: pulse 2s infinite;
    }
    .status-paper {
        background-color: #ffaa00;
    }
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("📈 Kalshi BTC 15-Minute Trader")
st.markdown("### Visual Command Center - Real-time Trading Intelligence")

# Status indicator
mode = os.getenv("MODE", "PAPER")
status_color = "status-live" if mode == "LIVE" else "status-paper"
status_text = "LIVE TRADING" if mode == "LIVE" else "PAPER TRADING"
st.markdown(f"""
    <div style="display: flex; align-items: center; margin-bottom: 20px;">
        <span class="status-indicator {status_color}"></span>
        <span style="font-size: 18px; font-weight: bold;">{status_text}</span>
    </div>
""", unsafe_allow_html=True)

# Create main layout with columns
col1, col2, col3 = st.columns([1, 1, 1])

# 1. Probability Gauge (Transformer P(Up) vs P(Down))
with col1:
    st.markdown("## 🎯 Probability Gauge")
    
    # Simulated real-time data (replace with actual API call)
    p_up = 0.62
    p_down = 0.38
    
    # Create gauge chart
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
    
    # Probability details
    st.markdown("### Probability Distribution")
    prob_data = pd.DataFrame({
        "Direction": ["Up", "Down"],
        "Probability": [p_up, p_down],
        "Color": ["#00ff88", "#ff4444"]
    })
    
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
    
    # Metric cards
    metric_cols = st.columns(2)
    for i, (label, value) in enumerate(metrics.items()):
        with metric_cols[i % 2]:
            st.markdown(f"""
                <div class="stMetric">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                </div>
            """, unsafe_allow_html=True)
    
    # Fortress Risk Status
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
        <div style="background: rgba(255, 255, 255, 0.05); border-radius: 10px; padding: 15px; border: 1px solid {risk_color};">
            <div style="color: {risk_color}; font-size: 24px; font-weight: bold;">{risk_level} Risk</div>
            <div style="color: white; font-size: 14px; margin-top: 5px;">Drawdown: {drawdown}%</div>
        </div>
    """, unsafe_allow_html=True)

# 3. Live Order Book Heatmap
with col3:
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
    
    # Create heatmap
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
    
    # Current price
    st.markdown("### Current Price")
    st.metric("BTC Price", "$44,250.00", delta="+25.50", delta_color="normal")

# 4. Settlement Watch
st.markdown("---")
st.markdown("## ⏱️ Settlement Watch")

settle_cols = st.columns([1, 1, 1])

with settle_cols[0]:
    st.markdown("### Countdown to Settlement")
    time_remaining = 45  # seconds
    st.metric("Time Remaining", f"{time_remaining}s", delta="-5s", delta_color="inverse")

with settle_cols[1]:
    st.markdown("### BRTI Running Average")
    brti_avg = 44248.32
    st.metric("BRTI Average", f"${brti_avg:.2f}", delta="+12.45", delta_color="normal")

with settle_cols[2]:
    st.markdown("### Settlement Predictor")
    prediction = 44251.80
    st.metric("Predicted Settlement", f"${prediction:.2f}", delta="+3.48", delta_color="normal")

# 5. Recent Trades Timeline
st.markdown("---")
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

# 6. System Health
st.markdown("---")
st.markdown("## 🔧 System Health")

health_cols = st.columns(3)

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

# Auto-refresh
if st.button("🔄 Refresh Data"):
    st.rerun()

st.markdown("""
    <script>
    // Auto-refresh every 5 seconds
    setTimeout(function() {
        window.location.reload();
    }, 5000);
    </script>
""", unsafe_allow_html=True)
