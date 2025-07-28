import pygame
from constants import *
from gamestate import *
from circleshape import *
from player import *
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import *
from powerup import *
from powerupobject import *
from upgradeobject import *
from upgradeasteroid import *
from extralifeobject import *

def main():
    while True:
        should_quit = run_game()
        if should_quit:
            break

def run_game():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    upgrade_asteroid_timer = 5.0
    upgrade_asteroid_spawned = False

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    upgrades = pygame.sprite.Group()
    extra_lives = pygame.sprite.Group()

    for shot in shots:
        all_sprites.add(shot)
    
    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    PowerUpObject.containers = (powerups, drawable, updatable)
    UpgradeObject.containers = (upgrades, updatable, drawable)
    AsteroidField.containers = updatable
    ExtraLifeObject.containers = (extra_lives, drawable, updatable)

    asteroid_field = AsteroidField()

    Player.containers = (updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    PowerUpObject.player = player
    UpgradeObject.player = player
    GameState.player = player

    dt = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True

        updatable.update(dt)

        if not player.is_alive:
            return False

        for asteroid in asteroids:
            if asteroid.collides_with(player):
                asteroid.kill()
                player.lose_life()

            for shot in shots:
                if asteroid.collides_with(shot):
                    shot.kill()
                    asteroid.split()

        for life in extra_lives:
            if player.collides_with(life):
                if player.lives < 3:
                    player.lives += 1
                life.kill()

        screen.fill("black")

        if GameState.infinite_map_mode:
            camera_offset = player.position - pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        else:
            camera_offset = pygame.Vector2(0, 0)

        for obj in drawable:
            obj.draw(screen, camera_offset)

        player.draw_lives_ui(screen)
        player.draw_powerup_ui(screen)  

        pygame.display.flip()

        # limit the framerate to 60 FPS
        dt = clock.tick(60) / 1000

        if not GameState.infinite_map_mode:
            upgrade_asteroid_timer -= dt

            if upgrade_asteroid_timer <= 0 and not upgrade_asteroid_spawned:
                from upgradeasteroid import UpgradeAsteroid
                iwasteroid = UpgradeAsteroid(side=random.choice(["left", "right"]))
                upgrade_asteroid_spawned = True
                upgrade_asteroid_timer = 0.0

        if upgrade_asteroid_spawned:
            golden_asteroids_remaining = any(
                isinstance(a, Asteroid) and hasattr(a, "is_upgrade") and a.is_upgrade
                for a in asteroids
            )

            if not golden_asteroids_remaining and not GameState.infinite_map_mode:
                upgrade_asteroid_spawned = False
                upgrade_asteroid_timer = 5.0

if __name__ == "__main__":
    main()