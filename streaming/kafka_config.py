# streaming/kafka_config.py

"""
Kafka configuration used by producer and consumer.
Values are imported from the main project config.
"""

from src.config import KAFKA_BROKER, KAFKA_TOPIC

# Optional additional configs
GROUP_ID = "fraud-detection-group"
AUTO_OFFSET_RESET = "earliest"