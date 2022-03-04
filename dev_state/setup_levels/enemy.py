import pygame
from tiles import AnimatedTile
from random import randint

class Enemy(AnimatedTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, 'graphics\\enemy\\run')
        self.rect.y += size - self.image.get_size()[1]  # смещение спрайта
        self.speed = randint(1, 5)

    # движение врагов
    def move(self):
        self.rect.x += self.speed

    def update(self, shift):
        self.rect.x += shift
        self.animation()
        self.move()