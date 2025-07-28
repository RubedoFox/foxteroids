import pygame
from circleshape import CircleShape
from constants import *

class Shot(CircleShape, pygame.sprite.Sprite):
    containers = ()
    
    def __init__(self, x, y, player):
        CircleShape.__init__(self, x, y, SHOT_RADIUS)
        pygame.sprite.Sprite.__init__(self, self.containers)

        self.player = player
        self.velocity = pygame.Vector2(0, 0)

        self.image = pygame.Surface((SHOT_RADIUS * 2, SHOT_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 255, 255), (SHOT_RADIUS, SHOT_RADIUS), SHOT_RADIUS)
        self.rect = self.image.get_rect(center=self.position)

    def update(self, dt):
        self.position += self.velocity * dt
        self.rect.center = self.position

        if self.player and self.position.distance_to(self.player.position) > SHOT_MAX_DIST:
            self.kill()

    def draw(self, screen, camera_offset):
        screen_pos = self.position - camera_offset
        screen.blit(self.image, self.image.get_rect(center=screen_pos))
