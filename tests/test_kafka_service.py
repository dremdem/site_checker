"""Testing Kafka service"""

import kafka

import config
import kafka_service


def test_send_message(mocker):
    """Test the sending a message to a Kafka"""
    message = {"message": "some text"}
    mocker.patch('kafka.KafkaProducer.send')
    kafka_service.send_message(message)
    (
        kafka.
        KafkaProducer.
        send.
        assert_called_once_with(config.KAFKA_CHECKER_TOPIC, message)
    )


def test_consume_messages(mocker):
    """Test the consuming Kafka messages"""
    # TODO(Vlad): Make research how to Mock an iterator and implement this test
    assert False
