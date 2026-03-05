"""
Class to manage database interactions.
"""

class DBManager:
    """
    Class to manage database interactions.
    """

    def __init__(self):
        pass

    def save_count(self, nb_people: int, avg_confidence: float, movement: bool, raspberry_id: str):
        """
        Save the count and average confidence to the database.

        Args:
            nb_people (int): The number of people detected.
            avg_confidence (float): The average confidence of the detections.
            movement (bool): Whether movement was detected.
            raspberry_id (str): The ID of the Raspberry Pi.
        """
        print(f"Saving to database: {nb_people} people, {avg_confidence} confidence, movement: {movement}, id: {raspberry_id}")
