from os import walk
import pygame

# подключение директорий
def import_folder(path):
    surface_lst = []
    
    for _, __, img_files in walk(path):
        for img in img_files:
            full_path = path + '\\' + img
            img_surf = pygame.image.load(full_path).convert_alpha()
            surface_lst.append(img_surf)
    print(surface_lst)
    return surface_lst