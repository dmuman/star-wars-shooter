import pygame
from constants import *

class ItemBox(pygame.sprite.Sprite):
	"""
	Клас для коробочок, які персонаж може взяти
	"""
	def __init__(self, item_type, x, y):
		"""
		Ініціалізація
		"""
		pygame.sprite.Sprite.__init__(self)
		self.item_type = item_type
		self.image = item_boxes[self.item_type]
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))


	def update(self, screen_scroll, player):
		"""
		Оновлення зображення
		"""
		# при скролі
		self.rect.x += screen_scroll
		# перевірка, чи персонаж підняв коробочку
		if pygame.sprite.collide_rect(self, player):
			# перевірка типу коробочки
			if self.item_type == 'Health':
				player.health += 25
				if player.health > player.max_health:
					player.health = player.max_health
			elif self.item_type == 'Ammo':
				player.ammo += 15
			elif self.item_type == 'Grenade':
				player.grenades += 3
			# видаленя коробочки
			self.kill()