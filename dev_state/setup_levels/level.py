from re import X
import pygame
from support import import_csv_layout, import_cut_tileset  # смотреть комменты в файле
from settings import tile_size
from tiles import Tile, StaticTile, Crate

class Level:
    # инициализация данных уровня, отображения картинки
    def __init__(self, level_data, surface):
        # основная настройка
        self.display_surf = surface
        self.move_camera = -5

        # настройка окружения terrain
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

        # настройка травы grass
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass')

        # настройка сундуков crates
        crate_layout = import_csv_layout(level_data['crate'])
        self.crate_sprites = self.create_tile_group(crate_layout, 'crate')

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
                    
                    sprite_group.add(sprite)

        return sprite_group

    # запуск игры
    def run(self):

        # окружение
        self.terrain_sprites.draw(self.display_surf)
        self.terrain_sprites.update(self.move_camera)

        # трава
        self.grass_sprites.draw(self.display_surf)
        self.grass_sprites.update(self.move_camera)

        # сундуки
        self.crate_sprites.draw(self.display_surf)
        self.crate_sprites.update(self.move_camera)