"""
Script to take analysis results from a Redis queue and transmit them with MQTT.
Sends the average number of people and the average 
confidence of the detections every 10 analysis results.
"""
import uuid
from raspberry_scripts.utils.redis_manager import RedisErrorsQueueManager
from shared import constants
from shared.mqtt_manager import MQTTErrorsPublisher


def main():
    errors_r = RedisErrorsQueueManager()
    mqtt_e = MQTTErrorsPublisher(constants.MQTT_BROKER_HOST, constants.MQTT_BROKER_PORT)
    raspberry_id = hex(uuid.getnode())

    while True:
        error_code = errors_r.get_error_from_queue()
        if error_code is not None:
            mqtt_e.publish_error(error_code, raspberry_id)
            print(f"Published error code {error_code} to MQTT")
        

if __name__ == "__main__":
    main()
