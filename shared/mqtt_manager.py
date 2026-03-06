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

        self.mqtt_client.reconnect_delay_set(min_delay=1, max_delay=120)

        self.mqtt_client.connect(host, port)

    def publish_to_topic(self, topic: str, payload: dict, qos: int = 1):
        """
        Publish the payload to the MQTT broker.

        Args:
            topic (str): The topic to publish to.
            payload (dict): The payload to publish.
        """
        return self.mqtt_client.publish(topic, json.dumps(payload), qos=qos)

    def loop_start(self):
        """
        Start the MQTT client loop.
        """
        self.mqtt_client.loop_start()
    
    def loop_forever(self):
        """
        Loop forever to keep the MQTT client running.
        """
        self.mqtt_client.loop_forever()


class MQTTCountPublisher(MQTTManager):
    """
    Class to manage MQTT transmission of the count stream from the Raspberry Pi to the server.
    """

    def __init__(self, host: str, port: int):
        super().__init__(host, port)
        self.loop_start()

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
        info = self.publish_to_topic(constants.MQTT_COUNT_TOPIC, payload)
        if info.rc != mqtt.MQTT_ERR_SUCCESS:
            print(f"Failed to publish message: {mqtt.error_string(info.rc)}")
        info.wait_for_publish()


class MQTTErrorsPublisher(MQTTManager):
    """
    Class to manage MQTT transmission of errors from the Raspberry Pi to the server.
    """

    def __init__(self, host: str, port: int):
        super().__init__(host, port)
        self.loop_start()

    def publish_error(self, error_code: int, raspberry_id: str):
        """
        Publish an error code to the MQTT broker.

        Args:
            error_code (int): The error code to publish.
            raspberry_id (str): The ID of the Raspberry Pi.
        """
        payload = {
            "error_code": error_code,
            "raspberry_id": raspberry_id
        }
        info = self.publish_to_topic(constants.MQTT_ERRORS_TOPIC, payload)
        if info.rc != mqtt.MQTT_ERR_SUCCESS:
            print(f"Failed to publish message: {mqtt.error_string(info.rc)}")
        info.wait_for_publish()


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

    @staticmethod
    def parse_message(message):
        """
        Parse the MQTT message payload.
        Args:
            message: The MQTT message.

        Returns:
            A tuple containing the number of people, average confidence, and movement status.
        """
        print('-' * 30)
        print(message)
        print('-' * 30)
        message =json.loads(message)
        return message["nb_people"], message["avg_confidence"], message["movement"], message["raspberry_id"]

class MQTTErrorsSubscriber(MQTTManager):
    """
    Class to manage MQTT subscription to errors from the Raspberry Pi to the server.
    """

    def __init__(self, host: str, port: int, on_message_callback):
        super().__init__(host, port)

        def on_connect(client, userdata, flags, rc):
            client.subscribe(constants.MQTT_ERRORS_TOPIC)

        self.mqtt_client.on_connect = on_connect
        self.mqtt_client.on_message = on_message_callback

    def stop(self):
        """
        Stop the MQTT client loop.
        """
        self.mqtt_client.loop_stop()
    
    @staticmethod
    def parse_message(message):
        """
        Parse the MQTT message payload.

        Args:
            message: The MQTT message.

        Returns:
            A tuple containing the error code and Raspberry Pi ID.
        """
        print('-' * 30)
        print(message)
        print('-' * 30)
        message =json.loads(message)
        return message["error_code"], message["raspberry_id"]
