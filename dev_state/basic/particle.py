import pygame
from support import import_folder

# частицы пыли для прыжка и приземления
class Particle_Effect(pygame.sprite.Sprite):
    def __init__(self, pos, type):
        super().__init__()
        self.frame_index = 0
        self.animation_speed = 0.5
        if type == 'jump':
            self.frames = import_folder('graphics\\character\\dust_particles\\jump')
        if type == 'land':
            self.frames = import_folder('graphics\\character\\dust_particles\\land')
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)

    # анимация частиц пыли
    def dust_animation(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    # обновление отображаемого изображения
    def update(self, x_shift):
        self.dust_animation()
        self.rect.x += x_shift