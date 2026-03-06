"""
File containing constants used in the project.
"""

ESP32_PID = 4097
ESP32_VID = 12346

ARDUINO_PID = 4098
ARDUINO_VID = 9025


OPENCV_MODEL_PATH = "./yolo11n.pt"


REDIS_IMAGES_QUEUE_NAME = "images"
REDIS_ANALYSIS_DATA_QUEUE_NAME = "analysis_data"


MQTT_COUNT_TOPIC = "IoT_Project/Count_Stream"
MQTT_BROKER_HOST = "localhost"
MQTT_BROKER_PORT = 1883


MOVEMENT_VALIDITY_INTERVAL = 30 * 60  # seconds (30 minutes)


INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_TOKEN = "my-token"
INFLUXDB_ORG = "my-org"
INFLUXDB_DATABASE = "iot_project_bucket"
