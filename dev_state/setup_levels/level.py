import pygame
from support import import_csv_layout  # смотреть комменты в файле

class Level:
    # инициализация данных уровня, отображения картинки
    def __init__(self, level_data, surface):
        self.display_surf = surface

        terrain_layout = import_csv_layout(level_data['terrain'])
        print(terrain_layout)

    # запуск игры
    def run(self):
        pass