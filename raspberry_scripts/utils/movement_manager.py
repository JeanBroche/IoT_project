"""
Class to manage movement data by checking the movement for time 
intervals and keeping the last movement data in memory.
"""
import time
from . import constants

class MovementManager:
    """Manager for movement data."""
    def __init__(self):
        self.last_movement_time = 0

    def register_movement(self):
        """Update the movement data."""
        self.last_movement_time = time.time()

    def is_movement_valid(self):
        """Get the last movement data if it's still valid."""
        return time.time() - self.last_movement_time < constants.MOVEMENT_VALIDITY_INTERVAL
