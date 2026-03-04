"""
Script to take images from a Redis queue and extract number of people with opencv.
"""
from utils.redis_manager import RedisImagesQueueManager
from utils.images_processor import PersonCounter, ImageUtilities
import cv2

OPENCV_MODEL_PATH = "yolo11n.pt"

def main():
    r = RedisImagesQueueManager()
    counter = PersonCounter(OPENCV_MODEL_PATH)

    i = 0

    while True:
        size, image_data, mouvement = r.get_image_from_queue()

        if not mouvement:
            continue

        image = ImageUtilities.cv2_imread_from_buffer(image_data)
        nb_people, avg_confidence = counter.count_people(image)

        # Write image to file
        cv2.imwrite(f"output_image_{i}.jpg", image)

        print("Nombre de personnes :", nb_people)
        print("Précision moyenne :", round(avg_confidence, 3))
        print("-" * 30)

        i += 1

if __name__ == "__main__":
    main()
