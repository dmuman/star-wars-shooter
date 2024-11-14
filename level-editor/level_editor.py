import pygame
import csv
import pathlib
from button import Button

# шлях до папки
folder_path = pathlib.Path(__file__).parent.resolve()

# ініціалізація pygame
pygame.init()

# налаштування FPS (к-сть кадрів в секунду)
clock = pygame.time.Clock()
FPS = 60

# розміри вікна
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
LOWER_MARGIN = 100
SIDE_MARGIN = 300

# відображення вікна
screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption('Редактор рівнів')

# визначення констант
ROWS = 16       # к-сть рядків в вікні
MAX_COLS = 150  # к-сть колонок в вікні
TILE_SIZE = SCREEN_HEIGHT // ROWS   # розмір кожної плиточки
TILE_TYPES = 21 # к-сть плиточок

# визначення кольорів
BLUE = (158, 154, 215)
WHITE = (255, 255, 255)
RED = (200, 25, 25)

# визначення шрифту
FONT = pygame.font.SysFont('Futura', 30)

# визначення інщих змінних
level = 0               # номер рівня
current_tile = 0        # номер поточної плиточки
scroll_left = False     # скрол вліво
scroll_right = False    # скрол вправо
scroll = 0              # скрол
scroll_speed = 1        # швидкість скролу

# завантаження картинок
city1_img = pygame.image.load(f'{folder_path}/img/Background/city1.png').convert_alpha()
city2_img = pygame.image.load(f'{folder_path}/img/Background/city2.png').convert_alpha()
city_back_img = pygame.image.load(f'{folder_path}/img/Background/city_back.png').convert_alpha()
sky_img = pygame.image.load(f'{folder_path}/img/Background/sky.png').convert_alpha()

# збереження картинок плиточок в списку
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'{folder_path}/img/tile/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

# завантаження кнопок збереження та завантаження
save_img = pygame.image.load(f'{folder_path}/img/Button/save_btn.png').convert_alpha()
load_img = pygame.image.load(f'{folder_path}/img/Button/load_btn.png').convert_alpha()

# створення пустого списку плиточок
world_data = []
for row in range(ROWS):
    # по дефолту, все дорівною -1
    # тобто нічому (повітрю)
    r = [-1] * MAX_COLS
    world_data.append(r)

# створення нижнього рівня
# (заповнення нижнього рядка 0-ю плиточкою)
for tile in range(0, MAX_COLS):
    world_data[ROWS - 1][tile] = 0


def draw_text(text, font, text_col, x, y):
    """
    Функція для відобреження тексту на екрані
    """
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def draw_bg():
    """
    Функція для відображення заднього фону
    з ефектом паралаксу
    """
    screen.fill(BLUE)
    width = sky_img.get_width()
    for x in range(4):
        # для створення ефекту паралаксу при прокручуванні
        # кожна картинка буде пропкручуватись з різною швидкістю
        screen.blit(sky_img, ((x * width) - scroll * 0.5, 0))
        screen.blit(city_back_img, ((x * width) - scroll * 0.6, SCREEN_HEIGHT - city_back_img.get_height() - 300))
        screen.blit(city1_img, ((x * width) - scroll * 0.7, SCREEN_HEIGHT - city1_img.get_height() - 150))
        screen.blit(city2_img, ((x * width) - scroll * 0.8, SCREEN_HEIGHT - city2_img.get_height()))


def draw_grid():
    """
    Функція для відображення гріду
    """
    # вертикальні лінії
    for c in range(MAX_COLS + 1):
        pygame.draw.line(screen, WHITE, (c * TILE_SIZE - scroll, 0), (c * TILE_SIZE - scroll, SCREEN_HEIGHT))

    # горизонтальні лінії
    for c in range(ROWS + 1):
        pygame.draw.line(screen, WHITE, (0, c * TILE_SIZE), (SCREEN_WIDTH, c * TILE_SIZE))


