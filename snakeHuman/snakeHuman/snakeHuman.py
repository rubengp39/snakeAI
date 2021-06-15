
import pygame
import random
from enum import Enum
from collections import namedtuple


pygame.init()
font = pygame.font.SysFont('arial', 20)

class Direction(Enum):
	RIGHT = 1
	LEFT = 2
	UP = 3
	DOWN = 4


Point = namedtuple('Point', 'x, y')

BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0,0,255)
YELLOW = (255, 255, 0)


BLOCK_SIZE = 20
SPEED = 20

class SnakeGame:

	def __init__(self, w=720, h= 480):
		self.w = w
		self.h = h
		
		self.display = pygame.display.set_mode((self.w, self.h))
		self.clock = pygame.time.Clock()

		self.direction = Direction.RIGHT

		self.head = Point(self.w/2, self.h/2)
		self.snake = [self.head, Point(self.head.x-BLOCK_SIZE, self.head.y), Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
		self.score = 0
		self.food = None
		self._place_food()


	def _place_food(self):
		x = random.randint(0,(self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
		y = random.randint(0,(self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
		self.food = Point(x,y)
		if self.food in self.snake:
			self._place_food()


	def play_step(self):
		#input
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if self.direction == Direction.DOWN:
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_LEFT:
						self.direction = Direction.LEFT
					elif event.key == pygame.K_RIGHT:
						self.direction = Direction.RIGHT
					elif event.key == pygame.K_DOWN:
						self.direction = Direction.DOWN

			elif self.direction == Direction.UP:
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_LEFT:
						self.direction = Direction.LEFT
					elif event.key == pygame.K_RIGHT:
						self.direction = Direction.RIGHT
					elif event.key == pygame.K_UP:
						self.direction = Direction.UP
			elif self.direction == Direction.RIGHT: 
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_RIGHT:
						self.direction = Direction.RIGHT
					elif event.key == pygame.K_UP:
						self.direction = Direction.UP
					elif event.key == pygame.K_DOWN:
						self.direction = Direction.DOWN
			else: 
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_LEFT:
						self.direction = Direction.LEFT
					elif event.key == pygame.K_UP:
						self.direction = Direction.UP
					elif event.key == pygame.K_DOWN:
						self.direction = Direction.DOWN


		#movement
		self._move(self.direction)
		self.snake.insert(0, self.head)

		#gameOver
		gameOver = False
		if self._is_collision():
			gameOver = True
			return gameOver, self.score

		#food
		if self.head == self.food:
			self.score += 1
			self._place_food()
		else:
			self.snake.pop()

		#UI
		self._update_ui()
		self.clock.tick(SPEED)


		return gameOver, self.score

	
	def _is_collision(self):
		#border
		if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
			return True

		#Snake
		if self.head in self.snake[1:]:
			return True

		return False

	def _update_ui(self):
		self.display.fill(BLACK)

		for i in self.snake:
			pygame.draw.rect(self.display, BLUE, pygame.Rect(i.x, i.y, BLOCK_SIZE, BLOCK_SIZE))
			pygame.draw.rect(self.display, YELLOW, pygame.Rect(i.x+4, i.y+4, 12, 12))

		pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

		text = font.render("Score: " + str(self.score), True, WHITE)
		self.display.blit(text, [0, 0])
		pygame.display.flip()

	def _move(self, direction):
		x = self.head.x
		y = self.head.y
		if direction == Direction.RIGHT:
			x += BLOCK_SIZE
		elif direction == Direction.LEFT:
			x -= BLOCK_SIZE
		elif direction == Direction.DOWN:
			y += BLOCK_SIZE
		elif direction == Direction.UP:
			y -= BLOCK_SIZE

		self.head = Point(x, y)



		#main

if __name__ == '__main__':
    game = SnakeGame()
    
    # game loop
    while True:
        game_over, score = game.play_step()
        
        if game_over == True:
            break
        
    print('Final Score', score)
        
        
    pygame.quit()