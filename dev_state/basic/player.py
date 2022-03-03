import pygame
from support import import_folder

class Player(pygame.sprite.Sprite):
    
    # базовые настройки тайла персонажа игрока
    def __init__(self, pos, surface, jump_dust_particles):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        
        # движение игрока
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16

        # частицы пыли
        self.import_dust_run_particles()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15
        self.display_surface = surface
        self.jump_dust_particles = jump_dust_particles

        # статус действий игрока по умолчанию
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

    # импорт ассетов персонажа
    def import_character_assets(self):
        character_path = 'graphics\\character'
        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    # импорт частиц пыли для бега
    def import_dust_run_particles(self):
        self.dust_run_particles = import_folder('graphics\\character\\run')

    # настройка анимации персонажа игрока
    def player_animation(self):
        animation = self.animations[self.status]

        # цикл по индексам кадров анимации
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        img = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = img
        else:
            flipped_img = pygame.transform.flip(img, True, False)
            self.image = flipped_img

        # настройка области отрисовки rect
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        if self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)

    # настройка анимации частиц пыли при беге
    def run_dust_animation(self):
        if self.status == 'run' and self.on_ground:
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.dust_run_particles):
                self.dust_frame_index = 0

            dust_particle = self.dust_run_particles[int(self.dust_frame_index)]

            if self.facing_right:
                pos = self.rect.bottomleft - pygame.math.Vector2(6, 10)
                self.display_surface.blit(dust_particle, pos)
            else:
                pos = self.rect.bottomright - pygame.math.Vector2(6, 10)
                flipped_dust_particle = pygame.transform.flip(dust_particle, True, False)
                self.display_surface.blit(flipped_dust_particle, pos)

    # считывание кнопок клавиатуры
    def get_input(self):
        keys = pygame.key.get_pressed()

        # движение вправо/влево по кнопкам или стрелкам
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

        # прыжок
        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()
            self.jump_dust_particles(self.rect.midbottom)

    # получение текущего действия, выполняемого персонажем игрока
    def get_player_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    # симуляция гравитации
    def gravity_simulate(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    # прыжок игрока
    def jump(self):
        self.direction.y = self.jump_speed

    # обновление изображения, движение в указанном направлении
    def update(self):
        self.get_input()
        self.get_player_status()
        self.player_animation()
        self.run_dust_animation()