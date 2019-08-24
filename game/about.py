import os
from tkinter import Toplevel, Label, LEFT, Button, W, SE, PhotoImage, Frame

# Next two lines are an evil hack to let me get a folder
# from the parent folder, even though I start at root.
# I must be doing something wrong.
import sys
sys.path.append(".")

from _version import __version__

class About:
    def __init__(self, parent):
        pad_px = 5
        self.top = Toplevel(parent)
        self.top.title('About:')
        self.top.grab_set() # Make the window modal

        label_title = Label(self.top, text='Minesweeper')
        label_title['font'] = 'Helvetica 16 bold'
        label_title.pack()
        file_path = os.path.dirname(os.path.realpath(__file__))        

        grid_middle = Frame(self.top)

        logo = PhotoImage(file=os.path.join(file_path, '../res/logo.gif'))
        label_logo = Label(grid_middle, image=logo)
        label_logo.image = logo # don't garbage collect me please.
        label_logo.grid(row=0, column=1, rowspan=2)
        
        label_description = Label(grid_middle,justify=LEFT, text = 'Use your deductive powers to figure out where the mines are on the grid.\nYou lose if you step on a mine.\nTo win you must open every square except for the mines.')
        label_description.grid(row=0, column=0)

        label_version = Label(grid_middle, justify=LEFT, text = 'Version: ' + __version__)
        label_version.grid(row=1, column=0, sticky='W')
        grid_middle.pack()

        button_ok = Button(self.top, text='OK', command = self.ok)
        button_ok.pack(padx=pad_px, pady=pad_px * 2, anchor=SE)

        self.top.resizable(False, False)
    
    def ok(self):
        # Close the dialog
        self.top.destroy()
