import os
from datetime import timedelta, datetime
import time
from tkinter import Button, Entry, Label, OptionMenu, PhotoImage, StringVar, Toplevel, N, S, E, W, CENTER, NO
from tkinter import ttk
from tkinter.messagebox import *
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
        padding = 5
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

        connection_string = settings.get_db_path(settings.storage_type)
        rows = settings.get_high_scores(connection_string, current_difficulty.get(), settings.storage['high_score_count'])
        for (idx, row) in enumerate(rows):
            parameters = (row['name'], str(timedelta(seconds=row['seconds'])), row['date'].strftime('%m/%d/%Y %H:%M:%S'))
            tvw.insert(parent='', index=idx, id=idx, text='', values=parameters)
        tvw.pack()

        closeButton = Button(self.top, text='OK', command=self.ok)
        closeButton.pack(padx=padding, pady=padding)


    def ok(self):
        # Close the dialog
        self.top.destroy()        

class EnterHighScore():
    def __init__(self, difficulty, seconds, parent=None):
        self.difficulty = difficulty
        self.seconds = seconds
        self.root = parent
        self.top = Toplevel(parent)  
        self.top.title = 'Enter High Score'
        self.build_gui()
        self.top.grab_set() # Make the window modal
        path = os.path.dirname(os.path.realpath(__file__))   
        logo = PhotoImage(file=os.path.join(path, '../res/logo.gif'))
        self.top.tk.call('wm', 'iconphoto', self.top._w, logo)
        self.top.resizable(False, False)

    def build_gui(self):
        padding = 5
        message = Label(self.top, text='Congratulation you got a high score. Please enter your name.')
        message.pack()
        self.text = Entry(self.top)
        self.text.pack()
        closeButton = Button(self.top, text='OK', command=self.ok)
        closeButton.pack(padx=padding, pady=padding)

    def ok(self):
        connection_string = settings.get_db_path(settings.storage_type)
        name = self.text.get()
        if len(name.strip()) > 0:
            settings.add_high_score(connection_string, self.difficulty, name, self.seconds, datetime.now())
            self.top.destroy()
        else:
            showerror("Error", "Please enter your name", )

        

