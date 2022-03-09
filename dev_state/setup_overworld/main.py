import pygame, sys

# шаблон настроек pygame
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
pygame.display.set_caption('PP_platformer_overworld')
#lvl = Level(level_0, screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0, 0, 0))  # или например (30, 30, 30) --RGB или 'grey'
    #lvl.run()

    pygame.display.update()
    clock.tick(60)