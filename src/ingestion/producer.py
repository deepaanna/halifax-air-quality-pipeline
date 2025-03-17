# producer.py
from kafka import KafkaProducer
import pandas as pd
import json
import time
import yaml

# Lad config
with open("../../config/config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Kafka Producer setup
producer = KafkaProducer(
    bootstrap_servers= config["kafka"]["bootstrap_servers"],
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# Load NAPS data
df = pd.read_csv("data/raw/halifax_data.csv", skiprows=7)
halifax_data = df[df["City//Ville"] == "Halifax"].dropna(subset=["Date//Date"])

# Stream hourly data
for _, row in halifax_data.iterrows():
    date = row["Date//Date"]
    for hour in range(1, 25):
        hour_key = f"H{str(hour).zfill(2)}"
        hour_key = f"{hour_key}//{hour_key}"
        pm25 = float(row[hour_key]) if row[hour_key] != -999 else 0.0
        timestamp = f"{date} {str(hour).zfill(2)}:00:00"
        message = {
            "timestamp": timestamp,
            "station": row["NAPS ID//Identifiant SNPA"],
            "pm25": pm25,
            "latitude": row["Latitude//Latitude"],
            "longitude": row["Longitude//Longitude"]
        }
        producer.send(config["kafka"]["topic"], value=message)
        print(f"Sent: {timestamp}, PM2.5: {pm25}")
        time.sleep(0.05) # ~20 messages/sec

producer.flush()