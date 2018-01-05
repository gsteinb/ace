import tkinter as tk
from tkinter import ttk, font,  Tk, Label, Button, Entry,\
                    StringVar, DISABLED, NORMAL, END, W, E
from tkinter.messagebox import showinfo
import database_api as db
from assignments import *
from gui_skeleton import *
from problem import *
from user import *
import ast
import datetime

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

from main import *

#import matplotlib
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
#from matplotlib.figure import Figure
#matplotlib.use("TkAgg")

YRSEC = 31556952
MONSEC = 2629746
DAYSEC = 86400
HRSEC = 3600
MINSEC = 60

APP_HIGHLIGHT_FONT = ("Helvetica", 14, "bold")
REGULAR_FONT = ("Helvetica", 12, "normal")
TITLE_FONT = ("Helvetica", 16, "normal")
NICE_BLUE = "#3399FF"
HOME_FONT = ("Comic Sans", 26, "bold")

conn = sqlite3.connect('ace.db')

class Leaderboard(GUISkeleton):
    '''
    Objects of this type are used to generate the GUI displaying a leaderboard
    '''
    def __init__(self, parent, controller, uid=None):
        GUISkeleton.__init__(self, parent)
        self.cont = controller

        self.labels = ["Rank", "UID", "Grade", "Time (Day - H:M:S)"]
        
        '''initiate the buttons on the screen'''
        new_frame = ttk.Frame(self)
        #screen title
        self.create_label(new_frame, "Leaderboard",
                              TITLE_FONT, "Red").pack(side="left", padx=40)	
        #back button
        back_button = self.create_button(new_frame, "Back")
        back_button["command"] = lambda : controller.show_frame(self.x, self.uid)
        back_button.pack(side="right", padx=10)
        new_frame.grid(row=0, column=0, pady=20, sticky="E", columnspan=3)
        
        # dictionaries to contain the widgets and associate widget to
        # corresponding user id
        self.names = {}

        self.grades = {}
        self.times = {}
        
        # the 3 static lables that are always there
        i = 0
        for label in self.labels:
            new_label = self.create_label(self, label, APP_HIGHLIGHT_FONT,
                                          NICE_BLUE).grid(row=1, column=i)
            # create first row of entries for add_problem function
            # set everything nicely on the grid
            # create first row of entries for add_user function
            # set everything nicely on the grid
            i += 1



        # generate all the dynamically generaterd widget rows
        self.gen_rows()

        # enable clicking functionality for all the buttons
        self.enable_buttons()

    def set_back(self, x):
        self.x = x


    def gen_rows(self):
        # get a list of all the user ids in the database
        ids = db.get_user_by_grade(conn)

        # Setup graph
        x_ax = []
        y_ax = []

        # set iterator for grid rows
        i = 0
        # for each id create a row
        for uid in ids:
            # create new entries
            user = db.get_user_details(conn, uid)
            rank_label = self.create_label(self, text=i+1, font=REGULAR_FONT)
            name_label = self.create_label(self, text=user[0][0], font=REGULAR_FONT)            
            grade_label = self.create_label(self, text=str(user[0][5]) + "%", font=REGULAR_FONT)
            time_label = self.create_label(self, text=self.datetimeFormat(user[0][6]), font=REGULAR_FONT)
            # add to corresponding dictonaries with user ids as keys
            self.names[uid] = name_label
            self.grades[uid] = grade_label
            self.times[uid] = time_label

            # set everything nicely on the grid using an iterator i
            rank_label.grid(row=i+3, column=0)
            name_label.grid(row=i+3, column=1)
            grade_label.grid(row=i+3, column=2)
            time_label.grid(row=i+3, column=3)
        

            # Append for graph
            x_ax.append(str(i) + "\n" + str(user[0][2]))
            y_ax.append(user[0][5])
            i+=1

        fig = Figure(figsize=(5,6), dpi=60)
        graph = fig.add_subplot(111)
        graph.set_title("Leaderboard Graph")
        graph.set_xlabel("Rank with name")
        graph.set_ylabel("Grade in %")
        graph.plot(x_ax, y_ax)

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.get_tk_widget().grid(row=i+4, column=0, columnspan=4)
        canvas._tkcanvas.grid(row=0, column=5, columnspan=4, rowspan=45,padx=15, pady=20)


    def refresh(self):
        for name in list(self.names.items()):
            name[1].destroy()

        for grade in list(self.grades.items()):
            grade[1].destroy()
        for time in list(self.times.items()):
            time[1].destroy()
 
        self.gen_rows()
        self.enable_buttons()

    def enable_buttons(self):
        # get a list of all existing user ids
        user_ids = db.get_user_ids(conn)

    def datetimeFormat(self, input_sec):
        """
        Returns inputted seconds in the following format:
        "Day - Hour:Minute:Second"
        """
        day = input_sec // DAYSEC
        hour = (input_sec % DAYSEC) // HRSEC
        minute = ((input_sec % DAYSEC) % HRSEC) // MINSEC
        sec = ((input_sec % DAYSEC) % HRSEC) % MINSEC
        return str(day) + " - " + str(hour) + ":" + str(minute) + ":" + str(sec)
