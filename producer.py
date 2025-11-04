from kafka import KafkaProducer
import requests
import json
import time

API_KEY = "MEDHY35ENENL0V0H"
STOCK_SYMBOL = "AAPL"  # Apple stock
TOPIC_NAME = "stock_prices"

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def get_stock_price():
    """Fetch latest stock price from Alpha Vantage API"""
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={STOCK_SYMBOL}&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()

    if "Global Quote" in data:
        quote = data["Global Quote"]
        return {
            "symbol": quote["01. symbol"],
            "price": float(quote["05. price"]),
            "volume": int(quote["06. volume"]),
            "timestamp": quote["07. latest trading day"]
        }
    else:
        return None

while True:
    stock_data = get_stock_price()
    if stock_data:
        producer.send(TOPIC_NAME, stock_data)
        print(f"📤 Sent: {stock_data}")
    else:
        print("⚠️ Failed to fetch stock data.")
    time.sleep(10)  # fetch every 10 seconds