import pygame
from tiles import Tile
from settings import tile_size, screen_width
from player import Player
from particle import Particle_Effect

# игровую логику помещаем сюда
class Level:
    def __init__(self, lvl_data, surface):
        
        # настройки уровня
        self.display_surface = surface
        self.lvl_setup(lvl_data)
        self.camera_shift = 0
        self.current_x = 0

        # частицы пыли
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False

    # вызов анимации частиц пыли
    def jump_dust_particles(self, pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(10, 5)
        else:
            pos += pygame.math.Vector2(10, -5)
        jump_particle_sprite = Particle_Effect(pos, 'jump')
        self.dust_sprite.add(jump_particle_sprite)

    # подтверждение, что персонаж упал на землю
    def get_char_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    # вызов анимации частиц пыли при приземлении
    def land_dust_particles(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10,15)
            else:
                offset = pygame.math.Vector2(-10,15)
            land_dust_particle = Particle_Effect(self.player.sprite.rect.midbottom - offset, 'land')
            self.dust_sprite.add(land_dust_particle)

    # настройки отрисовки уровня
    def lvl_setup(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        for row_index, row in enumerate(layout):
            for cell_index, cell in enumerate(row):
                x = cell_index * tile_size
                y = row_index * tile_size

                if cell == 'X':
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)
                if cell == 'P':
                    player_sprite = Player((x, y), self.display_surface, self.jump_dust_particles)
                    self.player.add(player_sprite)

    # следование камеры за игроком
    def move_camera(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 5 and direction_x < 0:
            self.camera_shift = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width / 5) and direction_x > 0:
            self.camera_shift = -8
            player.speed = 0
        else:
            self.camera_shift = 0
            player.speed = 8

    # проверка коллизий по горизонтали
    def x_axis_move_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):  # проверка столкновений
                if player.direction.x < 0:  # если игрок идет влево
                    player.rect.left = sprite.rect.right
                    player.on_left = True 
                    self.current_x = player.rect.left
                elif player.direction.x > 0:  # если игрок идет вправо
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

        # проверка уперся ли персонаж в стену слева или идет влево, и наоборот
        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    # проверка коллизий по вертикали
    def y_axis_move_collision(self):
        player = self.player.sprite
        player.gravity_simulate()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):  # проверка столкновений
                if player.direction.y > 0:  # если игрок падает вниз
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:  # если игрок прыгает вверх
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False

    # запуск, отрисовка, обновление экрана
    def run(self):
        # графика уровня
        self.tiles.update(self.camera_shift)
        self.tiles.draw(self.display_surface)
        self.move_camera()

        # графика игрока
        self.player.update()
        self.x_axis_move_collision()
        self.get_char_on_ground()
        self.y_axis_move_collision()
        self.land_dust_particles()
        self.player.draw(self.display_surface)

        # частицы пыли
        self.dust_sprite.update(self.camera_shift)
        self.dust_sprite.draw(self.display_surface)