"""Testing Kafka service"""
import collections

import kafka  # noqa

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

    DumbKafkaMessage = collections.namedtuple(
        'DumbKafkaMessage', [
            "value",
            "topic",
            "partition",
            "offset",
            "key",
        ]
    )

    def dumb_processor(value):
        assert value in ("qwe", "zxc", "dfg")

    mocker.patch.object(
        kafka_service.KafkaRegistry,
        'get_consumer',
        return_value=iter([
            DumbKafkaMessage("qwe", "checker", 1, 2, 1),
            DumbKafkaMessage("zxc", "checker", 1, 2, 2),
            DumbKafkaMessage("dfg", "checker", 1, 2, 3),
        ])
    )
    kafka_service.consume_messages(dumb_processor)
