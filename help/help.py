import os
import json
import webbrowser
from tkinter import Listbox, Toplevel, scrolledtext, WORD
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
        file_path = os.path.join(path, 'index.json')     
        f = open(file_path, 'rt')
        self.files = json.loads(f.read())
        for counter, entry in enumerate(self.files['files']):
            self.list.insert(counter, entry['name'])
        f.close()
    
    def list_click(self, event):
        index = self.list.curselection()[0]
        item = self.files['files'][index]
        path = os.path.dirname(os.path.realpath(__file__))   
        fileName = os.path.normpath(os.path.join(path, item['fileName']))
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
            fileName = os.path.normpath(os.path.join(path, url))
            self.render_file(fileName)
