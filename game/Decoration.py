import pygame
from constants import *

class Decoration(pygame.sprite.Sprite):
	"""
	Клас декорацій
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
		Оновлення на скролі
		"""
		self.rect.x += screen_scroll