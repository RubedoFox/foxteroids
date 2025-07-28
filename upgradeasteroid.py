import pygame
import random
from asteroid import Asteroid
from upgradeobject import UpgradeObject

class UpgradeAsteroid(Asteroid):
    def __init__(self, side="left"):
        y = random.uniform(0, 1) * pygame.display.get_surface().get_height()
        if side == "left":
            x = -40
            self.direction = pygame.Vector2(1, 0)
        else: 
            x = pygame.display.get_surface().get_width() + 40
            self.direction = pygame.Vector2(-1, 0)

        super().__init__(x, y, 20)

        self.is_upgrade = True
        
        self.velocity = self.direction * 300
        self.image.fill((0, 0, 0, 0))
        pygame.draw.circle(self.image, (255, 215, 0), (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=self.position)

        self.upgrade_type = "infinite_map"

    def update(self, dt):
        super().update(dt)

        screen_rect = pygame.display.get_surface().get_rect()
        if not screen_rect.inflate(100, 100).collidepoint(self.position):
            self.kill()

    def split(self):
        # Instead of splitting, spawn orb
        UpgradeObject(self.position, self.upgrade_type)
        self.kill()
        upgrade_asteroid_spawned = False