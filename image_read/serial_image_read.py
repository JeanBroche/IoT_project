import struct
import serial

# For linux
# ser = serial.Serial('/dev/serial0', 921600, timeout=5)

ser = serial.Serial('COM5', 921600, timeout=5)

i = 0

while True:
    # read size
    size_data = ser.read(4)
    if len(size_data) < 4:
        continue

    size = struct.unpack('<I', size_data)[0]

    # read image
    image_data = b''
    while len(image_data) < size:
        packet = ser.read(size - len(image_data))
        if not packet:
            break
        image_data += packet

    # Save the image to a file
    with open(f"image_{i}.jpg", "wb") as f:
        f.write(image_data)

    print("Image received :", size, "bytes")
    i += 1
    