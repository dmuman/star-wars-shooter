import pygame
from constants import *

class Explosion(pygame.sprite.Sprite):
	"""
	Клас вибуху гранати
	"""
	def __init__(self, x, y, scale):
		"""
		Ініціалізація
		"""
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		for num in range(1, 6):
			img = pygame.image.load(f'{folder_path}/img/explosion/exp{num}.png').convert_alpha()
			img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
			self.images.append(img)
		self.frame_index = 0
		self.image = self.images[self.frame_index]
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.counter = 0


	def update(self, screen_scroll):
		"""
		Оновлення зображення
		"""
		# при скролі
		self.rect.x += screen_scroll

		EXPLOSION_SPEED = 4
		# оновлення анімації вибуху
		self.counter += 1

		if self.counter >= EXPLOSION_SPEED:
			self.counter = 0
			self.frame_index += 1
			# якщо анімація закінчилась - можна видалити вибух
			if self.frame_index >= len(self.images):
				self.kill()
			else:
				self.image = self.images[self.frame_index]