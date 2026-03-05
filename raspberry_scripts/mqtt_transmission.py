"""
Script to take analysis results from a Redis queue and transmit them with MQTT.
Sends the average number of people and the average 
confidence of the detections every 10 analysis results.
"""
import uuid
from raspberry_scripts.utils.redis_manager import RedisAnalysisQueueManager
from raspberry_scripts.utils.movement_manager import MovementManager
from shared import constants
from shared.mqtt_manager import MQTTCountPublisher


def main():
    analysis_r = RedisAnalysisQueueManager()
    mqtt_c = MQTTCountPublisher(constants.MQTT_BROKER_HOST, constants.MQTT_BROKER_PORT)
    movement_manager = MovementManager()
    raspberry_id = hex(uuid.getnode())

    while True:
        analysis_array = []

        while len(analysis_array) < 10:
            nb_people, avg_confidence, movement = analysis_r.get_analysis_from_queue()
            analysis_array.append((nb_people, avg_confidence))

            if movement:
                movement_manager.register_movement()

        avg_nb_people = sum([x[0] for x in analysis_array]) / len(analysis_array)
        avg_confidence = sum([x[1] for x in analysis_array]) / len(analysis_array)

        mqtt_c.publish_count(
            int(avg_nb_people),
            avg_confidence,
            movement_manager.is_movement_valid(),
            raspberry_id
        )
        print("pub")


if __name__ == "__main__":
    main()
