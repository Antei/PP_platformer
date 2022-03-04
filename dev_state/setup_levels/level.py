from re import X
import pygame
from support import import_csv_layout, import_cut_tileset  # смотреть комменты в файле
from settings import tile_size
from tiles import *
from enemy import Enemy

class Level:
    # инициализация данных уровня, отображения картинки
    def __init__(self, level_data, surface):
        # основная настройка
        self.display_surf = surface
        self.move_camera = -5

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
                    pass
                    print('player start here')
                elif value == '1':
                    hat_surface = pygame.image.load('graphics\\character\\hat.png').convert_alpha()
                    sprite = StaticTile(tile_size, x, y, hat_surface)
                    self.goal.add(sprite)

    # запуск игры
    def run(self):

        # пальмы на заднем плане
        self.bg_palms_sprites.draw(self.display_surf)
        self.bg_palms_sprites.update(self.move_camera)

        # окружение
        self.terrain_sprites.draw(self.display_surf)
        self.terrain_sprites.update(self.move_camera)

        # сундуки
        self.crate_sprites.draw(self.display_surf)
        self.crate_sprites.update(self.move_camera)

        # враги
        # препятствия для врагов
        # отрисовка через метод draw не нужна
        self.enemies_sprites.update(self.move_camera)
        self.constraints_sprites.update(self.move_camera)
        self.constraints_reverse_enemy()
        self.enemies_sprites.draw(self.display_surf)

        # трава
        self.grass_sprites.draw(self.display_surf)
        self.grass_sprites.update(self.move_camera)

        # монеты
        self.coins_sprites.draw(self.display_surf)
        self.coins_sprites.update(self.move_camera)

        # пальмы на переднем плане
        self.fg_palms_sprites.draw(self.display_surf)
        self.fg_palms_sprites.update(self.move_camera)

        # спрайты игрока
        self.goal.draw(self.display_surf)
        self.goal.update(self.move_camera)