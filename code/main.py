import pygame
from settings import *
from levels import levels
from scene import Scene
from helpers import import_level, import_sprite_sheet

# Initialize Pygame
pygame.init()

# Main Window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()


class Main:
	def __init__(self):
		self.camera = pygame.math.Vector2(0, 0)
		self.scene = Scene(levels[1], self.camera)

	def run(self):
		self.mobile_surface = self.scene.run()
		window.blit(self.mobile_surface, (0, 0), ((self.camera.x, self.camera.y), window.get_size()))


game = Main()


# main loop
def main():
	while True:
		window.fill((20, 20, 20))
		# Event Loop
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()

		game.run()
		pygame.display.update()
		clock.tick(FPS)


if __name__ == '__main__':
	main()
