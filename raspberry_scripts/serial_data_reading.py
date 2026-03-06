import time
import serial
from raspberry_scripts.utils.sensors_manager import ESP32CameraManager, ArduinoXBeeManager, DeviceNotFoundException
from raspberry_scripts.utils.redis_manager import RedisImagesQueueManager, RedisErrorsQueueManager
from shared import constants

def wait_for_device(manager_class, name, not_found_callback=None, retry_delay=5):
    """Tentatively instantiate a device manager until successful."""
    while True:
        try:
            return manager_class()
        except DeviceNotFoundException:
            print(f"{name} not found. Retrying in {retry_delay}s...")
            if not_found_callback:
                not_found_callback()
            time.sleep(retry_delay)

def main():
    r = RedisImagesQueueManager(host='localhost', port=6379, db=0)
    r_errors = RedisErrorsQueueManager(host='localhost', port=6379, db=0)

    def handle_camera_error():
        r_errors.push_error_to_queue(constants.CAMERA_LOST_ERROR)
    def handle_xbee_error():
        r_errors.push_error_to_queue(constants.XBEES_LOST_ERROR)

    camera_manager = wait_for_device(ESP32CameraManager, "ESP32 Camera", handle_camera_error)
    xbee_manager = wait_for_device(ArduinoXBeeManager, "Arduino XBee", handle_xbee_error)

    while True:
        try:
            size, image_data = camera_manager.get_image_from_serial()
            if size is None or image_data is None:
                print("Failed to read image from ESP32 Camera")
                continue
        except (serial.SerialException, OSError) as e:
            print(f"ESP32 Camera disconnected: {e}. Reconnecting...")
            camera_manager = wait_for_device(ESP32CameraManager, "ESP32 Camera", handle_camera_error)
            continue

        try:
            movement_data = xbee_manager.get_movement_from_serial()
        except (serial.SerialException, OSError) as e:
            print(f"Arduino XBee disconnected: {e}. Reconnecting...")
            xbee_manager = wait_for_device(ArduinoXBeeManager, "Arduino XBee", handle_xbee_error)
            movement_data = False
            r_errors.push_error_to_queue(constants.XBEES_LOST_ERROR)

        try:
            r.push_image_to_queue(size, image_data, movement_data)
            print("Image pushed to Redis queue")
        except Exception as e:
            print(f"Failed to push image to Redis: {e}")

        time.sleep(0.1)

if __name__ == "__main__":
    main()