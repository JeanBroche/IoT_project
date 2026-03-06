"""
Class to manage database interactions.
"""

from influxdb_client_3 import InfluxDBClient3, Point, WritePrecision

from shared.constants import INFLUXDB_URL, INFLUXDB_TOKEN, INFLUXDB_ORG, INFLUXDB_DATABASE


class DBManager:
    """
    Class to manage database interactions.
    """

    def __init__(self):
        self.client = InfluxDBClient3(
            host=INFLUXDB_URL,
            token=INFLUXDB_TOKEN,
            org=INFLUXDB_ORG,
            database=INFLUXDB_DATABASE
        )
        print("Connected to InfluxDB")
        # self.save_count(15, 85.0, False, "test_id", "test_classroom2")

    def save_count(self, nb_people: int, avg_confidence: float,
                   movement: bool, raspberry_id: str, classroom_name: str):
        """
        Save the count and average confidence to the database.

        Args:
            nb_people (int): The number of people detected.
            avg_confidence (float): The average confidence of the detections.
            movement (bool): Whether movement was detected.
            raspberry_id (str): The ID of the Raspberry Pi.
            classroom_name (str): The name of the classroom.
        """
        point = Point("people_count") \
            .tag("raspberry_id", raspberry_id) \
            .tag("classroom_name", classroom_name) \
            .field("nb_people", nb_people) \
            .field("avg_confidence", avg_confidence) \
            .field("movement", movement)

        self.client.write(point, write_precision=WritePrecision.S)

        print(f"Saving to database: {nb_people} people, {avg_confidence} confidence, movement: {movement}, id: {raspberry_id}, classroom: {classroom_name}")
