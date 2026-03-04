"""
Class to manage image processing, including person counting and image utilities.
"""
from ultralytics import YOLO
import numpy as np
import cv2

class PersonCounter:
    def __init__(self, model_path,
                 conf_threshold=0.7):

        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold

    def count_people(self, image):

        results = self.model(image, conf=self.conf_threshold, verbose=False)

        boxes = results[0].boxes
        nb_personnes = 0
        confidences = []

        for box in boxes:
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])

            # Classe 0 = person (COCO)
            if class_id == 0:
                nb_personnes += 1
                confidences.append(confidence)

        moyenne_precision = np.mean(confidences) if nb_personnes > 0 else 0.0

        return nb_personnes, float(moyenne_precision)



class ImageUtilities:
    cv2_imread_from_buffer = staticmethod(lambda image_data: cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR))