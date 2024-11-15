import pygame
import csv
from Button import Button
from constants import *
from ScreenFade import ScreenFade
from World import World
from Grenade import Grenade

pygame.init()

pygame.display.set_caption('Shooter')

#set framerate
clock = pygame.time.Clock()
FPS = 60
font = pygame.font.SysFont('Futura', 30)
start_game = False
start_intro = False
moving_left = False
moving_right = False
shoot = False
grenade = False
grenade_thrown = False
screen_scroll = 0
bg_scroll = 0
level = 1

def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))


def draw_bg():
	screen.fill(BG)
	width = sky_img.get_width()
	for x in range(5):
		screen.blit(sky_img, ((x * width) - bg_scroll * 0.5, 0))
		screen.blit(city_back_img, ((x * width) - bg_scroll * 0.6, SCREEN_HEIGHT - city_back_img.get_height() - 300))
		screen.blit(city1_img, ((x * width) - bg_scroll * 0.7, SCREEN_HEIGHT - city1_img.get_height() - 150))
		screen.blit(city2_img, ((x * width) - bg_scroll * 0.8, SCREEN_HEIGHT - city2_img.get_height()))

world_data = []
for row in range(ROWS):
	r = [-1] * COLS
	world_data.append(r)
#load in level data and create world
with open(f'{folder_path}/level{level}_data.csv', newline='') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	for x, row in enumerate(reader):
		for y, tile in enumerate(row):
			world_data[x][y] = int(tile)
world = World()
player, health_bar = world.process_data(world_data)

#function to reset level
def reset_level():
	enemy_group.empty()
	bullet_group.empty()
	grenade_group.empty()
	explosion_group.empty()
	item_box_group.empty()
	decoration_group.empty()
	water_group.empty()
	exit_group.empty()

	#create empty tile list
	data = []
	for row in range(ROWS):
		r = [-1] * COLS
		data.append(r)

	return data


#create screen fades
intro_fade = ScreenFade(1, BLACK, 4)
death_fade = ScreenFade(2, PINK, 4)


#create buttons
start_button = Button(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 - 150, start_img, 1)
exit_button = Button(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 50, exit_img, 1)
restart_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, restart_img, 2)

run = True
while run:

	clock.tick(FPS)

	if start_game == False:
		#draw menu
		screen.fill(BG)
		#add buttons
		if start_button.draw(screen):
			start_game = True
			start_intro = True
		if exit_button.draw(screen):
			run = False
	else:
		#update background
		draw_bg()
		#draw world map
		world.draw(screen_scroll)
		#show player health
		health_bar.draw(player.health)
		#show ammo
		draw_text('AMMO: ', font, WHITE, 10, 35)
		for x in range(player.ammo):
			screen.blit(bullet_img, (90 + (x * 10), 40))
		#show grenades
		draw_text('GRENADES: ', font, WHITE, 10, 60)
		for x in range(player.grenades):
			screen.blit(grenade_img, (135 + (x * 15), 60))


		player.update()
		player.draw()

		for enemy in enemy_group:
			enemy.ai(screen_scroll, player, bg_scroll, world)
			enemy.update()
			enemy.draw()

		#update and draw groups
		bullet_group.update(screen_scroll, world, player)
		grenade_group.update(screen_scroll, world, player)
		explosion_group.update(screen_scroll)
		item_box_group.update(screen_scroll, player)
		decoration_group.update(screen_scroll)
		water_group.update(screen_scroll)
		exit_group.update(screen_scroll)
		bullet_group.draw(screen)
		grenade_group.draw(screen)
		explosion_group.draw(screen)
		item_box_group.draw(screen)
		decoration_group.draw(screen)
		water_group.draw(screen)
		exit_group.draw(screen)

		#show intro
		if start_intro == True:
			if intro_fade.fade():
				start_intro = False
				intro_fade.fade_counter = 0


		#update player actions
		if player.alive:
			#shoot bullets
			if shoot:
				player.shoot()
			#throw grenades
			elif grenade and grenade_thrown == False and player.grenades > 0:
				grenade = Grenade(player.rect.centerx + (0.5 * player.rect.size[0] * player.direction),\
				 			player.rect.top, player.direction)
				grenade_group.add(grenade)
				#reduce grenades
				player.grenades -= 1
				grenade_thrown = True
			if player.in_air:
				player.update_action(2)#2: jump
			elif moving_left or moving_right:
				player.update_action(1)#1: run
			else:
				player.update_action(0)#0: idle
			screen_scroll, level_complete = player.move(moving_left, moving_right, bg_scroll, world)
			bg_scroll -= screen_scroll
			#check if player has completed the level
			if level_complete:
				start_intro = True
				level += 1
				bg_scroll = 0
				world_data = reset_level()
				if level <= MAX_LEVELS:
					#load in level data and create world
					with open(f'{folder_path}/level{level}_data.csv', newline='') as csvfile:
						reader = csv.reader(csvfile, delimiter=',')
						for x, row in enumerate(reader):
							for y, tile in enumerate(row):
								world_data[x][y] = int(tile)
					world = World()
					player, health_bar = world.process_data(world_data)	
		else:
			screen_scroll = 0
			if death_fade.fade():
				if restart_button.draw(screen):
					death_fade.fade_counter = 0
					start_intro = True
					bg_scroll = 0
					world_data = reset_level()
					#load in level data and create world
					with open(f'{folder_path}/level{level}_data.csv', newline='') as csvfile:
						reader = csv.reader(csvfile, delimiter=',')
						for x, row in enumerate(reader):
							for y, tile in enumerate(row):
								world_data[x][y] = int(tile)
					world = World()
					player, health_bar = world.process_data(world_data)


	for event in pygame.event.get():
		#quit game
		if event.type == pygame.QUIT:
			run = False
		#keyboard presses
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_a:
				moving_left = True
			if event.key == pygame.K_d:
				moving_right = True
			if event.key == pygame.K_SPACE:
				shoot = True
			if event.key == pygame.K_q:
				grenade = True
			if event.key == pygame.K_w and player.alive:
				player.jump = True
				jump_fx.play()
			if event.key == pygame.K_ESCAPE:
				run = False


		#keyboard button released
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_a:
				moving_left = False
			if event.key == pygame.K_d:
				moving_right = False
			if event.key == pygame.K_SPACE:
				shoot = False
			if event.key == pygame.K_q:
				grenade = False
				grenade_thrown = False


	pygame.display.update()

pygame.quit()