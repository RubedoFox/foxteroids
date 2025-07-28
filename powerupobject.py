import pygame
import random
from powerup import *
from constants import *
from player import *

class PowerUpObject(pygame.sprite.Sprite):
    player = None
    
    def __init__(self, position, type_name):
        super().__init__(self.containers)
        
        self.type = type_name
        self.position = pygame.Vector2(position)
        self.radius = 8
        self.color = POWERUP_COLORS[type_name]
        
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=position)
        
        self.angle = 0
        self.base_image = self.image.copy()

        self.lifetime = 8.0
        self.time = 0

        self.velocity = pygame.Vector2(20, 20)
        self.attraction_range = 100
        self.attraction_strength = 300

    def draw(self, screen, camera_offset):
        screen_pos = self.position - camera_offset
        screen.blit(self.image, self.image.get_rect(center=screen_pos))

    def update(self, dt):
        self.time += dt
        if self.time >= self.lifetime:
            self.kill()

        if self.player is None:
            return

        #collision
        distance = self.position.distance_to(self.player.position)
        if distance < self.radius + self.player.radius:
            self.player.add_powerup(self.type)
            self.kill()
            return

        #magnetism
        direction = self.player.position - self.position
        distance = direction.length()

        if distance < self.attraction_range:
            if distance != 0:
                pull = direction.normalize() * self.attraction_strength * dt
                self.velocity += pull

        #rotation
        self.position += self.velocity * dt
        self.angle = (self.angle + 180 * dt) % 360
        self.image = pygame.transform.rotate(self.base_image, self.angle)
        self.rect = self.image.get_rect(center=self.position)