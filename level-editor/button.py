import pygame

class Button():
    """
    Клас для кнопки
    """
    def __init__(self, x: int, y: int, image: pygame.Surface, scale: int | float):
        """
        Ініціалізація кнопки
        """
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface: pygame.Surface) -> bool:
        """
        Функція для відображення (малювання)
        кнопки на екрані.

        Повертає
        """
        action = False
        # отримання позиції мишки
        pos = pygame.mouse.get_pos()
        
        # перевірка, чи було наведено на кнопку мишку
        # та чи було її натиснуто
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        # якщо кнопку відпустили
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # відображення кнопки на екрані
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action