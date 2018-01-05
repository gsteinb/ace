import tkinter as tk
from tkinter import ttk, font,  Tk, Label, Button, Entry,\
                    StringVar, DISABLED, NORMAL, END, W, E
from tkinter.messagebox import showinfo
import database_api as db
from assignments import *
from gui_skeleton import *
from problem import *
import ast


APP_HIGHLIGHT_FONT = ("Helvetica", 14, "bold")
REGULAR_FONT = ("Helvetica", 12, "normal")
TITLE_FONT = ("Helvetica", 14, "normal")
NICE_BLUE = "#3399FF"
HOME_FONT = ("Comic Sans", 26, "bold")

conn = sqlite3.connect('ace.db')
    

class Attempt(GUISkeleton):
    '''
    Objects of this type are used to genereate the GUI for the problem Database
    Management screen
    '''
    def __init__(self, parent, controller, uid=None, aid=None):
        GUISkeleton.__init__(self, parent)
        self.cont = controller
        self.labels = ["Subject", "Question", "Answer"]
        # dictionaries to contain the widgets and associate widget to
        # correspondin problem id
        self.entries = []
        self.labels = []
        

        back_button = self.create_button(self, "Back")
        back_button["command"] = lambda: self.refresh()
        back_button.grid(row=0, column=3)
        
        
        # enable clicking functionality for all the buttons
        # self.enable_buttons()
        
    def set_uid(self, uid, aid=None):
        self.uid = uid
        if (aid):
            self.aid = aid
            # label at top of the frame
        title = self.create_label(self, "A"+str(aid)+" Attempt",
                                  TITLE_FONT,
                                  "Red").grid(row=0, column=1, pady=10)            
        self.gen_rows()
           
        Label(self, text="Problem", font=REGULAR_FONT).grid(row=1,column=0, pady=10)
        Label(self, text="Solution", font=REGULAR_FONT).grid(row=1,column=1, pady=10)
        
    def gen_rows(self):
        # get a list of all the problem ids for the user for that assignment
        ids = db.get_user_first_attempt(self.aid, self.uid, conn)[1]
        # set iterator for grid rows
        ids = ast.literal_eval(ids)
        # for each id create a row
        i = 0
        for qid in ids:
            # create new entries 
            question_label = Label(self, font=REGULAR_FONT)
            answer_entry = Entry(self, font=REGULAR_FONT)
            self.labels.append(question_label)
            self.entries.append(answer_entry)
            # add to corresponding dictonaries with problem ids as keys
            # self.subjects[qid] = subject_entry
            # self.questions[qid] = question_entry
            # self.answers[qid] = answer_entry
          
            
            # set everything nicely on the grid using an iterator i
            question_label.grid(row=i+3, column=0)
            answer_entry.grid(row=i+3, column=1)
            i += 1
            
            # set each entry with the corresponding value from the problem object
            question_label.config(text=db.get_problem_details(conn, qid)[0][2])
    
            
    def refresh(self):
        for i in self.entries:
            i.destroy()
        for j in self.labels:
            j.destroy()
        self.cont.show_frame('ViewUserAssignments', self.uid)
        
    """       
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


        
    def enable_buttons(self):
        # get a list of all existing problem ids
        problem_ids = db.get_problem_ids(conn)        
        # configure clicking function for all the delete buttons
        for qid in problem_ids:
            self.deletes[qid].config(command=lambda j=qid: self.del_problem(j))
        # configure clicking function for all the update buttons
        for qid in problem_ids:
            self.updates[qid].config(command=lambda j=qid: self.up_problem(j))
    """
