"""
Class to manage the connection to Redis and push data to a queue.
"""
import json
import redis

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
        return self.r.blpop(self.queue_name)


class RedisImagesQueueManager(RedisQueueManager):
    """Manager for Redis connection to push images."""
    def __init__(self, host='localhost', port=6379, db=0):
        super().__init__(queue_name='images', max_queue_size=10, host=host, port=port, db=db)

    def push_image_to_queue(self, size, image_data, mouvement):
        """Push image data to the Redis queue."""
        queue_data = {
            'size': size,
            'image_data': image_data.hex(),
            'mouvement': mouvement
        }
        self.push_to_queue(json.dumps(queue_data))

    def get_image_from_queue(self):
        """Get image data from the Redis queue."""
        (_, queue_data) = self.get_from_queue()
        queue_dict = json.loads(queue_data)

        size = queue_dict['size']
        image_data = bytes.fromhex(queue_dict['image_data'])
        mouvement = queue_dict['mouvement']

        return size, image_data, mouvement
