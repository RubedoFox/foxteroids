import pygame
import random
from constants import *
from circleshape import CircleShape
from shot import Shot
from powerup import *

#Player derived from CircleShape
class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        
        self.color = (0, 0, 0)

        self.rotation = 0
        self.fire_time = 0
        
        self.lives = 3
        self.is_alive = True

        self.has_grace = False
        self.grace = 0.0
        self.grace_time = 1.5
        
        self.powerup_durations = {
            "invulnerability": 0,
            "acceleration": 0,
            "multishot": 0,
        }

        self.has_invulnerability = False
        self.has_acceleration = False
        self.has_multishot = False
        
        self.current_powerup = None

    def lose_life(self):
        if self.has_invulnerability or self.has_grace:
            return
        
        self.lives -= 1

        if self.lives <= 0:
            self.is_alive = False
        
        else:
            self.has_grace = True
            self.grace = self.grace_time
            
            self.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    def draw(self, screen):
        pygame.draw.polygon(screen, self.color, self.triangle(), 0)
        pygame.draw.polygon(screen, "white", self.triangle(), 2)
        if self.grace > 0:
            pygame.draw.circle(screen, (255, 255, 255), self.position, self.radius + 5, 2)
        

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def update(self, dt):
        self.fire_time -= dt
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
        if keys[pygame.K_i]:
            self.has_invulnerability = True
            self.powerup_durations["invulnerability"] = 10.0
        if keys[pygame.K_o]:
            self.has_acceleration = True
            self.powerup_durations["acceleration"] = 10.0
        if keys[pygame.K_p]:
            self.has_multishot = True
            self.powerup_durations["multishot"] = 10.0

        if self.grace > 0:
            self.grace -= dt
            if self.grace <= 0:
                self.has_grace = False

        for key in self.powerup_durations:
            if self.powerup_durations[key] > 0:
                self.powerup_durations[key] -= dt
                if self.powerup_durations[key] <= 0:
                    if key == "invulnerability":
                        self.has_invulnerability = False
                    if key == "acceleration":
                        self.has_acceleration = False
                    if key == "multishot":
                        self.has_multishot = False

        self.update_powerup_color()
 
    def update_powerup_color(self):
        r, g, b = 0, 0, 0
        if self.has_invulnerability:
            r = max(r, 255)
        if self.has_acceleration:
            g = max(g, 255)
        if self.has_multishot:
            b = max(b, 255)
        self.color = (r, g, b)

    def shoot(self):
        if self.fire_time > 0:
            return
        self.fire_time = PLAYER_COOLDOWN_TIME
        shots = []
        
        if self.has_multishot:
            offsets = [20, 0, -20]
            angles = [-10, 0, 10]
            for offset, angle in zip(offsets, angles):
                pos = self.position + pygame.Vector2(offset, 0).rotate(self.rotation)
                shot = Shot(pos.x, pos.y)
                shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation + angle) * PLAYER_SHOOT_SPEED
                shots.append(shot)
        else:
            shot = Shot(self.position.x, self.position.y)
            shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
            shots.append(shot)
        

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
    
    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        if self.has_acceleration:
            self.position += forward * FAST_PLAYER_SPEED * dt
        else:
            self.position += forward * PLAYER_SPEED * dt