"""
Class to manage the connection to Redis and push data to a queue.
"""
import json
import redis
from . import constants

class RedisQueueManager:
    """Manager for Redis connection."""
    def __init__(self, queue_name, max_queue_size = 10, host='localhost', port=6379, db=0):
        self.r = redis.Redis(host=host, port=port, db=db)
        self.queue_name = queue_name
        self.max_queue_size = max_queue_size

    def push_to_queue(self, data):
        """Push data to the Redis queue."""
        self.r.rpush(self.queue_name, data)
        # Keep only the last max_queue_size items in the list
        self.r.ltrim(self.queue_name, -self.max_queue_size, -1)

    def get_from_queue(self):
        """Get data from the Redis queue."""
        # empty the queue
        return self.r.blpop(self.queue_name)


class RedisImagesQueueManager(RedisQueueManager):
    """Manager for Redis connection to push images."""
    def __init__(self, host='localhost', port=6379, db=0):
        super().__init__(
            queue_name=constants.REDIS_IMAGES_QUEUE_NAME,
            max_queue_size=10, host=host, port=port, db=db
        )

    def push_image_to_queue(self, size, image_data, movement):
        """Push image data to the Redis queue."""
        queue_data = {
            'size': size,
            'image_data': image_data.hex(),
            'movement': movement
        }
        self.push_to_queue(json.dumps(queue_data))

    def get_image_from_queue(self):
        """Get image data from the Redis queue."""
        (_, queue_data) = self.get_from_queue()
        queue_dict = json.loads(queue_data)

        size = queue_dict['size']
        image_data = bytes.fromhex(queue_dict['image_data'])
        movement = queue_dict['movement']

        return size, image_data, movement

class RedisAnalysisQueueManager(RedisQueueManager):
    """Manager for Redis connection to push images."""
    def __init__(self, host='localhost', port=6379, db=0):
        super().__init__(
            queue_name=constants.REDIS_ANALYSIS_DATA_QUEUE_NAME,
            max_queue_size=10, host=host, port=port, db=db
        )

    def push_analysis_to_queue(self, nb_people, avg_confidence, movement):
        """Push analysis data to the Redis queue."""
        queue_data = {
            'nb_people': nb_people,
            'avg_confidence': avg_confidence,
            'movement': movement
        }
        self.push_to_queue(json.dumps(queue_data))

    def get_analysis_from_queue(self):
        """Get analysis data from the Redis queue."""
        (_, queue_data) = self.get_from_queue()
        queue_dict = json.loads(queue_data)

        nb_people = queue_dict['nb_people']
        avg_confidence = queue_dict['avg_confidence']
        movement = queue_dict['movement']

        return nb_people, avg_confidence, movement
