import tkinter as tk
from models.chair import Chair
from renderer import Renderer
from loader import Loader
from database import db_api, db_syncer

class App:
    def __init__(self) -> None:
        # config
        self.root = tk.Tk()
        self.root.title("ijustwantaseat")
        self.root.state("zoomed")

        # initialization
        self.loader = Loader()
        self.renderer = Renderer(self.root)
        self.db_syncer = db_syncer
        db_syncer.seed_db()
        db_syncer.sync() # listens for changes does not loop
        self.loop(1000, self.renderer.loops)

        # start app
        self.root.mainloop()

    def loop(self, interval, *functions):
        for function in functions:
            function()
        self.root.after(interval, lambda: self.loop(interval, *functions))
