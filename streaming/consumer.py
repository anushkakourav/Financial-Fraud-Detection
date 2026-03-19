# streaming/consumer.py

import json
from kafka import KafkaConsumer

from src.config import KAFKA_BROKER, KAFKA_TOPIC
from src.predict import predict_transaction
from src.database import create_table, insert_transaction


# Create database table if not exists
create_table()


consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    group_id="fraud-detector-group",
    auto_offset_reset="earliest",
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
)


def process_message(message):
    """Extract transaction from Kafka message"""
    return message.value


def start_consumer():

    print("🔥 Kafka Consumer Running...")
    print("📡 Listening for transactions...\n")

    for message in consumer:

        transaction = process_message(message)

        # Run fraud detection model
        prediction, probability = predict_transaction(transaction)

        trans_id = transaction.get("trans_num", "N/A")

        if probability < 0.50:
            risk = "🟢 LOW RISK"

        elif probability < 0.75:
            risk = "🟡 MEDIUM RISK"

        elif probability < 0.90:
            risk = "🟠 HIGH RISK"

        else:
            risk = "🔴 CRITICAL FRAUD"

        print(f"{risk} | Transaction: {trans_id} | Probability: {probability:.4f}")

        # Save result to database
        insert_transaction(transaction, prediction, probability, risk)


if __name__ == "__main__":
    start_consumer()