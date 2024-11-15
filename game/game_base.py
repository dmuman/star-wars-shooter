import pygame

# ініціалізація pygame
pygame.init()

# налаштування екрану
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Базова концепція гри")

# констранти кольорів
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# властивості гравця
player_size = 50
player_x = WIDTH // 2
player_y = HEIGHT // 2
player_speed = 5

# головний цикл гри
running = True
while running:
    # обробка подій
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # отримання натиснутих клавіш
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed

    # логіка для обмеження руху гравця в межах екрану
    player_x = max(0, min(WIDTH - player_size, player_x))
    player_y = max(0, min(HEIGHT - player_size, player_y))

    # малювання
    screen.fill(BLACK)  # заливка фону
    pygame.draw.rect(screen, RED, (player_x, player_y, player_size, player_size))  # відображення гравця

    pygame.display.flip()  # оновлення екрану
    pygame.time.Clock().tick(60)  # обмеження FPS до 60

pygame.quit()