"""
Script to take analysis results from a Redis queue and transmit them with MQTT.
Sends the average number of people and the average 
confidence of the detections every 10 analysis results.
"""
from server_scripts.utils.db_manager import DBManager
from shared import constants
from shared.mqtt_manager import MQTTCountSubscriber, MQTTErrorsSubscriber


classroom_map = {
    "0xe45f01fb97c1": "Salle B03",
}

error_map = {
    constants.CAMERA_LOST_ERROR: "Camera lost",
    constants.XBEES_LOST_ERROR: "Xbees lost",
}

def main():
    db_manager = DBManager()

    def on_message_callback(client, userdata, message):
        nb_people, avg_confidence, movement, raspberry_id = MQTTCountSubscriber.parse_message(message.payload)
        classroom_name = classroom_map.get(raspberry_id, "Unknown")
        db_manager.save_count(nb_people, avg_confidence, movement, raspberry_id, classroom_name)
    
    def on_error_receive_callback(client, userdata, message):
        error_message, raspberry_id = MQTTErrorsSubscriber.parse_message(message.payload)
        error_name = error_map.get(error_message, "Unknown")
        classroom_name = classroom_map.get(raspberry_id, "Unknown")
        db_manager.save_error(error_name, raspberry_id, classroom_name)

    mqtt_c = MQTTCountSubscriber("127.0.0.1", constants.MQTT_BROKER_PORT, on_message_callback)
    mqtt_e = MQTTErrorsSubscriber("127.0.0.1", constants.MQTT_BROKER_PORT, on_error_receive_callback)
    mqtt_e.loop_start()
    mqtt_c.loop_forever()


if __name__ == "__main__":
    main()
