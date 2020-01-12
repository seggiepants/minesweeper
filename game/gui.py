import os
from functools import reduce, partial
from tkinter import Tk, Label, Frame, Menu, PhotoImage, IntVar
from tkinter.messagebox import showinfo
import game.settings as settings
from game.about import About
from game.grid import Grid, GameState
from game.cell import Cell, State

class GameWindow(object):

    def __init__(self):        
        pass

    def open(self, col, row, event):
        self.grid.open(col, row)
        self.redraw_grid()

    def toggle_flagged(self, col, row, event):
        self.grid.toggle_flagged(col, row)
        self.redraw_cell(col, row)
    
    def init_icons(self):
        file_path = os.path.dirname(os.path.realpath(__file__))
        self.icons = {}
        for i in range(1, 9):
            self.icons[i] = PhotoImage(file=os.path.join(file_path, f'../res/{i}.ppm'))
        self.icons['blank'] = PhotoImage(file=os.path.join(file_path, '../res/blank.ppm'))
        self.icons['bomb'] = PhotoImage(file=os.path.join(file_path, '../res/bomb.ppm'))
        self.icons['default'] = PhotoImage(file=os.path.join(file_path, '../res/default.ppm'))
        self.icons['flagged'] = PhotoImage(file=os.path.join(file_path, '../res/flagged.ppm'))
        self.icons['logo'] = PhotoImage(file=os.path.join(file_path, '../res/logo.gif'))        

    def redraw_grid(self):
        for j in range(self.grid.height):
            for i in range(self.grid.width):
                self.redraw_cell(i, j)
    
    def redraw_cell(self, col, row):
        cell = self.grid_frame.nametowidget(f'cell_{col}_{row}')
        if self.grid.get(col, row).state == State.FLAGGED:
            icon = self.icons['flagged']
        elif self.grid.get(col, row).state == State.DEFAULT:
            icon = self.icons['default']
        else:
            bomb_count = self.grid.get_bomb_count(col, row)
            icon = self.icons['blank']
            if self.grid.get(col, row).is_bomb:
                icon = self.icons['bomb']
            elif bomb_count >= 1 and bomb_count <= 8:
                icon = self.icons[bomb_count]
        cell.config(image=icon)
    
    def show_about(self):
        dialog = About(self.root)
        self.root.wait_window(dialog.top)

    
    def change_difficulty(self):        
        self.grid = Grid(self.current_difficulty['width'], self.current_difficulty['height'])
        self.grid.seed_grid(self.current_difficulty['bombs'])

        icon = self.icons['default']
        for j in range(self.grid.height):
            for i in range(self.grid.width):
                cell = Label(self.grid_frame, width=icon.width(), height=icon.height(), borderwidth=0, image=icon, name=f'cell_{i}_{j}')
                cell.bind('<Button-1>', partial(self.open, i, j))
                cell.bind('<Button-3>', partial(self.toggle_flagged, i, j))
                cell.grid(column = i, row = j, ipadx = 0, ipady = 0, padx = 0, pady=0)
        
        self.redraw_grid()
    
    def menu_change_difficulty(self):        
        widgets = self.grid_frame.grid_slaves()
        for widget in widgets:
            widget.destroy()

        self.current_difficulty = settings.storage["difficulty"][self.difficulty_idx.get()]
        settings.storage["default_difficulty"] = self.current_difficulty["name"]
        self.change_difficulty()
    
    def not_yet_implemented(self):
        showinfo('OK', 'This has not yet been implemented.')

    def build_gui(self):
        self.root = Tk()

        main_menu = Menu(self.root)
        game_menu = Menu(main_menu, tearoff=0)
        game_menu.add_command(label='New Game', command=self.menu_change_difficulty)
        game_menu.add_separator()
        game_menu.add_command(label='Exit', command=self.root.quit)
        main_menu.add_cascade(label='Game', menu=game_menu)

        self.difficulty_idx = IntVar()
        difficulty_menu = Menu(main_menu, tearoff = 0)
        for idx, item in enumerate(settings.storage['difficulty']):
            #difficulty_menu.add_radiobutton(label=item['name'], variable=self.current_difficulty, value=item, command=self.not_yet_implemented)
            difficulty_menu.add_radiobutton(label=item['name'], variable=self.difficulty_idx, value=idx, indicatoron=1, command=self.menu_change_difficulty)
            if item == self.current_difficulty:
                self.difficulty_idx.set(idx)
                print(f'Set Difficulty Index = {idx}')
        
        main_menu.add_cascade(label='Difficulty', menu=difficulty_menu)

        help_menu = Menu(main_menu, tearoff=0)
        help_menu.add_command(label='About', command=self.show_about)
        main_menu.add_cascade(label='Help', menu=help_menu)

        self.root.config(menu=main_menu)
        self.root.title('Minesweeper')

        self.init_icons()
        self.grid_frame = Frame()
        self.grid_frame.pack()

        self.change_difficulty()

        file_path = os.path.dirname(os.path.realpath(__file__))        
        icon = PhotoImage(file=os.path.join(file_path, '../res/logo.gif'))
        self.root.icon = icon # don't garbage collect me please.
        #self.icons['logo'] = icon
        self.root.tk.call('wm', 'iconphoto', self.root._w, self.icons['logo'])

    def run_game(self, default_difficulty):
        self.current_difficulty = reduce(lambda x, y: x if x['name'] == settings.storage['default_difficulty'] else y, settings.storage['difficulty'], settings.storage['difficulty'][0])
        self.build_gui()
        self.root.mainloop()
