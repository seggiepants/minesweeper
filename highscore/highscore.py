import os
from tkinter import Button, Label, OptionMenu, PhotoImage, StringVar, Toplevel, N, S, E, W, CENTER, NO
from tkinter import ttk
import game.settings as settings

class HighScore:
    def __init__(self, parent=None):
        self.root = parent
        self.top = Toplevel(parent)  
        self.top.title = 'High Scores'
        self.build_gui()
        self.top.grab_set() # Make the window modal
        path = os.path.dirname(os.path.realpath(__file__))   
        logo = PhotoImage(file=os.path.join(path, '../res/logo.gif'))
        self.top.tk.call('wm', 'iconphoto', self.top._w, logo)
        self.top.resizable(False, False)
    
    def build_gui(self):
        lbl = Label(self.top, text='Difficulty:')
        lbl.pack()
        difficulty_types = [setting['name'] for setting in settings.storage['difficulty']]
        current_difficulty = StringVar(self.top)
        current_difficulty.set(settings.storage['default_difficulty'])
        difficultyLevel = OptionMenu(self.top, current_difficulty, *difficulty_types)
        difficultyLevel.pack()
        tvw = ttk.Treeview(self.top)
        tvw['columns']=('Name', 'Time', 'Date')
        tvw.column('#0', width=0, stretch=NO)
        tvw.column('Name', anchor=CENTER, width=80)
        tvw.column('Time', anchor=CENTER, width=80)
        tvw.column('Date', anchor=CENTER, width=80)

        tvw.heading('#0', text='', anchor=CENTER)
        tvw.heading('Name', text='Name', anchor=CENTER)
        tvw.heading('Time', text='Time', anchor=CENTER)
        tvw.heading('Date', text='Date', anchor=CENTER)

        tvw.insert(parent='', index=0, id=0, text='', values=('seggiepants', 100, '1/1/1900'))
        tvw.pack()

        closeButton = Button(self.top, text='OK', command=self.ok)
        closeButton.pack()

    def ok(self):
        # Close the dialog
        self.top.destroy()        

