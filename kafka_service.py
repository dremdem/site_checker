"""Services for the Kafka"""
import json
from typing import Callable

import kafka

import config

producer = kafka.KafkaProducer(
    bootstrap_servers=[f'{config.KAFKA_HOST}:{config.KAFKA_PORT}'],
    value_serializer=lambda m: json.dumps(m).encode('ascii'))


consumer = kafka.KafkaConsumer(
    config.KAFKA_CHECKER_TOPIC,
    bootstrap_servers=[f'{config.KAFKA_HOST}:{config.KAFKA_PORT}'],
    value_deserializer=lambda m: json.loads(m.decode('ascii'))
)


def send_message(message: dict):
    """Send message asynchronously"""
    producer.send(config.KAFKA_CHECKER_TOPIC, message)


def consume_messages(processor: Callable):
    for message in consumer:
        processor(message.value)
        print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                             message.offset, message.key,
                                             message.value))


# consume_messages()
