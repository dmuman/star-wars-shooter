import pygame
from constants import *
from Explosion import Explosion

class Grenade(pygame.sprite.Sprite):
	"""
	Клас для гранати
	"""
	def __init__(self, x, y, direction):
		"""
		Ініціалізація
		"""
		pygame.sprite.Sprite.__init__(self)
		self.timer = 100
		self.vel_y = -11
		self.speed = 7
		self.image = grenade_img
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.direction = direction

	def update(self, screen_scroll, world, player):
		"""
		Оновлення зображення
		"""
		# застосування фізики
		self.vel_y += GRAVITY
		dx = self.direction * self.speed
		dy = self.vel_y

		# перевірка колізії з елементами рівня
		for tile in world.obstacle_list:
			# перевірка колізії зі стінами
			if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
				self.direction *= -1
				dx = self.direction * self.speed
			# перевірка колізії у напрямку y
			if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
				self.speed = 0
				# якщо гнаната нижче землі, тобто кинута
				if self.vel_y < 0:
					self.vel_y = 0
					dy = tile[1].bottom - self.rect.top
				# якщо вище, тобто падає
				elif self.vel_y >= 0:
					self.vel_y = 0
					dy = tile[1].top - self.rect.bottom	


		# оновлення позиції гранати
		self.rect.x += dx + screen_scroll
		self.rect.y += dy

		# зворотній відлік
		self.timer -= 1
		if self.timer <= 0:
			self.kill()
			grenade_fx.play()
			explosion = Explosion(self.rect.x, self.rect.y, 0.5)
			explosion_group.add(explosion)
			# наносити шкоду усім, хто поруч
			if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 2 and \
				abs(self.rect.centery - player.rect.centery) < TILE_SIZE * 2:
				player.health -= 50
			for enemy in enemy_group:
				if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 2 and \
					abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 2:
					enemy.health -= 50