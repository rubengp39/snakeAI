
import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()
font = pygame.font.SysFont('arial', 20)



class Direction(Enum):
	RIGHT = 0
	LEFT = 1
	UP = 2
	DOWN = 3


Point = namedtuple('Point', 'x, y')

BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0,0,255)
YELLOW = (255, 255, 0)


BLOCK_SIZE = 20
SPEED = 20

class SnakeGameAI:

	def __init__(self, w=720, h= 480):
		self.w = w
		self.h = h
		
		self.display = pygame.display.set_mode((self.w, self.h))
		self.clock = pygame.time.Clock()

		self.reset()

	def reset(self):
		self.direction = random.choice(list(Direction))

		self.head = Point(self.w/2, self.h/2)
		self.snake = [self.head, Point(self.head.x-BLOCK_SIZE, self.head.y), Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
		self.score = 0
		self.food = None
		self._place_food()
		self.iteration = 0

	def _place_food(self):
		x = random.randint(0,(self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
		y = random.randint(0,(self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
		self.food = Point(x,y)
		if self.food in self.snake:
			self._place_food()


	def play_step(self, action):

		self.iteration += 1
		#input
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			
		#movement
		self._move(action)
		self.snake.insert(0, self.head)

		#gameOver
		reward = 0
		gameOver = False
		if self._is_collision() or self.iteration > 80*len(self.snake):
			gameOver = True
			reward = -10
			return reward, gameOver, self.score

		#food
		if self.head == self.food:
			reward += 10
			self.score += 1
			self._place_food()
		else:
			self.snake.pop()

		#UI
		self._update_ui()
		self.clock.tick(SPEED)


		return reward, gameOver, self.score

	
	def _is_collision(self, pt=None):

		if pt is None:
			pt = self.head
		#border
		if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
			return True

		#Snake
		if pt in self.snake[1:]:
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

	def _move(self, action):
		# straight, right, left

		clockWise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
		idx = clockWise.index(self.direction)

		if np.array_equal(action,[1,0,0]):
			newDir = clockWise[idx]
		elif np.array_equal(action,[0,1,0]):
			nextIdx = (idx + 1) % 4
			newDir = clockWise[nextIdx]
		else:
			nextIdx = (idx - 1) % 4
			newDir = clockWise[nextIdx]

		self.direction = newDir


		x = self.head.x
		y = self.head.y
		if self.direction == Direction.RIGHT:
			x += BLOCK_SIZE
		elif self.direction == Direction.LEFT:
			x -= BLOCK_SIZE
		elif self.direction == Direction.DOWN:
			y += BLOCK_SIZE
		elif self.direction == Direction.UP:
			y -= BLOCK_SIZE

		self.head = Point(x, y)


