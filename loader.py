from models.chair import Chair
from models.table import Table

class Loader:
    def __init__(self):
        self.initial_load()

    def initial_load(self):
        self.load_tables()
        self.load_chairs()

    def load_chairs(self):
        coords = self.read_coords('assets/chair_coords.txt')
        for i in range(1, len(coords) + 1):
            chair = Chair(i, int('1000' +  str(i).zfill(3)), False)
            Chair.instances.append(chair)
        for chair, coord in zip(Chair.instances, coords):  
            chair.coordinates = coord
        
    def load_tables(self):
        coords = self.read_coords('assets/table_coords.txt')
        for i in range(1, len(coords) + 1):
            table = Table(i)
            Table.instances.append(table)
        for table, coord in zip(Table.instances, coords):  
            table.coordinates = coord

    def read_coords(self, filepath):
        coords = []
        with open(filepath, 'r') as file:
            lines = file.readlines()
            for line in lines:
                coord = list(map(int, line.strip().strip('[]').split(',')))
                coords.append(coord)
        return coords