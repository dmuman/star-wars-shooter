import pygame
import os
from constants import *
import random

class Soldier(pygame.sprite.Sprite):
	"""
	Клас для солдата, який буде використано 
	як для гравця, так і для противника
	"""
	def __init__(self, char_type, x, y, scale, speed, ammo, grenades):
		"""
		Ініціалізація об'єкту
		"""
		pygame.sprite.Sprite.__init__(self)
		self.alive = True
		self.char_type = char_type
		self.speed = speed
		self.ammo = ammo
		self.start_ammo = ammo
		self.shoot_cooldown = 0
		self.grenades = grenades
		self.health = 100
		self.max_health = self.health
		self.direction = 1
		self.vel_y = 0
		self.jump = False
		self.in_air = True
		self.flip = False
		self.animation_list = []
		self.frame_index = 0
		self.action = 0
		self.update_time = pygame.time.get_ticks()
		# змінні для ШІ
		self.move_counter = 0
		self.vision = pygame.Rect(0, 0, 150, 20)
		self.idling = False
		self.idling_counter = 0
		
		# завантаження всіх необхідних зображень для гравця
		animation_types = ['Idle', 'Run', 'Jump', 'Death']
		for animation in animation_types:
			# скидання тимчасового списку картинок
			temp_list = []
			# прорахунок кількості об'єктів в папці (кількість кадрів)
			num_of_frames = len(os.listdir(f'{folder_path}/img/{self.char_type}/{animation}'))
			for i in range(num_of_frames):
				img = pygame.image.load(f'{folder_path}/img/{self.char_type}/{animation}/{i}.png').convert_alpha()
				img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
				temp_list.append(img)
			self.animation_list.append(temp_list)

		self.image = self.animation_list[self.action][self.frame_index]
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.width = self.image.get_width()
		self.height = self.image.get_height()


	def update(self):
		"""
		Оновлення анімація
		"""
		self.update_animation()
		self.check_alive()
		# оновлення кулдауну
		if self.shoot_cooldown > 0:
			self.shoot_cooldown -= 1


	def move(self, moving_left, moving_right, bg_scroll, world):
		"""
		Функція для руху
		"""
		# скидання змінних руху
		screen_scroll = 0
		dx = 0
		dy = 0

		# оновлення змінних руху в залежності від напрямку
		if moving_left:
			dx = -self.speed
			self.flip = True
			self.direction = -1
		if moving_right:
			dx = self.speed
			self.flip = False
			self.direction = 1

		# стрибок
		if self.jump == True and self.in_air == False:
			self.vel_y = -11
			self.jump = False
			self.in_air = True

		# застосування гравітації
		self.vel_y += GRAVITY
		if self.vel_y > 10:
			self.vel_y
		dy += self.vel_y

		# перевірка колізії
		for tile in world.obstacle_list:
			# перевірка колізії у напрямку х
			if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
				dx = 0
				# якщо ШІ вдарився об стінку, то він повернеться в інший бік
				if self.char_type == 'enemy':
					self.direction *= -1
					self.move_counter = 0
			# перевірка колізії у напрямку у
			if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
				# перевірка на те, чи нижче землі, тобто стрибок
				if self.vel_y < 0:
					self.vel_y = 0
					dy = tile[1].bottom - self.rect.top
				# на те, чи вище, тобто падіння
				elif self.vel_y >= 0:
					self.vel_y = 0
					self.in_air = False
					dy = tile[1].top - self.rect.bottom


		# перевірка на колізію з водою
		if pygame.sprite.spritecollide(self, water_group, False):
			self.health = 0

		# перевірка на колізію з виходом
		level_complete = False
		if pygame.sprite.spritecollide(self, exit_group, False):
			level_complete = True

		# якщо випав з карти
		if self.rect.bottom > SCREEN_HEIGHT:
			self.health = 0


		# перевірка, чи не виходить за межі екрану
		if self.char_type == 'player':
			if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
				dx = 0

		# оновлення позиції
		self.rect.x += dx
		self.rect.y += dy

		# оновлення скролу в залежності від позиціх гравця
		if self.char_type == 'player':
			if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and bg_scroll < (world.level_length * TILE_SIZE) - SCREEN_WIDTH)\
				or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
				self.rect.x -= dx
				screen_scroll = -dx

		return screen_scroll, level_complete



	def shoot(self):
		"""
		Функція для пострілу
		"""
		from Bullet import Bullet
		if self.shoot_cooldown == 0 and self.ammo > 0:
			self.shoot_cooldown = 20
			bullet = Bullet(self.rect.centerx + (0.75 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
			bullet_group.add(bullet)
			# зменшення кількості патронів
			self.ammo -= 1
			shot_fx.play()


	def ai(self, screen_scroll, player, bg_scroll, world):
		"""
		Функція для ШІ
		"""
		if self.alive and player.alive:
			if self.idling == False and random.randint(1, 200) == 1:
				self.update_action(0) #0: idle
				self.idling = True
				self.idling_counter = 50
			# перевірка, чи боти біля гравця
			if self.vision.colliderect(player.rect):
				# зупинка бігу й поворот в бік гравця
				self.update_action(0) #0: idle
				# постріл
				self.shoot()
			else:
				if self.idling == False:
					if self.direction == 1:
						ai_moving_right = True
					else:
						ai_moving_right = False
					ai_moving_left = not ai_moving_right
					self.move(ai_moving_left, ai_moving_right, bg_scroll, world)
					self.update_action(1) #1: run
					self.move_counter += 1
					# оновлення зору ботів, коли вони рухаються
					self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)

					if self.move_counter > TILE_SIZE:
						self.direction *= -1
						self.move_counter *= -1
				else:
					self.idling_counter -= 1
					if self.idling_counter <= 0:
						self.idling = False

		# скрол
		self.rect.x += screen_scroll


	def update_animation(self):
		"""
		Оновленнч анімації
		"""
		# оновлення анімації
		ANIMATION_COOLDOWN = 100
		# оновлення картинки в залежності від кадру
		self.image = self.animation_list[self.action][self.frame_index]
		# перевірка, чи пройшло достатньо часу з минулого оновлення
		if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
			self.update_time = pygame.time.get_ticks()
			self.frame_index += 1
		# якщо анімація кінчилась - почати її спочатку
		if self.frame_index >= len(self.animation_list[self.action]):
			if self.action == 3:
				self.frame_index = len(self.animation_list[self.action]) - 1
			else:
				self.frame_index = 0



	def update_action(self, new_action):
		"""
		Оновлення дій
		"""
		# перевірка, чи теперішня дія відрізняється від попередньої
		if new_action != self.action:
			self.action = new_action
			# оновлення налаштувань анімації
			self.frame_index = 0
			self.update_time = pygame.time.get_ticks()



	def check_alive(self):
		"""
		Перевірка на те, чи живий
		"""
		if self.health <= 0:
			self.health = 0
			self.speed = 0
			self.alive = False
			self.update_action(3)


	def draw(self):
		"""
		Відображення
		"""
		screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)