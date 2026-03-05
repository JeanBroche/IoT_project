"""
Class to manage MQTT transmission from the Raspberry Pi to the server.
"""
import json
import paho.mqtt.client as mqtt
from . import constants

class MQTTManager:
    """
    Class to manage MQTT transmission from the Raspberry Pi to the server.
    """

    def __init__(self, host: str, port: int):
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect(host, port)

    def publish_to_topic(self, topic: str, payload: dict):
        """
        Publish the payload to the MQTT broker.

        Args:
            topic (str): The topic to publish to.
            payload (dict): The payload to publish.
        """
        self.mqtt_client.publish(topic, json.dumps(payload), qos=1)


class MQTTCountPublisher(MQTTManager):
    """
    Class to manage MQTT transmission of the count stream from the Raspberry Pi to the server.
    """

    def publish_count(self, nb_people: int, avg_confidence: float, movement: bool, raspberry_id: str):
        """
        Publish the count and average confidence to the MQTT broker.

        Args:
            nb_people (int): The number of people detected.
            avg_confidence (float): The average confidence of the detections.
            movement (bool): Whether movement was detected.
            raspberry_id (str): The ID of the Raspberry Pi.
        """
        payload = {
            "nb_people": nb_people,
            "avg_confidence": avg_confidence,
            "movement": movement,
            "raspberry_id": raspberry_id
        }
        self.publish_to_topic(constants.MQTT_COUNT_TOPIC, payload)


class MQTTCountSubscriber(MQTTManager):
    """
    Class to manage MQTT subscription to the count stream from the Raspberry Pi to the server.
    """

    def __init__(self, host: str, port: int, on_message_callback):
        super().__init__(host, port)

        def on_connect(client, userdata, flags, rc):
            client.subscribe(constants.MQTT_COUNT_TOPIC)

        self.mqtt_client.on_connect = on_connect
        self.mqtt_client.on_message = on_message_callback

    def stop(self):
        """
        Stop the MQTT client loop.
        """
        self.mqtt_client.loop_stop()

    def loop_forever(self):
        """
        Loop forever to keep the MQTT client running.
        """
        self.mqtt_client.loop_forever()

    @staticmethod
    def parse_message(message):
        """
        Parse the MQTT message payload.
        Args:
            message: The MQTT message.

        Returns:
            A tuple containing the number of people, average confidence, and movement status.
        """
        message =json.loads(message.payload.decode("utf-8"))
        return message["nb_people"], message["avg_confidence"], message["movement"], message["raspberry_id"]
