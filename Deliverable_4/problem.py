import tkinter as tk
from tkinter import ttk, font,  Tk, Label, Button, Entry,\
                    StringVar, DISABLED, NORMAL, END, W, E
from tkinter.messagebox import showinfo
import database_api as db
from assignments import *
from gui_skeleton import *

APP_HIGHLIGHT_FONT = ("Helvetica", 14, "bold")
REGULAR_FONT = ("Helvetica", 12, "normal")
TITLE_FONT = ("Helvetica", 14, "normal")
NICE_BLUE = "#3399FF"
HOME_FONT = ("Comic Sans", 26, "bold")

conn = sqlite3.connect('ace.db')

class Problem():
    '''
    A problem object which is used to interact with problems' data,
    and perform actions that affect problems' data
    '''
    def __init__(self, qid):
        '''
        qid is the problem id of the student we want to create
        '''
        # get problem details from database
        problem = db.get_problem_details(conn, qid)[0]
        # assign corresponding values to variables
        self.qid = problem[0]
        self.subject = problem[1]
        self.question = problem[2]
        self.answer = problem[3]
        
    # getters and setters
    def get_qid(self):
        return self.qid
    def get_subject(self):
        return self.subject      
    def get_question(self):
        return self.question
    def get_answer(self):
        return self.answer
    

class ProblemInterface(GUISkeleton):
    '''
    Objects of this type are used to genereate the GUI for the problem Database
    Management screen
    '''
    def __init__(self, parent, controller):
        GUISkeleton.__init__(self, parent)
        self.cont = controller
        self.labels = ["Subject", "Question", "Answer"]
        # label at top of the frame
        title = self.create_label(self, "Problem Database Management\n",
                                  TITLE_FONT,
                                  "Red").grid(row=0, column=1, pady=10)
        # dictionaries to contain the widgets and associate widget to
        # correspondin problem id
        self.subjects = {}
        self.questions = {}
        self.answers = {}
        # the buttons
        self.updates = {}
        self.deletes = {}
        
        # the 3 static lables that are always there
        i = 0
        for label in self.labels:
            new_label = self.create_label(self, label, REGULAR_FONT,
                                          NICE_BLUE).grid(row=1, column=i)
            # create first row of entries for add_problem function
            # set everything nicely on the grid
            new_entry = self.create_entry(self, label,
                                          REGULAR_FONT).grid(row=2, column=i)
            i += 1
        # create add problem button
        add_problem_button = self.create_button(self, "Add problem")
        add_problem_button.grid(row=2, column=3)
        back_button = self.create_button(self, "Back")
        # set button method to add_problem
        add_problem_button.config(command=lambda : self.add_problem())
        back_button["command"] = lambda: controller.show_frame('HomeScreen')
        back_button.grid(row=0, column=3)
        
        # generate all the dynamically generated widget rows
        self.gen_rows()
        
        # enable clicking functionality for all the buttons
        self.enable_buttons()
        
          
        
    def gen_rows(self):
        # get a list of all the problem ids in the database
        ids = db.get_problem_ids(conn)
        # set iterator for grid rows
        i = 0
        # for each id create a row
        for qid in ids:
            # create new entries 
            subject_entry = ttk.Entry(self, font=REGULAR_FONT)
            question_entry = ttk.Entry(self, font=REGULAR_FONT)
            answer_entry = ttk.Entry(self, font=REGULAR_FONT)
            # add to corresponding dictonaries with problem ids as keys
            self.subjects[qid] = subject_entry
            self.questions[qid] = question_entry    
            self.answers[qid] = answer_entry
          
            # create new buttons
            update_button = ttk.Button(self, text="Update")
            delete_button = ttk.Button(self, text="Delete")
            # add to corresponding dictonaries with problem ids as keys        
            self.deletes[qid] = delete_button
            self.updates[qid] = update_button
            
            # set everything nicely on the grid using an iterator i
            subject_entry.grid(row=i+3, column=0)
            question_entry.grid(row=i+3, column=1)
            answer_entry.grid(row=i+3, column=2)
            update_button.grid(row=i+3, column=3)
            delete_button.grid(row=i+3, column=4)
            i += 1
            
            # create new problem object to contain problem info
            problem = Problem(qid)
            # set each entry with the corresponding value from the problem object
            subject_entry.insert(0, problem.get_subject())
            question_entry.insert(0, problem.get_question())
            answer_entry.insert(0, problem.get_answer())
            
        
            
    def del_problem(self, button):
        '''
        delete a problem from the database and show a success popup
        '''
        # remove problem from databse
        db.remove_problem(button, conn)
        
        self.refresh()
        
        # show popup
        showinfo("Success", "problem #" + str(button) + " has been deleted")
    
    def up_problem(self, button):
        '''
        delete a problem details in the database and show a success popup
        '''        
        # get new parameters from entry widgets in the dictionaries
        new_subject = self.subjects[button].get()
        new_question = self.questions[button].get()
        new_answer = self.answers[button].get()
        # update the database with new entries
        db.update_problem_subject(button, new_subject, conn)
        db.update_problem_question(button, new_question, conn)
        db.update_problem_answer(button, new_answer, conn)
        
        self.refresh()
        
        # show popup
        showinfo("Success", "problem #" + str(button) + " has been updated")
        
    def add_problem(self):
        '''
        delete a problem from the database and show a success popup
        '''
        # get new parameters from entry widgets in the dictionaries
        new_subject = self.entry_fields["Subject"] .get()
        new_question = self.entry_fields["Question"].get()
        new_answer = self.entry_fields["Answer"].get()        
        # add new problem to databse and save his id number
        qid = db.add_problem(new_subject, new_question, new_answer, conn)
        # show popup
        self.refresh()
        # clear entries
        self.entry_fields["Subject"].set('')
        self.entry_fields["Question"].set('')
        self.entry_fields["Answer"].set('')      
        showinfo("Success", "problem #" + str(qid) + " has been added to database")

    def refresh(self):
        for subject in list(self.subjects.items()):
            subject[1].destroy()
        for question in list(self.questions.items()):
            question[1].destroy()
        for answer in list(self.answers.items()):
            answer[1].destroy()
        for update in list(self.updates.items()):
            update[1].destroy()
        for delete in list(self.deletes.items()):
            delete[1].destroy()
        self.gen_rows()
        self.enable_buttons()
        
    def enable_buttons(self):
        # get a list of all existing problem ids
        problem_ids = db.get_problem_ids(conn)        
        # configure clicking function for all the delete buttons
        for qid in problem_ids:
            self.deletes[qid].config(command=lambda j=qid: self.del_problem(j))
        # configure clicking function for all the update buttons
        for qid in problem_ids:
            self.updates[qid].config(command=lambda j=qid: self.up_problem(j))