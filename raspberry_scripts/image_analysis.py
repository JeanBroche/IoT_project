"""
Script to take images from a Redis queue and extract number of people with opencv.
"""
from utils.redis_manager import RedisImagesQueueManager, RedisAnalysisQueueManager
from utils.images_processor import PersonCounter, ImageUtilities
from utils import constants

def main():
    images_r = RedisImagesQueueManager()
    analysis_r = RedisAnalysisQueueManager()
    counter = PersonCounter(constants.OPENCV_MODEL_PATH)

    while True:
        _, image_data, movement = images_r.get_image_from_queue()

        image = ImageUtilities.cv2_imread_from_buffer(image_data)
        nb_people, avg_confidence = counter.count_people(image)

        print("Nombre de personnes :", nb_people)
        print("Précision moyenne :", round(avg_confidence, 3))
        print("-" * 30)

        analysis_r.push_analysis_to_queue(nb_people, avg_confidence, movement)


if __name__ == "__main__":
    main()
