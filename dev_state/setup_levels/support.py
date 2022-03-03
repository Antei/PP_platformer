from csv import reader

# возвращает данные из экспортированных в csv данных карты уровня
def import_csv_layout(path):
    terrain_map = []
    with open(path) as map:
        lvl = reader(map, delimiter=',')
        for row in lvl:
            terrain_map.append(list(row))
        
        return terrain_map