def draw_world():
    """
    Функція для відображення плиточок
    (по суті, відображення самого світу) 
    """
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            # якщо плиточка має значення
            if tile >= 0:
                screen.blit(img_list[tile], (x * TILE_SIZE - scroll, y * TILE_SIZE))

# створення кнопок
save_btn = Button(SCREEN_WIDTH // 1.1, SCREEN_HEIGHT + LOWER_MARGIN - 75, save_img, 1)
load_btn = Button(SCREEN_WIDTH // 1.1 + 200, SCREEN_HEIGHT + LOWER_MARGIN - 75, load_img, 1)

# створення списку кнопок
button_list = []
button_col = 0
button_row = 0

# створення кнопок для плиточок, щоб їх можна було розміщати
for i in range(len(img_list)):
    tile_button = Button(SCREEN_WIDTH + (75 * button_col) + 50, 75 * button_row + 50, img_list[i], 1)
    button_list.append(tile_button)
    button_col += 1
    # максимум 3 колонки
    if button_col == 3:
        button_row += 1
        button_col = 0


# головний цикл
run = True
while run:

    clock.tick(FPS)

    # відображення заднього фону, гріду, плиточок
    draw_bg()
    draw_grid()
    draw_world()

    # додавання тексту
    draw_text(f'Рівень: {level}', FONT, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 90)
    draw_text('Треба натиснути стрілочку ВВЕРХ чи ВНИЗ щоб змінити рівень', FONT, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 60)

    # збереження даних
    if save_btn.draw(screen):
        # збереження у форматі csv, щоб було зручніше потім вивантажувати дані
        with open(f'level{level}_data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter = ',')
            for row in world_data:
                writer.writerow(row)

    # завантаження даних
    if load_btn.draw(screen):
        # скрол скидається до початку рівня
        scroll = 0
        with open(f'level{level}_data.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter = ',')
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    # наповнення списку плиточок
                    world_data[x][y] = int(tile)
                

    # відображення панелі плиточок і самих плиточок
    pygame.draw.rect(screen, BLUE, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))

    # обрання плиточки
    button_count = 0
    for button_count, i in enumerate(button_list):
        if i.draw(screen):
            current_tile = button_count

    # хайлайт обраної плиточки
    pygame.draw.rect(screen, RED, button_list[current_tile].rect, 3)

    # склор карти
    if scroll_left and scroll > 0:
        scroll -= 5 * scroll_speed
    if scroll_right and scroll < (MAX_COLS * TILE_SIZE) - SCREEN_WIDTH:
        scroll +=5 * scroll_speed

    # додавання нових плиточок на екран
    # отримання позиції мишки
    pos = pygame.mouse.get_pos()
    x = (pos[0] + scroll) // TILE_SIZE
    y = pos[1] // TILE_SIZE

    # перевірка, чи координати в межах дозволеної області
    if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
        # оновлення значення плиточки
        if pygame.mouse.get_pressed()[0] == 1:
            if world_data[y][x] != current_tile:
                world_data[y][x] = current_tile

        # видалення плиточки
        if pygame.mouse.get_pressed()[2] == 1:
            world_data[y][x] = -1

    # перевірка івентів (натискання клавіш)
    for event in pygame.event.get():
        # якщо було натиснуто кнопку вийти (червоний хрестик)
        if event.type == pygame.QUIT:
            run = False
        
        # натискання клавіш
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                level += 1
            if event.key == pygame.K_DOWN or event.key == pygame.K_s and level > 0:
                level -= 1
            if event.key == pygame.K_LEFT or event.key == pygame.K_d:
                scroll_left = True
            if event.key == pygame.K_RIGHT or event.key == pygame.K_a:
                scroll_right = True
            # лівий шифт для швидшого скролу
            if event.key == pygame.K_LSHIFT:
                scroll_speed = 5

        # якщо клавішу більше не натискають
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_d:
                scroll_left = False
            if event.key == pygame.K_RIGHT or event.key == pygame.K_a:
                scroll_right = False
            if event.key == pygame.K_LSHIFT:
                scroll_speed = 1
            
    # оновлення екрану
    pygame.display.update()

pygame.quit()