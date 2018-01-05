import tkinter as tk
from tkinter import ttk, font,  Tk, Label, Button, Entry,\
                    StringVar, DISABLED, NORMAL, END, W, E
from tkinter.messagebox import showinfo
import database_api as db
import sqlite3
from user import *
from main import *
from random import sample

conn = sqlite3.connect('ace.db')

APP_HIGHLIGHT_FONT = ("Helvetica", 14, "bold")
REGULAR_FONT = ("Helvetica", 12, "normal")
TITLE_FONT = ("Helvetica", 14, "normal")
NICE_BLUE = "#3399FF"
HOME_FONT = ("Comic Sans", 26, "bold")


class AddAssignment(GUISkeleton):
    '''
    Window used to input details about an assignment and generate a new assignment
    based on those details
    '''
    def __init__(self, parent, controller):
        GUISkeleton.__init__(self, parent)
        self.cont = controller
        self.row_counter = 0
        self.pairs = {}
        # init lists for labels
        self.subjs = []
        self.nums = []
        # init formula holder
        self.formula = ""        
        
        # label at top of the frame
        ttk.Label(self, text="Add Assignment Menu\n",
                             font=TITLE_FONT, foreground="red").grid(
                                 row=self.row_counter, column=1, pady=10)
        # increment current row counter
        self.row_counter += 1
        
        # set form labels and entries, while keeping track on current line
        self.name_label = Label(self, text="Assignment Name:\n",
                             font=REGULAR_FONT, foreground=NICE_BLUE)
        self.name_label.grid(row=self.row_counter, column=0)
        self.name_entry = Entry(self)
        self.name_entry.grid(row=self.row_counter, column=1)        
        self.row_counter += 1           
        
        self.deadline_label = Label(self, text="Deadline:\n(dd/mm/yyyy)",
                             font=REGULAR_FONT, foreground=NICE_BLUE)
        self.deadline_label.grid(row=self.row_counter, column=0)
        self.deadline_entry = Entry(self)
        self.deadline_entry.grid(row=self.row_counter, column=1)
        self.row_counter += 1
        
        self.visible_label = Label(self, text="Visible:\n(0 or 1)\n",
                             font=REGULAR_FONT, foreground=NICE_BLUE)
        self.visible_label.grid(row=self.row_counter, column=0)
        self.visible_entry = Entry(self)
        self.visible_entry.grid(row=self.row_counter, column=1)        
        self.row_counter += 1
         
        self.subj_label = Label(self, text="Subject:",
                             font=REGULAR_FONT, foreground=NICE_BLUE)
        self.subj_label.grid(row=self.row_counter, column=0)
        self.num_quests_label = Label(self, text="# Of Questions:",                        font=REGULAR_FONT, foreground=NICE_BLUE)
        self.num_quests_label.grid(row=self.row_counter, column=1)
        self.row_counter += 1
        
        self.subj_entry = Entry(self)
        self.subj_entry.grid(row=self.row_counter, column=0)
        
        self.num_quests_entry = Entry(self)
        self.num_quests_entry.grid(row=self.row_counter, column=1)        
        
        # add and place the buttons
        self.add_button = Button(self, text="Add Subject", font=REGULAR_FONT, 
                                 command=lambda :
                                 self.gen_row(self.subj_entry.get(),
                                              self.num_quests_entry.get()))
        self.add_button.grid(row=self.row_counter, column=2) 
        self.done_button = Button(self, text="Done", font=REGULAR_FONT,
                                  command=self.done)
        self.done_button.grid(row=self.row_counter, column=3)  
        self.done_button = Button(self, text="Back", font=REGULAR_FONT,
                                  command=lambda :
                                 self.cont.show_frame('HomeScreen'))
        self.done_button.grid(row=self.row_counter, column=4)          
        self.row_counter += 1 
        
    def refresh(self):
        self.name_entry.delete(0, END)
        self.deadline_entry.delete(0, END)
        self.visible_entry.delete(0, END)
        self.subj_entry.delete(0, END)
        self.num_quests_entry.delete(0, END)
        
        for subj in self.subjs:
            subj.destroy()
        for num in self.nums:
            num.destroy()
            
        self.formula = ""
        self.pairs = {}
        
    def gen_row(self, subj, num_quests):
        '''
        takes a subject a number of questions from that subject, add these
        to a dictionary to keep track, and displays a line in the gui with
        these details.
        '''
        # create a subj label, add to list of labels, and fill with details
        subj_label = Label(self, text=subj,
                         font=REGULAR_FONT, foreground="black")
        subj_label.grid(row=self.row_counter, column=0)
        self.subjs.append(subj_label)
        # create a #q's label, add to list of labels, and fill with details
        num_quests_label = Label(self, text=num_quests,
                         font=REGULAR_FONT, foreground="black")
        num_quests_label.grid(row=self.row_counter, column=1)
        self.nums.append(num_quests_label)
        
        # create a dictinary pair
        self.pairs[subj] = num_quests
        # increment current row counter
        self.row_counter += 1  
        
        self.subj_entry.delete(0, END)
        self.num_quests_entry.delete(0, END) 
        
        
            
    def create_formula(self):
        '''
        create the formula with the format " subj1:#1q's, subj2:#q's2... "
        based on the text from the labels in the list, and the numbers from
        the labels in the other list
        '''
        # append pairs to formula for each pair
        for pair in self.pairs.items():
            self.formula += str(pair[0]) + ":" + str(pair[1]) + ","
            
        self.formula = self.formula[:-1]

    def update_assignments_table(self):
        ''' 
        insert a new row to the assignments table with the details
        '''
        num = db.add_assignment(self.name_entry.get(), self.formula, 
                          self.deadline_entry.get(), self.visible_entry.get(), conn)
        # return id of new assignment
        return num
        
    def done(self):
        '''
        create formula, update table, 
        create new assignment table->add row for each user
        '''
        self.create_formula()
        num = self.update_assignments_table()
        # create the assignment table with it's proper name in the format: a#
        db.create_assignment_table(num, conn)
        
        # get a list of currently existing user ids in the system
        ids = db.get_user_ids(conn)
        
        # for each user id, create a first attempt entry using a unique set 
        # of questions
        for uid in ids:
            # unique set of questions
            quests = self.create_problem_set(self.formula)
            # ectract a list of problem ids
            prob_ids = []
            # add all ids to the list
            for quest in quests:
                prob_ids.append(quest[0])   
            # create the user attempt entry
            db.add_attempt("a"+str(num), uid, prob_ids, conn)
            
        
        self.refresh()
        
        
    def create_problem_set(self, formula):
        '''
        takes a formula "subj1:num1,subj2:num2..." , creates a unique set
        of problems set according to the formula
        '''
        problem_set = []
        pairs = {}
        # separate the string to pairs, break at the ","
        str_pairs = formula.split(",")
        # for each pair , split at the ":" and add to dictionary
        for pair in str_pairs:
            p = pair.split(":")
            pairs[p[0]] = p[1]
        # for each pair in the dictionary:
        for item in pairs.items():
            # get a list of the problems with the same subject
            rows = db.get_problems_by_subj(item[0], conn)
            # get a sample space of random rows with the right amount of problems
            sample_rows = sample(rows, int(item[1]))
            # add subj sample rows to problem_set
            problem_set += sample_rows
            
        return problem_set
