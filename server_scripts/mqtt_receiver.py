"""
Script to take analysis results from a Redis queue and transmit them with MQTT.
Sends the average number of people and the average 
confidence of the detections every 10 analysis results.
"""
from server_scripts.utils.db_manager import DBManager
from shared import constants
from shared.mqtt_manager import MQTTCountSubscriber

def main():
    db_manager = DBManager()

    def on_message_callback(client, userdata, message):
        nb_people, avg_confidence, movement, raspberry_id = MQTTCountSubscriber.parse_message(message.payload)
        db_manager.save_count(nb_people, avg_confidence, movement, raspberry_id)

    mqtt_c = MQTTCountSubscriber("127.0.0.1", constants.MQTT_BROKER_PORT, on_message_callback)
    mqtt_c.loop_forever()


if __name__ == "__main__":
    main()
