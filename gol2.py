import time
import numpy as np
import pygame


WIDTH = 1280
HEIGHT = 720
SIZE = 10

n = 2 		# order of game (number of neighbours)  default = 1
lb = 5 		# lower bound of population             default = 2
ub = 9 		# Upper bound of population             default = 3
blb = 7 	# lower bound of birth                  default = 3
bub = 8 	# Upper bound of birth                  default = 3

#COLOR_BGR = (10, 10, 10)
COLOR_BGR = (10, 10, 40)
#COLOR_GRID = (40, 40, 40)
COLOR_GRID = (30, 30, 60)
#COLOR_DIE_NEXT = (170, 170, 170)
COLOR_DIE_NEXT = COLOR_BGR
COLOR_ALIVE_NEXT = (255, 255, 255)

def update(screen, cells, size, with_progress=False):
	updated_cells = np.zeros((cells.shape[0], cells.shape[1]))

	for row, col in np.ndindex(cells.shape):
		alive = np.sum(cells[row - n:row + n+1, col - n:col + n+1]) - cells[row, col]
		color = COLOR_BGR if cells[row, col] == 0 else COLOR_ALIVE_NEXT

		if cells[row, col] == 1:
			if alive < lb or alive > ub:
				if with_progress:
					color = COLOR_DIE_NEXT
			elif lb <= alive <= ub:
				updated_cells[row, col] = 1

				if with_progress:
					color = COLOR_ALIVE_NEXT
		else:
			if blb <= alive <= bub:
				updated_cells[row, col] = 1

				if with_progress:
					color = COLOR_ALIVE_NEXT

		pygame.draw.rect(screen, color, (col * size, row * size, size - 1, size - 1))

	return updated_cells

def main():
	pygame.init()

	screen = pygame.display.set_mode((WIDTH, HEIGHT))

	pygame.display.set_caption('John Conway\'s Game of Life')

	cells = np.zeros((int(HEIGHT / SIZE), int(WIDTH / SIZE)))

	screen.fill(COLOR_GRID)

	update(screen, cells, SIZE)

	pygame.display.flip()
	pygame.display.update()

	running = False

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				return
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					running = not running
                    
				if event.key == pygame.K_r:
					cells = np.random.rand(cells.shape[0], cells.shape[1]) > 0.8

					update(screen, cells, SIZE)

					pygame.display.update()
                    
				if event.key == pygame.K_c:
					cells = np.zeros(cells.shape)

					update(screen, cells, SIZE)

					pygame.display.update()

			if pygame.mouse.get_pressed()[0]:
				pos = pygame.mouse.get_pos()

				cells[pos[1] // SIZE, pos[0] // SIZE] = 1

				update(screen, cells, SIZE)

				pygame.display.update()
               
			if pygame.mouse.get_pressed()[2]:
				pos = pygame.mouse.get_pos()

				cells[pos[1] // SIZE, pos[0] // SIZE] = 0

				update(screen, cells, SIZE)

				pygame.display.update()
                
		screen.fill(COLOR_GRID)

		if running:
			cells = update(screen, cells, SIZE, True)
			
			pygame.display.update()

		time.sleep(0.001)

if __name__ == '__main__':
	main()
