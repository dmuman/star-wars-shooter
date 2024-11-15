import pygame
from constants import *

class Water(pygame.sprite.Sprite):
	"""
	Клас для води
	"""
	def __init__(self, img, x, y):
		"""
		Ініціалізація
		"""
		pygame.sprite.Sprite.__init__(self)
		self.image = img
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

	def update(self, screen_scroll):
		"""
		Оновлення зображення
		"""
		self.rect.x += screen_scroll