"""
Class to manage the devices connected to the serial ports :
- The ESP32 camera module
- The Arduino with the XBee module, for the movement detection
"""
import struct
import serial
import serial.tools.list_ports
from shared import constants

class DeviceNotFoundException(Exception):
    """Exception raised when the device is not found."""


class SensorManager:
    """Base class for sensor managers."""
    def __init__(self, pid: int, vid: int, timeout: int = 10, baudrate: int = 9600):
        self.pid = pid
        self.vid = vid
        self.timeout = timeout
        self.baudrate = baudrate
        self.ser = None
        self.try_connection()

    def __init_serial(self, device: str = None) -> serial.Serial:
        """Initialize the serial connection."""
        if device:
            return serial.Serial(device, self.baudrate, timeout=self.timeout)
        else:
            return None

    def __find_device(self) -> str:
        """Find the serial device based on the PID and VID."""
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if port.vid == self.vid and port.pid == self.pid:
                return port.device
        return None

    def try_connection(self):
        """Retry the serial connection."""
        device = self.__find_device()
        if not device:
            raise DeviceNotFoundException("Device not found")
        self.ser = self.__init_serial(device)


class ESP32CameraManager(SensorManager):
    """Manager for the ESP32 camera module."""
    def __init__(self):
        super().__init__(
            pid=constants.ESP32_PID, vid=constants.ESP32_VID, timeout=10, baudrate=921600
        )

    def get_image_from_serial(self):
        """Read an image from the serial port."""
        # read size
        size_data = self.ser.read(4)
        if len(size_data) < 4:
            return None

        size = struct.unpack('<I', size_data)[0]

        # read image
        image_data = b''
        while len(image_data) < size:
            packet = self.ser.read(size - len(image_data))
            if not packet:
                break
            image_data += packet

        return size, image_data


class ArduinoXBeeManager(SensorManager):
    """Manager for the Arduino with XBee module. For the movement detection."""
    def __init__(self):
        super().__init__(
            pid=constants.ARDUINO_PID, vid=constants.ARDUINO_VID, timeout=1, baudrate=9600
        )
        self.ser.reset_input_buffer()

    def get_movement_from_serial(self):
        """Read latest available line from serial buffer."""
        lines = []

        while self.ser.in_waiting:
            line = self.ser.readline().decode().strip()
            lines.append(line)

        if lines:
            data = lines[-1]
            return data == "1"

        return False
