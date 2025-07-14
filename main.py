import pygame
from player import Player
from constants import *
def main():
	pygame.init()
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	clock = pygame.time.Clock()
	player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
	dt = 0

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return

		screen.fill("black")
		player.draw(screen)
		pygame.display.flip()

		#FPS limiter
		dt = clock.tick(60) / 1000.0


if __name__ == "__main__":
    main()
