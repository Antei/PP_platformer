import pygame, sys
from settings import *
from level import Level
from gamedata import level_0

# шаблон настроек pygame
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
pygame.display.set_caption('PP_platformer')
lvl = Level(level_0, screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        screen.fill('black')  # или например (30, 30, 30)
        lvl.run()

        pygame.display.update()
        clock.tick(60)