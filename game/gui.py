import os
import webbrowser
from functools import reduce, partial
import json
from tkinter import Tk, Label, Listbox, Frame, Menu, PhotoImage, IntVar, Toplevel, scrolledtext, WORD
from tkinter.messagebox import showinfo
import game.settings as settings
from game.about import About
from game.grid import Grid, GameState
from game.cell import Cell, State
from markdown.MarkdownParser import MarkdownParser
from markdown.MarkdownRenderTk import MarkdownRenderTk

class HelpWindow(Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.root = master
        self.title = 'Help'
        self.list = Listbox(self)
        self.list.pack(side="left", fill="y")
        self.text = scrolledtext.ScrolledText(self, wrap = WORD)
        self.text.pack(side="right", fill="both", expand=True)
        self.images = []    
        self.load_list()
        self.list.bind('<<ListboxSelect>>', self.list_click)
        self.list.select_set(0)
        self.list_click(None)
            
    
    def load_list(self):
        self.files = {}

        path = os.path.dirname(os.path.realpath(__file__))   
        file_path = os.path.join(path, '../help/index.json')     
        f = open(file_path, 'rt')
        self.files = json.loads(f.read())
        for counter, entry in enumerate(self.files['files']):
            self.list.insert(counter, entry['name'])
        f.close()
    
    def list_click(self, event):
        index = self.list.curselection()[0]
        item = self.files['files'][index]
        path = os.path.dirname(os.path.realpath(__file__))   
        fileName = os.path.normpath(os.path.join(path, '../help/', item['fileName']))
        self.render_file(fileName)

    def render_file(self, fileName):
        path = os.path.dirname(os.path.realpath(__file__))   
        f = open(os.path.join(fileName), 'rt')
        buffer = f.read()
        f.close()
        parser = MarkdownParser()
        tokens = parser.parse(buffer)
        renderer = MarkdownRenderTk(self.text)
        renderer.render(tokens, os.path.normpath(os.path.join(path, '../res')), self.images, self.link_click)


    def link_click(self, url, title):
        if (url.startswith('http:') or url.startswith('https:')):
            # Open a web browser with that link.
            webbrowser.open(url)
        else:
            # Open a markdown file.
            path = os.path.dirname(os.path.realpath(__file__))
            fileName = os.path.normpath(os.path.join(path, '../help', url))
            self.render_file(fileName)

class GameWindow(object):

    def __init__(self):        
        self.game_over = False

    def win(self):
        showinfo('You Win!', 'Congratulations, you won')
        self.game_over = True

    def lose(self):
        showinfo('You lose', 'BOOM! You stepped on a mine.\r\nYou Lost the game.')
        self.game_over = True

    def open(self, col, row, event):
        if not self.game_over:
            self.grid.open(col, row)
            self.redraw_grid()
            if self.grid.get(col, row).is_bomb:
                self.lose()
            elif self.grid.get_count_remaining_to_open() == 0:
                self.win()

    def toggle_flagged(self, col, row, event):
        if not self.game_over:
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

    def show_help(self):
        HelpWindow(self.root)

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
        self.game_over = False
    
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
        help_menu.add_command(label='Index', command=self.show_help)
        help_menu.add_separator()
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
        self.game_over = False
        self.root.mainloop()
