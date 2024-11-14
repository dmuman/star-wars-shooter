import pygame
from pygame import mixer
import pathlib

folder_path = pathlib.Path(__file__).parent.resolve()

mixer.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#define game variables
GRAVITY = 0.75
SCROLL_THRESH = 200
ROWS = 16
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 21
MAX_LEVELS = 3

#define player action variables


jump_fx = pygame.mixer.Sound(f'{folder_path}/audio/jump.wav')
jump_fx.set_volume(0.05)
shot_fx = pygame.mixer.Sound(f'{folder_path}/audio/shot.wav')
shot_fx.set_volume(0.05)
grenade_fx = pygame.mixer.Sound(f'{folder_path}/audio/grenade.wav')
grenade_fx.set_volume(0.05)


#load images
#button images
start_img = pygame.image.load(f'{folder_path}/img/start_btn.png').convert_alpha()
exit_img = pygame.image.load(f'{folder_path}/img/exit_btn.png').convert_alpha()
restart_img = pygame.image.load(f'{folder_path}/img/restart_btn.png').convert_alpha()
#background
pine1_img = pygame.image.load(f'{folder_path}/img/Background/pine1.png').convert_alpha()
pine2_img = pygame.image.load(f'{folder_path}/img/Background/pine2.png').convert_alpha()
mountain_img = pygame.image.load(f'{folder_path}/img/Background/mountain.png').convert_alpha()
sky_img = pygame.image.load(f'{folder_path}/img/Background/sky_cloud.png').convert_alpha()
#store tiles in a list
img_list = []
for x in range(TILE_TYPES):
	img = pygame.image.load(f'{folder_path}/img/Tile/{x}.png')
	img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
	img_list.append(img)
#bullet
bullet_img = pygame.image.load(f'{folder_path}/img/icons/bullet.png').convert_alpha()
#grenade
grenade_img = pygame.image.load(f'{folder_path}/img/icons/grenade.png').convert_alpha()
#pick up boxes
health_box_img = pygame.image.load(f'{folder_path}/img/icons/health_box.png').convert_alpha()
ammo_box_img = pygame.image.load(f'{folder_path}/img/icons/ammo_box.png').convert_alpha()
grenade_box_img = pygame.image.load(f'{folder_path}/img/icons/grenade_box.png').convert_alpha()
item_boxes = {
	'Health'	: health_box_img,
	'Ammo'		: ammo_box_img,
	'Grenade'	: grenade_box_img
}


#define colours
BG = (144, 201, 120)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
PINK = (235, 65, 54)

#create sprite groups
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()