from imports import *
from constants import *

class Gui:
    def __init__(self,widgets: dict[tk.Widget,typing.Callable],size=(SCREEN_WIDTH,SCREEN_HEIGHT),title="tk",load=False) -> None:
        '''Pass in a dict of widgets and the function to place them (grid, pack or place), and optionally the screen size (x,y) and the title of the window, then you can load or unload this gui at once.
        Setting "load" to True makes the GUI load on initialization.'''
        self.widgets = widgets
        if len(widgets) == 0:
            self.window = -1
        else:
            self.window: tk.Tk = list(widgets.keys())[0].winfo_toplevel()
        self.screen_size = size
        self.win_title = title
        if load:
            self.load()
    def load(self):
        self.window.title(self.win_title)
        self.window.geometry("x".join(map(str,self.screen_size)))
        if self.window == -1:
            return
        for w in self.widgets.keys():
            self.widgets[w]()
    def unload(self):
        if self.window == -1:
            return
        for w in self.widgets.keys():
            try:
                w.pack_forget()
            except Exception:
                try:
                    w.place_forget()
                except Exception:
                    w.grid_forget()
