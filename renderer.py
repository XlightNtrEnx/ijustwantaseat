import tkinter as tk
from models.chair import Chair
from database import db_api
from models.table import Table

class Renderer:
    def __init__(self, root, width=733+400, height=460):
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
        self.render_legend()

    def render_chairs(self):
        for chair in Chair.instances:
            if hasattr(chair, 'canvas_id'):
                self.canvas.delete(chair.canvas_id)
            if hasattr(chair, 'coordinates'):
                x1, y1, x2, y2 = chair.coordinates
                x1 = x1 + 200
                #y1 = y1 + 200
                x2 = x2 + 200
                #y2 = y2 + 200
                if chair.sociable:
                    id = self.create_rainbow_rectangle(x1, y1, x2, y2)
                    chair.canvas_id = id
                else: 
                    fill = '#0099E5' if chair.reserved else ('#FF4C4C' if chair.occupied else '#34BF49')
                    id = self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill)
                    chair.canvas_id = id

    def render_tables(self):
        for table in Table.instances:
            if hasattr(table, 'coordinates'):
                x1, y1, x2, y2 = table.coordinates
                x1 = x1 + 200
                #y1 = y1 + 200
                x2 = x2 + 200
                #y2 = y2 + 200
                id = self.canvas.create_rectangle(x1, y1, x2, y2, fill='#EBE3D8')
                table.canvas_id = id

    def render_legend(self):
        id_1 = self.canvas.create_rectangle(733+250, 2, 833+238, 2+10+10+60+10, fill='')
        id_2 = self.canvas.create_rectangle(733+250+5, 2+10, 733+250+10+10, 2+10+10, fill='#34BF49')
        id_3 = self.canvas.create_rectangle(733+250+5, 2+10+20, 733+250+10+10, 2+10+10+20, fill='#FF4C4C')
        id_4 = self.canvas.create_rectangle(733+250+5, 2+10+40, 733+250+10+10, 2+10+10+40, fill='#0099E5')
        id_5 = self.create_rainbow_rectangle(733+250+5, 2+10+60, 733+250+10+10, 2+10+10+60)
        self.canvas.create_text(733+250+30, 2+10+5, text="Available", anchor="w")
        self.canvas.create_text(733+250+30, 2+10+20+5, text="Occupied", anchor="w")
        self.canvas.create_text(733+250+30, 2+10+40+5, text="Reserved", anchor="w")
        self.canvas.create_text(733+250+30, 2+10+60+5, text="Sociable", anchor="w")
        
                
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

    def create_rainbow_rectangle(self, x1, y1, x2, y2):
        colors = ['#FF0000', '#FF7F00', '#FFFF00', '#00FF00', '#0000FF', '#4B0082', '#8B00FF']  # Rainbow colors
        rectangle_width = (x2 - x1) / len(colors)

        for i, color in enumerate(colors):
            rect_x1 = x1 + i * rectangle_width
            rect_x2 = rect_x1 + rectangle_width
            self.canvas.create_rectangle(rect_x1, y1, rect_x2, y2, fill=color)
    
    def loops(self):
        # TODO: optimize this such that only the chairs that have changed are re-rendered
        self.render_chairs()