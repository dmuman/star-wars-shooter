import pygame
import os
from constants import folder_path

pygame.init()

# всновлення розмірів екрану
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Базова фізика')

# встановлення обмеження FPS
clock = pygame.time.Clock()
FPS = 60

# константа гравітації
GRAVITY = 0.75

# визначення змінних руху
moving_left = False
moving_right = False
shoot = False


# завантаження картинки патрону
bullet_img = pygame.image.load(f'{folder_path}/img/icons/bullet.png').convert_alpha()


# визначення кольорів
BG = (144, 201, 120)
RED = (255, 0, 0)

# відображення фону
def draw_bg():
	screen.fill(BG)
	pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300))



class Soldier(pygame.sprite.Sprite):
	"""
	Клас для солдата, який буде використано 
	як для гравця, так і для противника
	"""
	def __init__(self, char_type, x, y, scale, speed, ammo):
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
		
		# завантаження всіх необхідних зображень
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


	def update(self):
		"""
		Оновлення анімація
		"""
		self.update_animation()
		self.check_alive()
		# оновлення кулдауну
		if self.shoot_cooldown > 0:
			self.shoot_cooldown -= 1


	def move(self, moving_left, moving_right):
		"""
		Функція для руху
		"""
		# скидання змінних руху
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

		# перевірка колізії з підлогою
		if self.rect.bottom + dy > 300:
			dy = 300 - self.rect.bottom
			self.in_air = False

		# оновлення позиції
		self.rect.x += dx
		self.rect.y += dy


	def shoot(self):
		"""
		Функція для пострілу
		"""
		if self.shoot_cooldown == 0 and self.ammo > 0:
			self.shoot_cooldown = 20
			bullet = Bullet(self.rect.centerx + (0.6 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
			bullet_group.add(bullet)
			# зменшення кількості патронів
			self.ammo -= 1


	def update_animation(self):
		"""
		Оновлення анімації
		"""
		# кулдаун анімації
		ANIMATION_COOLDOWN = 100
		# оновлення зображення в залежності від фрейму
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



class Bullet(pygame.sprite.Sprite):
	"""
	Клас для патрону
	"""
	def __init__(self, x, y, direction):
		"""
		Ініціалізаіця
		"""
		pygame.sprite.Sprite.__init__(self)
		self.speed = 10
		self.image = bullet_img
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.direction = direction

	def update(self):
		"""
		Оновлення
		"""
		# рух патрону
		self.rect.x += (self.direction * self.speed)
		# перевірка, чи патрон вилетів за екран
		if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
			self.kill()

		# перевірка колізії з персонажами
		if pygame.sprite.spritecollide(player, bullet_group, False):
			if player.alive:
				player.health -= 5
				self.kill()
		if pygame.sprite.spritecollide(enemy, bullet_group, False):
			if enemy.alive:
				enemy.health -= 25
				self.kill()



# створення групи спрайтів
bullet_group = pygame.sprite.Group()


# створення персонажів
player = Soldier('player', 200, 200, 3, 5, 20)
enemy = Soldier('enemy', 400, 200, 3, 5, 20)


# головний цикл гри
run = True
while run:

	clock.tick(FPS)

	draw_bg()

	player.update()
	player.draw()

	enemy.update()
	enemy.draw()

	# оновлення та відображення груп
	bullet_group.update()
	bullet_group.draw(screen)


	# оновлення дій гравця
	if player.alive:
		# постріл
		if shoot:
			player.shoot()
		if player.in_air:
			player.update_action(2)#2 : стрибок
		elif moving_left or moving_right:
			player.update_action(1)# 1: біг
		else:
			player.update_action(0)# 0: idle
		player.move(moving_left, moving_right)


	for event in pygame.event.get():
		# вихід з гри
		if event.type == pygame.QUIT:
			run = False
		# натискання клавіш
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_a:
				moving_left = True
			if event.key == pygame.K_d:
				moving_right = True
			if event.key == pygame.K_SPACE:
				shoot = True
			if event.key == pygame.K_w and player.alive:
				player.jump = True
			if event.key == pygame.K_ESCAPE:
				run = False


		# відпускання клавіш
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_a:
				moving_left = False
			if event.key == pygame.K_d:
				moving_right = False
			if event.key == pygame.K_SPACE:
				shoot = False




	pygame.display.update()

pygame.quit()