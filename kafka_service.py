"""
Services for the Kafka

Import as:
import kafka_service
"""
import logging

import json
from typing import Callable

import kafka # noqa

import config

logger = logging.getLogger(__name__)


producer = kafka.KafkaProducer(
    bootstrap_servers=[f'{config.KAFKA_HOST}:{config.KAFKA_PORT}'],
    value_serializer=lambda m: json.dumps(m).encode('ascii'))

consumer = kafka.KafkaConsumer(
    config.KAFKA_CHECKER_TOPIC,
    bootstrap_servers=[f'{config.KAFKA_HOST}:{config.KAFKA_PORT}'],
    value_deserializer=lambda m: json.loads(m.decode('ascii'))
)


def send_message(message: dict) -> None:
    """
    Send message asynchronously

    :param message: Dict message to send.
    """
    producer.send(config.KAFKA_CHECKER_TOPIC, message)


def consume_messages(processor: Callable) -> None:
    """
    Synchronous loop for message consuming.

    :param processor: Callable function for processing messages.
    """
    for message in consumer:
        processor(message.value)
        logger.info(
            f"{message.topic}:{message.partition}:{message.offset}: "
            f"key={message.key} value={message.value}")
