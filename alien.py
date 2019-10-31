import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    # Класс представляющий одного пришельца
    def __init__(self, ai_settings, screen):
        # Инициализирует пришельца и задает его начальную позицию
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.x = 0

        # Загрузка изображения пришельца и назначение атрибута rect
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Каждый новы пришелец появляется в левом верхнем углу экрна
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Сохранение точной позиции пришельца
        self.rect.y = float(self.rect.x)

    def blitme(self):
        # Выводит пришельца в текущем положении
        self.screen.blit(self.image, self.rect)

    def update(self):
        # Перемещает пришельцев вправо
        self.rect.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)

    def check_edges(self):
        # Возвращает True, если пришелец находится у крааев эркана
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
