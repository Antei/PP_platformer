import pygame
from tiles import AnimatedTile
from random import randint

class Enemy(AnimatedTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, 'graphics\\enemy\\run')
        self.rect.y += size - self.image.get_size()[1]  # смещение спрайта
        self.speed = randint(2, 4)

    # движение врагов
    def move(self):
        self.rect.x += self.speed

    # разворот изображения
    def reverse_img(self):
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image, True, False)

    # реверс направления движения
    def reverse_side(self):
        self.speed *= -1

    def update(self, shift):
        self.rect.x += shift
        self.animation()
        self.move()
        self.reverse_img()