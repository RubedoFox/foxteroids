import pygame
import random
import math
from constants import *
from circleshape import CircleShape

class ExtraLifeObject(CircleShape, pygame.sprite.Sprite):
    containers = ()

    def __init__(self, position):
        position = pygame.Vector2(position)
        CircleShape.__init__(self, position.x, position.y, 12)
        pygame.sprite.Sprite.__init__(self, self.containers)

        self.base_radius = 12
        self.pulse_time = 0.0
        self.image = pygame.Surface((self.base_radius * 4, self.base_radius * 4), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=self.position)

    def update(self, dt):
        self.pulse_time += dt

        scale = 1 + 0.2 * math.sin(self.pulse_time * 4)

        self.image.fill((0, 0, 0, 0))
        center = self.image.get_width() // 2

        size = self.base_radius * scale

        points = [
            (center, center - size),                    # top
            (center - size, center + size),             # bottom-left
            (center + size, center + size)              # bottom-right
        ]

        pygame.draw.polygon(self.image, (255, 255, 255), points)

        self.rect = self.image.get_rect(center=self.position)

    def draw(self, screen, camera_offset):
        screen_pos = self.position - camera_offset
        screen.blit(self.image, self.image.get_rect(center=screen_pos))
