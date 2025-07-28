import pygame
import random
from asteroid import Asteroid
from constants import *
from gamestate import GameState  # To access player position

class AsteroidField(pygame.sprite.Sprite):
    edges = [
        [
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ],
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS),
        ],
    ]
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)

        self.spawn_timer = 0.0

        self.chunk_size = 600  # Area size per chunk
        self.generated_chunks = set()  # Track chunks we've already filled

    def update(self, dt):
        if GameState.infinite_map_mode:
            self.update_infinite()
        else:
            self.update_fixed(dt)
    
    def update_fixed(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer > ASTEROID_SPAWN_RATE:
            self.spawn_timer = 0

            edge = random.choice(self.edges)
            speed = random.randint(40, 100)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            kind = random.randint(1, ASTEROID_KINDS)
            radius = ASTEROID_MIN_RADIUS * kind

            self.spawn(radius, position, velocity)

    def update_infinite(self):
        player_pos = GameState.player.position
        chunk_x = int(player_pos.x // self.chunk_size)
        chunk_y = int(player_pos.y // self.chunk_size)

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                chunk = (chunk_x + dx, chunk_y + dy)
                if chunk not in self.generated_chunks:
                    self.generated_chunks.add(chunk)
                    self.spawn_asteroids_in_chunk(chunk)

    def spawn(self, radius, position, velocity):
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity

    def spawn_asteroids_in_chunk(self, chunk):
        chunk_x, chunk_y = chunk
        base_x = chunk_x * self.chunk_size
        base_y = chunk_y * self.chunk_size

        num_asteroids = random.randint(3, 6)
        for _ in range(num_asteroids):
            kind = random.randint(1, ASTEROID_KINDS)
            radius = ASTEROID_MIN_RADIUS * kind

            x = base_x + random.randint(0, self.chunk_size)
            y = base_y + random.randint(0, self.chunk_size)

            velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
            if velocity.length() == 0:
                velocity = pygame.Vector2(1, 0)
            velocity = velocity.normalize() * random.randint(40, 100)

            self.spawn(radius, pygame.Vector2(x, y), velocity)
