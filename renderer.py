import tkinter as tk
from models.chair import Chair
from database import db_api
from models.table import Table

class Renderer:
    def __init__(self, root, width=730, height=460):
        self.root = root
        self.canvas = tk.Canvas(root, width=width, height=height)
        self.canvas.pack()
        self.initial_render()

    def initial_render(self):
        self.render_chairs()
        self.render_tables()

    def render_chairs(self):
        for chair in Chair.instances:
            if hasattr(chair, 'coordinates'):
                x1, y1, x2, y2 = chair.coordinates
                fill = 'blue' if chair.reserved else ('red' if chair.occupied else 'green')
                id = self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill)
                chair.canvas_id = id

    def render_tables(self):
        for table in Table.instances:
            if hasattr(table, 'coordinates'):
                x1, y1, x2, y2 = table.coordinates
                id = self.canvas.create_rectangle(x1, y1, x2, y2, fill='black')
                table.canvas_id = id
    
    def loops(self):
        # TODO: optimize this such that only the chairs that have changed are re-rendered
        self.render_chairs()