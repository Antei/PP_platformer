import pygame
from csv import reader
from settings import tile_size

# возвращает данные из экспортированных в csv данных карты уровня
def import_csv_layout(path):
    terrain_map = []
    with open(path) as map:
        lvl = reader(map, delimiter=',')
        for row in lvl:
            terrain_map.append(list(row))
        
        return terrain_map

# возвращает список нарезанного сета тайлов
def import_cut_tileset(path):
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / tile_size)
    tile_num_y = int(surface.get_size()[1] / tile_size)

    cut_tileset = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * tile_size
            y = row * tile_size
            new_surface = pygame.Surface((tile_size, tile_size))
            new_surface.blit(surface, (0, 0), pygame.Rect(x, y, tile_size, tile_size))
            cut_tileset.append(new_surface)

    return cut_tileset