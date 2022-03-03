import pygame, sys
from settings import *
from level import Level

# шаблон настроек pygame
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
pygame.display.set_caption('PP_platformer')
#lvl = Level(level_data, screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        screen.fill((30, 30, 30))  # или 'black'
#        lvl.run()

        pygame.display.update()
        clock.tick(60)