import pygame, sys
from settings import *

# шаблон настроек pygame
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
pygame.display.set_caption('PP_platformer_overworld')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0, 0, 0))  # например (30, 30, 30) или 'grey'

    pygame.display.update()
    clock.tick(60)