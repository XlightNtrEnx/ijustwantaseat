import tkinter as tk
from models.chair import Chair
from database import db_api
from models.table import Table

class Renderer:
    def __init__(self, root, width=733, height=460):
        self.root = root
        
        self.heading_label = tk.Label(root, text="Seat Map of SUTD canteen", font=("Calibri", 20))
        self.heading_label.pack(pady=20)
        
        self.canvas = tk.Canvas(root, width=width, height=height)
        self.canvas.pack()
        
        self.center_ui()
        
        self.initial_render()

    def initial_render(self):
        self.render_chairs()
        self.render_tables()

    def render_chairs(self):
        for chair in Chair.instances:
            if hasattr(chair, 'canvas_id'):
                self.canvas.delete(chair.canvas_id)
            if hasattr(chair, 'coordinates'):
                x1, y1, x2, y2 = chair.coordinates
                fill = '#0099E5' if chair.reserved else ('#FF4C4C' if chair.occupied else '#34BF49')
                id = self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill)
                chair.canvas_id = id

    def render_tables(self):
        for table in Table.instances:
            if hasattr(table, 'coordinates'):
                x1, y1, x2, y2 = table.coordinates
                id = self.canvas.create_rectangle(x1, y1, x2, y2, fill='#EBE3D8')
                table.canvas_id = id
                
    def center_ui(self):
        # Get the screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate the position to center the UI
        canvas_width = self.canvas.winfo_reqwidth()
        canvas_height = self.canvas.winfo_reqheight()
        x = (screen_width - canvas_width) // 2
        y = (screen_height - canvas_height - self.heading_label.winfo_reqheight()) // 2

        # Place the canvas and heading label at the centered position
        self.canvas.place(x=x, y=y)
        self.heading_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
    
    def loops(self):
        # TODO: optimize this such that only the chairs that have changed are re-rendered
        self.render_chairs()