import tkinter as tk
from tkinter import ttk, font,  Tk, Label, Button, Entry,\
                    StringVar, DISABLED, NORMAL, END, W, E
from tkinter.messagebox import showinfo
import database_api as db

APP_HIGHLIGHT_FONT = ("Helvetica", 14, "bold")
REGULAR_FONT = ("Helvetica", 12, "normal")
NICE_BLUE = "#3399FF"

class GUISkeleton(ttk.Frame):
    '''Skeleton for creating frames in Tkinter'''
    def __init__(self, parent):
        self.entry_fields = {}
        ttk.Frame.__init__(self, parent)
        
    def create_label(self, location, text, font=None, foreground=None):
        '''creates a label the programmer will be able to assign
        this to a variable, edit the parameters, and pack to their liking'''
        label = ttk.Label(location)
        label["text"] = text
        if (font != None):
            label["font"] = font
        if (foreground != None):
            label["foreground"] = foreground
        return label
    
    def create_entry(self, location, key, font=None):
        ''' Returns an entry box that the programmer is able to pack'''
        # create an entrybox
        new_entry = ttk.Entry(location)
        if (font != None):
            new_entry["font"] = font
        # assign a stringvar to the Entry
        self.entry_fields[key] = StringVar()
        new_entry["textvariable"] = self.entry_fields[key]
        return new_entry
    
    def create_button(self, location, text):
        ''' creates a button with the wanted text that the programmer
        can customize'''
        new_button = ttk.Button(location)
        new_button["text"] = text
        return new_button   

        
    def create_empty_label(location, num):
        ''' creates an empty label with the designated number of newlines
        create_empty_label(self, 1)
        GUI: \n              <-- this is the label created
        widget
        '''
        txt = ""
        for i in range(num):
            txt += "\n"
            label = ttk.Label(location)
            label["text"] = txt
        label.pack()
        
    def set_uid(self, uid, aid=None, atid=None):
        self.uid = uid
        self.aid = aid
        self.atid = atid    

