# Requirements
- Python 3.14+
- Redis 8.6+
- Eclipse Mosquitto

# Computer vision model

Using openCV and a pre-trained model to detect people in images.

Used model : Yolo8n for object detection, because it's small and fast, adatpted for raspberry pi (2 Go).

# Structure

The project is structured in four main parts:
- `raspberry_scripts`: Contains the scripts that run on the Raspberry Pi, including serial data reading, image analysis, and MQTT transmission. made to work as three separate processes to avoid blocking and data loss.
- `server_scripts`: Contains the script that runs on the server to receive MQTT messages and save them to the database.
- `esp_32_source`: Contains the source code for the ESP32 XIAO sense, that reads the data from the camera and sends it via serial.
- `arduino`: Contains the source code for the 2 Arduino that communicate via ZigBee. The sender reads from the movement detector and sends the data to the receiver that is connected to the Raspberry Pi via USB and sends the data via serial.

# Other
The `ml_image-reader` contains a jupyter notebook that was used to test the image analysis and the model, but it's not used in the final project.

`shared` contains the code that is shared between the Raspberry Pi and the server, such as the MQTT manager and the constants.

# Start commands :
```bash
python -m raspberry_scripts.serial_data_reading
python -m raspberry_scripts.image_analysis
python -m raspberry_scripts.mqtt_transmission
```

# Install redis on raspberry pi :
```bash
sudo apt install redis-server
sudo systemctl enable redis-server
sudo systemctl start redis-server
```
