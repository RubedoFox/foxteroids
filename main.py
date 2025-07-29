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
import random


def main():
    while True:
        should_quit = run_game()
        if should_quit:
            break

def run_game():
    paused = False
    selected_option = 0

    pygame.init()
    pygame.font.init()
    big_font = pygame.font.SysFont(None, 100)
    small_font = pygame.font.SysFont(None, 36)

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    game_stats = GameStats()

    width, height = screen.get_width(), screen.get_height()

    game_time = 0.0

    upgrade_asteroid_timer = 5.0
    upgrade_asteroid_spawned = False

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    upgrades = pygame.sprite.Group()
    extra_lives = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    PowerUpObject.containers = (powerups, drawable, updatable)
    UpgradeObject.containers = (upgrades, updatable, drawable)
    AsteroidField.containers = updatable
    ExtraLifeObject.containers = (extra_lives, drawable, updatable)

    asteroid_field = AsteroidField()
    Player.containers = (updatable, drawable)

    player = Player(width / 2, height / 2)
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

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
                    selected_option = 0

                elif paused:
                    if event.key in (pygame.K_UP, pygame.K_DOWN):
                        selected_option = 1 - selected_option
                    elif event.key == pygame.K_RETURN:
                        if selected_option == 0:
                            paused = False
                        else:
                            pygame.quit()
                            exit()

        if not paused:
            if not player.is_alive:
                run_time = game_time
                show_game_over(screen, game_stats, run_time, big_font, small_font)
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

            camera_offset = (player.position - pygame.Vector2(width / 2, height / 2)
                             if GameState.infinite_map_mode else pygame.Vector2(0, 0))

            for obj in drawable:
                obj.draw(screen, camera_offset)

            player.draw_lives_ui(screen)
            player.draw_powerup_ui(screen)

        else:
            run_time = game_time
            screen.fill("black")
            title = big_font.render("PAUSED", True, (255, 255, 0))
            screen.blit(title, title.get_rect(center=(width // 2, height // 5)))

            render_stats(screen, small_font, game_stats, run_time, width // 2, height // 5 + 80)

            options = ["Continue", "Exit"]
            for i, option in enumerate(options):
                color = (255, 255, 255) if i == selected_option else (100, 100, 100)
                label = small_font.render(option, True, color)
                screen.blit(label, label.get_rect(center=(width // 2, height * 4 // 5 + i * 40)))

        pygame.display.flip()
        dt = clock.tick(60) / 1000

        if not paused:
            game_time += dt
            updatable.update(dt)

        if not GameState.infinite_map_mode:
            upgrade_asteroid_timer -= dt
            if upgrade_asteroid_timer <= 0 and not upgrade_asteroid_spawned:
                from upgradeasteroid import UpgradeAsteroid
                iwasteroid = UpgradeAsteroid(side=random.choice(["left", "right"]))
                upgrade_asteroid_spawned = True
                upgrade_asteroid_timer = 0.0

        if upgrade_asteroid_spawned:
            golden_asteroids_remaining = any(
                isinstance(a, Asteroid) and getattr(a, "is_upgrade", False)
                for a in asteroids
            )
            if not golden_asteroids_remaining and not GameState.infinite_map_mode:
                upgrade_asteroid_spawned = False
                upgrade_asteroid_timer = 5.0

def render_stats(screen, font, game_stats, run_time, center_x, start_y):
    lines = []

    lines.append(font.render(f"Run Duration: {run_time:.1f} seconds", True, (255, 255, 255)))
    lines.append(font.render(f"Upgrades Acquired: {game_stats.upgrades_acquired}", True, (255, 255, 255)))
    lines.append(font.render(f"Asteroids Destroyed: {game_stats.asteroids_destroyed}", True, (255, 255, 255)))

    for p, count in game_stats.powerup_usage.items():
        lines.append(font.render(f"{p.title()} Used: {count}", True, (255, 255, 255)))

    for i, line in enumerate(lines):
        rect = line.get_rect(center=(center_x, start_y + i * 40))
        screen.blit(line, rect)

def show_game_over(screen, game_stats, run_time, big_font, small_font):
    width, height = screen.get_width(), screen.get_height()

    selected_option = 0
    options = ["Restart", "Exit"]

    game_over_text = big_font.render("GAME OVER", True, (255, 0, 0))
    game_over_rect = game_over_text.get_rect(center=(width // 2, height // 4))

    runtime_text = small_font.render(f"Run Duration: {run_time:.1f} seconds", True, (255, 255, 255))
    runtime_rect = runtime_text.get_rect(center=(width // 2, height // 4 + 60))

    upgrades_text = small_font.render(f"Upgrades Acquired: {game_stats.upgrades_acquired}", True, (255, 255, 255))
    upgrades_rect = upgrades_text.get_rect(center=(width // 2, height // 4 + 100))

    asteroids_text = small_font.render(f"Asteroids Destroyed: {game_stats.asteroids_destroyed}", True, (255, 255, 255))
    asteroids_rect = asteroids_text.get_rect(center=(width // 2, height // 4 + 140))

    usage_lines = []
    y_offset = height // 4 + 180
    for p, count in game_stats.powerup_usage.items():
        usage_lines.append(small_font.render(f"{p.title()} Used: {count}", True, (255, 255, 255)))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    selected_option = 1 - selected_option
                if event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        return
                    else:
                        pygame.quit()
                        exit()

        screen.fill("black")
        screen.blit(game_over_text, game_over_rect)
        screen.blit(runtime_text, runtime_rect)
        screen.blit(upgrades_text, upgrades_rect)
        screen.blit(asteroids_text, asteroids_rect)

        for i, line in enumerate(usage_lines):
            screen.blit(line, (width // 2 - line.get_width() // 2, y_offset + i * 30))

        for i, option in enumerate(options):
            color = (255, 255, 255) if i == selected_option else (100, 100, 100)
            label = small_font.render(option, True, color)
            rect = label.get_rect(center=(width // 2, height * 3 // 4 + i * 40))
            screen.blit(label, rect)

        pygame.display.flip()
        pygame.time.Clock().tick(30)


if __name__ == "__main__":
    main()
