import pygame
from support import import_csv_layout, import_cut_tileset  # смотреть комменты в файле
from settings import *
from tiles import *
from enemy import Enemy
from decoration import *
from player import Player
from particle import Particle_Effect

class Level:
    # инициализация данных уровня, отображения картинки
    def __init__(self, level_data, surface):
        # основная настройка
        self.display_surf = surface
        self.camera_shift = 0
        self.current_x = None

        # настройка игрока
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        # настройка окружения terrain
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

        # настройка травы grass
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass')

        # настройка сундуков crates
        crate_layout = import_csv_layout(level_data['crate'])
        self.crate_sprites = self.create_tile_group(crate_layout, 'crate')

        # настройка монет
        coins_layout = import_csv_layout(level_data['coins'])
        self.coins_sprites = self.create_tile_group(coins_layout, 'coins')

        # настройка пальм на переднем плане
        fg_palms_layout = import_csv_layout(level_data['fg_palms'])
        self.fg_palms_sprites = self.create_tile_group(fg_palms_layout, 'fg_palms')

        # настройка пальм на заднем плане
        bg_palms_layout = import_csv_layout(level_data['bg_palms'])
        self.bg_palms_sprites = self.create_tile_group(bg_palms_layout, 'bg_palms')

        # настройка врагов
        enemies_layout = import_csv_layout(level_data['enemies'])
        self.enemies_sprites = self.create_tile_group(enemies_layout, 'enemies')

        # настройка препятствий для врагов
        constraints_layout = import_csv_layout(level_data['constraints'])
        self.constraints_sprites = self.create_tile_group(constraints_layout, 'constraints')

        # декорации уровня
        self.sky = Sky(8)
        level_width = len(terrain_layout[0]) * tile_size
        self.water = Water(screen_height - 30, level_width)
        self.clouds = Clouds(400, level_width, 30)

        # частицы пыли
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            #print(row_index, row, sep='\n')  # проверка
            for value_index, value in enumerate(row):
                if value != '-1':
                    x = value_index * tile_size
                    y = row_index * tile_size

                    if type == 'terrain':
                        terrain_tile_list = import_cut_tileset('graphics\\terrain\\terrain_tiles.png')
                        tile_surface = terrain_tile_list[int(value)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == 'grass':
                        grass_tile_list = import_cut_tileset('graphics\\decoration\\grass\\grass.png')
                        tile_surface = grass_tile_list[int(value)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == 'crate':
                        sprite = Crate(tile_size, x, y)

                    if type == 'coins':
                        if value == '0':
                            sprite = Coin(tile_size, x, y, 'graphics\\coins\\gold')
                        elif value == '1':
                            sprite = Coin(tile_size, x, y, 'graphics\\coins\\silver')

                    if type == 'fg_palms':
                        if value == '4':  # при создании тайлсета для пальм назначены такие id
                            sprite = Palm(tile_size, x, y, 'graphics\\terrain\\palm_small', 38)
                        elif value == '8':  # при создании тайлсета для пальм назначены такие id
                            sprite = Palm(tile_size, x, y, 'graphics\\terrain\\palm_large', 64)

                    if type == 'bg_palms':
                        sprite = Palm(tile_size, x, y, 'graphics\\terrain\\palm_bg', 64)

                    if type == 'enemies':
                        sprite = Enemy(tile_size, x, y)

                    if type == 'constraints':
                        sprite = Tile(tile_size, x, y)
                    
                    sprite_group.add(sprite)

        return sprite_group

    # разворот врагов после коллизии с препятствием-ограничителем
    def constraints_reverse_enemy(self):
        for enemy in self.enemies_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraints_sprites, False):
                enemy.reverse_side()

    # настройка игрока
    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for value_index, value in enumerate(row):
                x = value_index * tile_size
                y = row_index * tile_size
                if value == '0':
                    sprite = Player((x, y), self.display_surf, self.jump_dust_particles)
                    self.player.add(sprite)
                elif value == '1':
                    hat_surface = pygame.image.load('graphics\\character\\hat.png').convert_alpha()
                    sprite = StaticTile(tile_size, x, y, hat_surface)
                    self.goal.add(sprite)

    # вызов анимации частиц пыли
    def jump_dust_particles(self, pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(10, 5)
        else:
            pos += pygame.math.Vector2(10, -5)
        jump_particle_sprite = Particle_Effect(pos, 'jump')
        self.dust_sprite.add(jump_particle_sprite)

    # проверка коллизий по горизонтали
    def x_axis_move_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        collidable_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites() + self.fg_palms_sprites.sprites()

        for sprite in collidable_sprites:
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
        collidable_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites() + self.fg_palms_sprites.sprites()

        for sprite in collidable_sprites:
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

    # следование камеры за игроком
    def move_camera(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 4 and direction_x < 0:
            self.camera_shift = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.camera_shift = -8
            player.speed = 0
        else:
            self.camera_shift = 0
            player.speed = 8

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

    # запуск игры
    def run(self):

        # небо
        self.sky.draw(self.display_surf)
        self.clouds.draw(self.display_surf, self.camera_shift)

        # пальмы на заднем плане
        self.bg_palms_sprites.draw(self.display_surf)
        self.bg_palms_sprites.update(self.camera_shift)

        # окружение
        self.terrain_sprites.draw(self.display_surf)
        self.terrain_sprites.update(self.camera_shift)

        # сундуки
        self.crate_sprites.draw(self.display_surf)
        self.crate_sprites.update(self.camera_shift)

        # враги
        # препятствия для врагов
        # отрисовка через метод draw не нужна
        self.enemies_sprites.update(self.camera_shift)
        self.constraints_sprites.update(self.camera_shift)
        self.constraints_reverse_enemy()
        self.enemies_sprites.draw(self.display_surf)

        # трава
        self.grass_sprites.draw(self.display_surf)
        self.grass_sprites.update(self.camera_shift)

        # монеты
        self.coins_sprites.draw(self.display_surf)
        self.coins_sprites.update(self.camera_shift)

        # пальмы на переднем плане
        self.fg_palms_sprites.draw(self.display_surf)
        self.fg_palms_sprites.update(self.camera_shift)

        # пыль
        self.dust_sprite.update(self.camera_shift)
        self.dust_sprite.draw(self.display_surf)

        # спрайты игрока
        self.player.update()  # судя по всему, лучше сначала обновляться, а потом отрисовывать

        self.x_axis_move_collision()
        self.get_char_on_ground()
        self.y_axis_move_collision()
        self.land_dust_particles()

        self.move_camera()
        self.player.draw(self.display_surf)
        self.goal.draw(self.display_surf)
        self.goal.update(self.camera_shift)

        # вода
        self.water.draw(self.display_surf, self.camera_shift)