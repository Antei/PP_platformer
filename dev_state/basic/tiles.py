import pygame

class Tile(pygame.sprite.Sprite):
    # базовые настройки тайла карты
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface((size, size))  # создаем поверхность с размерами x, y
        self.image.fill('grey')  # заполняем серым цветом, или другим по (R, G, B)
        self.rect = self.image.get_rect(topleft = pos)

    # обновление изображения на экране
    def update(self, x_shift):
        self.rect.x += x_shift  # сдвиг камеры по оси Х