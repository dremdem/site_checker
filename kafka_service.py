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


class KafkaRegistry:
    """
    Registry for obtaining the Kafka properties

    Moved to the class in order to loose coupling between the module importing
    and the Kafka producer and consumer initialization.
    """

    __producer__ = None
    __consumer__ = None

    @classmethod
    def get_producer(cls):
        """Get producer only once"""
        if not cls.__producer__:
            cls.__producer__ = kafka.KafkaProducer(
                bootstrap_servers=[f'{config.KAFKA_HOST}:{config.KAFKA_PORT}'],
                value_serializer=lambda m: json.dumps(m).encode('ascii'),
                **config.KAFKA_CREDS
            )
        return cls.__producer__

    @classmethod
    def get_consumer(cls):
        """Get consumer only once"""
        if not cls.__consumer__:
            cls.__consumer__ = kafka.KafkaConsumer(
                config.KAFKA_CHECKER_TOPIC,
                bootstrap_servers=[f'{config.KAFKA_HOST}:{config.KAFKA_PORT}'],
                value_deserializer=lambda m: json.loads(m.decode('ascii')),
                **config.KAFKA_CREDS,
            )
        return cls.__consumer__


def send_message(message: dict) -> None:
    """
    Send message asynchronously

    :param message: Dict message to send.
    """
    KafkaRegistry.get_producer().send(config.KAFKA_CHECKER_TOPIC, message)


def consume_messages(processor: Callable) -> None:
    """
    Synchronous loop for message consuming.

    :param processor: Callable function for processing messages.
    """
    for message in KafkaRegistry.get_consumer():
        processor(message.value)
        logger.info(
            f"{message.topic}:{message.partition}:{message.offset}: "
            f"key={message.key} value={message.value}")
