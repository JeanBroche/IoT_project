"""
Script to read images from a serial port and push them to a Redis queue.
"""
import time

from utils.sensors_manager import ESP32CameraManager, ArduinoXBeeManager, DeviceNotFoundException
from utils.redis_manager import RedisImagesQueueManager

MAX_QUEUE_SIZE = 10

def main():
    r = RedisImagesQueueManager(host='localhost', port=6379, db=0)

    while True:
        error = False
        try:
            camera_manager = ESP32CameraManager()
        except DeviceNotFoundException:
            print("ESP not found")
            error = True
            time.sleep(5)
        if not error:
            break
    
    while True:
        error = False
        try:
            xbee_manager = ArduinoXBeeManager()
        except DeviceNotFoundException:
            print("Arduino not found")
            error = True
            time.sleep(5)
        if not error:
            break

    while True:
        size, image_data = camera_manager.get_image_from_serial()

        movement_data = xbee_manager.get_movement_from_serial()

        print(movement_data)

        r.push_image_to_queue(size, image_data, movement_data)

if __name__ == "__main__":
    main()
