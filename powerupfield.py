import pygame
import random
from powerupobject import PowerUpObject
from constants import *
from gamestate import *


class PowerUpField(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(self.containers)
        self.spawn_timer = 0
        self.spawn_interval = 1.0

        self.chunk_size = 600  # Area size per chunk
        self.generated_chunks = set()  # Track chunks we've already filled

    def update(self, dt):
        if GameState.infinite_map_mode:
            self.update_infinite()
        else:
            self.update_fixed(dt)

    def update_fixed(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0

            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            type_name = random.choice(["invulnerability", "acceleration", "multishot"])
            PowerUpObject(pygame.Vector2(x, y), type_name)

    def update_infinite(self):
        player_pos = GameState.player.position
        chunk_x = int(player_pos.x // self.chunk_size)
        chunk_y = int(player_pos.y // self.chunk_size)

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                chunk = (chunk_x + dx, chunk_y + dy)
                if chunk not in self.generated_chunks:
                    self.generated_chunks.add(chunk)
                    self.spawn_powerups_in_chunk(chunk)

    def spawn_powerups_in_chunk(self, chunk):
        chunk_x, chunk_y = chunk
        base_x = chunk_x * self.chunk_size
        base_y = chunk_y * self.chunk_size

        num = random.randint(1, 2)
        for _ in range(num):
            x = base_x + random.randint(0, self.chunk_size)
            y = base_y + random.randint(0, self.chunk_size)

            type_name = random.choice(["invulnerability", "acceleration", "multishot"])
            PowerUpObject(pygame.Vector2(x, y), type_name)