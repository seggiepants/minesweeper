from tkinter import Tk, Menu
from tkinter.messagebox import showinfo
from functools import partial
from game.about import About

def ShowAbout(parent):
    dialog = About(parent)
    parent.wait_window(dialog.top)

def NotYetImplemented():
    showinfo('OK', 'This has not yet been implemented.')

def BuildGUI():
    root = Tk()

    main_menu = Menu(root)
    game_menu = Menu(main_menu, tearoff=0)
    game_menu.add_command(label='New Game', command=NotYetImplemented)
    game_menu.add_separator()
    game_menu.add_command(label='Exit', command=root.quit)
    main_menu.add_cascade(label='Game', menu=game_menu)

    help_menu = Menu(main_menu, tearoff=0)
    help_menu.add_command(label='About', command=partial(ShowAbout, root))
    main_menu.add_cascade(label='Help', menu=help_menu)

    root.config(menu=main_menu)
    return root

def RunGame():
    root = BuildGUI()
    root.mainloop()
