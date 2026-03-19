# streaming/producer.py

import random
import uuid
from datetime import datetime
import json
import time
import pandas as pd
from kafka import KafkaProducer

from src.config import CLEANED_TEST_FILE, FINAL_TEST_FILE, KAFKA_BROKER, KAFKA_TOPIC, TARGET_COLUMN


# Load dataset (simulate live transactions)
df = pd.read_csv(CLEANED_TEST_FILE)

# Remove target column (producer should not send labels)
df = df.drop(columns=[TARGET_COLUMN])


producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)


def start_producer(delay=2):

    print("🚀 Kafka Producer Started...")

    for _ in range(200):

        # pick random transaction
        row = df.sample(1).iloc[0].to_dict()

        # Add transaction metadata
        row["trans_num"] = f"TXN_{uuid.uuid4().hex[:10]}"
        row["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        producer.send(KAFKA_TOPIC, row)
        producer.flush()

        print(f"📤 Sent Transaction {row['trans_num']}")

        delay = random.uniform(0.5, 3)
        time.sleep(delay)


if __name__ == "__main__":
    start_producer()