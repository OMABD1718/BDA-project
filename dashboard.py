import streamlit as st
import pandas as pd
import time
from datetime import datetime

st.set_page_config(
    page_title="📈 Real-Time Stock Market Dashboard",
    page_icon="💹",
    layout="wide"
)

# --- Page Title ---
st.title("📊 Real-Time Stock Market Dashboard")
st.markdown("### Live streaming of stock prices from Kafka (powered by Alpha Vantage API)")
st.markdown("---")

# --- Layout ---
placeholder = st.empty()

# --- Styling ---
st.markdown("""
<style>
    .big-font {
        font-size: 28px !important;
        font-weight: bold;
        color: #00b4d8;
    }
    .sub-font {
        font-size: 16px;
        color: #666666;
    }
</style>
""", unsafe_allow_html=True)


# --- Live Data Loop ---
while True:
    try:
        df = pd.read_csv('stock_data.csv')

        # Ensure we only use latest 50 points for better visuals
        df = df.tail(50)

        # --- Current stats ---
        current_price = df['price'].iloc[-1]
        last_time = df['timestamp'].iloc[-1]
        avg_price = round(df['price'].mean(), 2)
        max_price = round(df['price'].max(), 2)
        min_price = round(df['price'].min(), 2)

        with placeholder.container():
            # --- Top Metrics ---
            st.markdown("### 💰 Stock Overview")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Current Price", f"${current_price:.2f}")
            col2.metric("Average Price", f"${avg_price:.2f}")
            col3.metric("High", f"${max_price:.2f}")
            col4.metric("Low", f"${min_price:.2f}")

            # --- Line Chart ---
            st.markdown("### 📉 Price Trend")
            st.line_chart(df.set_index('timestamp')['price'])

            # --- Data Table ---
            st.markdown("### 🧾 Recent Records")
            st.dataframe(df.tail(10), use_container_width=True)

            # --- Footer ---
            st.markdown("---")
            st.markdown(f"⏱️ *Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")

        time.sleep(5)

    except FileNotFoundError:
        st.warning("Waiting for stock data... Run the producer and consumer first.")
        time.sleep(5)
    except Exception as e:
        st.error(f"⚠️ Error: {e}")
        time.sleep(5)