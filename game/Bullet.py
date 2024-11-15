import pygame
from constants import *

class Bullet(pygame.sprite.Sprite):
	"""
	Клас для кулі
	"""
	def __init__(self, x, y, direction):
		"""
		Ініціалізація
		"""
		pygame.sprite.Sprite.__init__(self)
		self.speed = 10
		self.image = bullet_img
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.direction = direction

	def update(self, screen_scroll, world, player):
		"""
		Оновлення
		"""
		# рух кулі
		self.rect.x += (self.direction * self.speed) + screen_scroll
		# перевірка, чи куля вилетіла за екран
		if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
			self.kill()
		# перевірка колізії з елементами рівня
		for tile in world.obstacle_list:
			if tile[1].colliderect(self.rect):
				self.kill()

		# перевірка колізії з персонажами
		if pygame.sprite.spritecollide(player, bullet_group, False):
			if player.alive:
				player.health -= 5
				self.kill()
		for enemy in enemy_group:
			if pygame.sprite.spritecollide(enemy, bullet_group, False):
				if enemy.alive:
					enemy.health -= 25
					self.kill()