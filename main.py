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
from gamestats import *

def main():
    while True:
        should_quit = run_game()
        if should_quit:
            break

def run_game():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    game_stats = GameStats()

    start_time = time.time()
    upgrades_acquired = 0
    asteroids_destroyed = 0
    powerup_usage = {
        "invulnerability": 0,
        "acceleration": 0,
        "multishot": 0,
    }

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
    player.game_stats = game_stats
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
            run_time = time.time() - start_time
            show_game_over(screen, game_stats, run_time)
            return False

        for asteroid in asteroids:
            if asteroid.collides_with(player):
                asteroid.kill()
                player.lose_life()

            for shot in shots:
                if asteroid.collides_with(shot):
                    shot.kill()
                    asteroid.split()
                    game_stats.increment_asteroid_destroyed()

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

def show_game_over(screen, game_stats, run_time):
    pygame.font.init()
    big_font = pygame.font.SysFont(None, 100)
    small_font = pygame.font.SysFont(None, 36)

    game_over_text = big_font.render("GAME OVER", True, (255, 0, 0))
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))

    runtime_text = small_font.render(f"Run Duration: {run_time:.1f} seconds", True, (255, 255, 255))
    runtime_rect = runtime_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 60))

    upgrades_text = small_font.render(f"Upgrades Acquired: {game_stats.upgrades_acquired}", True, (255, 255, 255))
    upgrades_rect = upgrades_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 100))

    asteroids_text = small_font.render(f"Asteroids Destroyed: {game_stats.asteroids_destroyed}", True, (255, 255, 255))
    asteroids_rect = asteroids_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 140))

    usage_lines = []
    y_offset = SCREEN_HEIGHT // 4 + 180
    for p, count in game_stats.powerup_usage.items():
        usage_lines.append(small_font.render(f"{p.title()} Used: {count}", True, (255, 255, 255)))

    prompt_text = small_font.render("Press SPACE to restart", True, (255, 255, 255))
    prompt_rect = prompt_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return

        screen.fill("black")
        screen.blit(game_over_text, game_over_rect)
        screen.blit(runtime_text, runtime_rect)
        screen.blit(upgrades_text, upgrades_rect)
        screen.blit(asteroids_text, asteroids_rect)

        for i, line in enumerate(usage_lines):
            screen.blit(line, (SCREEN_WIDTH // 2 - line.get_width() // 2, y_offset + i * 30))

        screen.blit(prompt_text, prompt_rect)
        pygame.display.flip()
        pygame.time.Clock().tick(30)


if __name__ == "__main__":
    main()