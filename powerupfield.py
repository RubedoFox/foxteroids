import pygame
import random
from powerupobject import PowerUpObject
from constants import *


class PowerUpField(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(self.containers)
        self.spawn_timer = 0
        self.spawn_interval = 1.0

    def update(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            self.spawn_powerup()

    def spawn_powerup(self):
        x = random.randint(50, SCREEN_WIDTH - 50)
        y = random.randint(50, SCREEN_HEIGHT - 50)
        type_name = random.choice(["invulnerability", "acceleration", "multishot"])
        PowerUpObject((x, y), type_name)