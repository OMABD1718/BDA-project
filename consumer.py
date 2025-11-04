from kafka import KafkaConsumer
import json
import pandas as pd
import time

consumer = KafkaConsumer(
    'stock_prices',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

data = []

print("🟢 Listening for stock data...")

for message in consumer:
    record = message.value
    print(f"📥 Received: {record}")
    data.append(record)

    if len(data) % 5 == 0:  # Save every 5 readings
        df = pd.DataFrame(data)
        df.to_csv('stock_data.csv', index=False)
        print("💾 Saved 5 records to stock_data.csv")