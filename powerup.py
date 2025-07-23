import random
import time

class PowerUp:
    def __init__(self, name, duration=5.0):
        self.name = name
        self.duration = duration
        self.start_time = time.time()

    def is_expired(self):
        return (time.time() - self.start_time) >= self.duration

    def apply(self, player):
        if self.name == "invulnerability":
            player.has_invulnerability = True
            player.color = (255, 0, 0) #Red
        elif self.name == "acceleration":
            player.has_acceleration = True
            player.color = (0, 255, 0) #Green
        elif self.name == "multishot":
            player.has_multishot = True
            player.color = (0, 0, 255) #Blue

    def clear(self, player):
        player.has_invulnerability = False
        player.has_acceleration = False
        player.has_multishot = False
        player.color = (255, 255, 255)