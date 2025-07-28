import pygame
from constants import *
from gamestate import *

class UpgradeObject(pygame.sprite.Sprite):
    player = None
    containers = ()

    def __init__(self, position, upgrade_type):
        super().__init__(self.containers)
        self.upgrade_type = upgrade_type
        self.position = pygame.Vector2(position)
        self.radius = 10
        self.color = (255, 255, 100)

        self.image = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=position)

        self.velocity = pygame.Vector2(0, 0)

    def update(self, dt):
        direction = self.player.position - self.position
        if direction.length() < 120 and direction.length() > 0:
            self.velocity += direction.normalize() * 200 * dt
        
        self.position += self.velocity * dt
        self.rect.center = self.position

        if self.player.position.distance_to(self.position) < self.radius + self.player.radius:
            GameState.apply_upgrade(self.upgrade_type)
            self.kill()

    def draw(self, screen, camera_offset):
        screen_pos = self.position - camera_offset
        screen.blit(self.image, self.image.get_rect(center=screen_pos))