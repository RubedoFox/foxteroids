import pygame
import random
from circleshape import CircleShape
from constants import *

class Asteroid(CircleShape, pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        pygame.sprite.Sprite.__init__(self, self.containers)
        CircleShape.__init__(self, x, y, radius)

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(random.uniform(-100, 100), random.uniform(-100, 100))
        self.radius = radius

        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (150, 150, 150), (radius, radius), radius)
        self.rect = self.image.get_rect(center=self.position)

    def update(self, dt):
        self.position += self.velocity * dt
        self.rect.center = self.position

    def draw(self, screen, camera_offset):
        screen_pos = self.position - camera_offset
        screen.blit(self.image, self.image.get_rect(center=screen_pos))

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        
        random_angle = random.uniform(20, 50)

        vector1 = self.velocity.rotate(random_angle)
        vector2 = self.velocity.rotate(-random_angle)

        new_radius = self.radius - ASTEROID_MIN_RADIUS

        a1 = Asteroid(self.position.x, self.position.y, new_radius)
        a1.velocity = vector1 * 1.2
        
        a2 = Asteroid(self.position.x, self.position.y, new_radius)
        a2.velocity = vector2 * 1.2


