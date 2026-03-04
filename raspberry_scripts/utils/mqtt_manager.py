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
        self.mqtt_client.publish(topic, json.dumps(payload))


class MQTTCountManager(MQTTManager):
    """
    Class to manage MQTT transmission of the count stream from the Raspberry Pi to the server.
    """

    def publish_count(self, nb_people: int, avg_confidence: float, movement: bool):
        """
        Publish the count and average confidence to the MQTT broker.

        Args:
            nb_people (int): The number of people detected.
            avg_confidence (float): The average confidence of the detections.
            movement (bool): Whether movement was detected.
        """
        payload = {
            "nb_people": nb_people,
            "avg_confidence": avg_confidence,
            "movement": movement
        }
        self.publish_to_topic(constants.MQTT_COUNT_TOPIC, payload)
