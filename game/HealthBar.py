import pygame
from constants import *

class HealthBar():
	"""
	Клас для рівня здоров'я
	"""
	def __init__(self, x, y, health, max_health):
		"""
		Ініціалізація
		"""
		self.x = x
		self.y = y
		self.health = health
		self.max_health = max_health

	def draw(self, health):
		"""
		Відображення
		"""
		# оновлення з новим значенням здоров'я
		self.health = health
		# підрахунок відношення здоров'я
		ratio = self.health / self.max_health
		pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 154, 24))
		pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
		pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20))