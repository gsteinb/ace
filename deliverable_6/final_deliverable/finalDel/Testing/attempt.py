import tkinter as tk
from tkinter import ttk, font,  Tk, Label, Button, Entry,\
                    StringVar, DISABLED, NORMAL, END, W, E
from tkinter.messagebox import showinfo
import database_api as db
from gui_skeleton import *
from problem import *
import ast
from random import sample
import time
import sqlite3


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
        
    def set_uid(self, uid, aid=None, atid=None):
        self.uid = uid
        self.aid = aid
        self.atid = atid
    
            # label at top of the frame
        title = self.create_label(self, "A"+str(aid)+" Attempt",
                                  TITLE_FONT,
                                  "Red").grid(row=0, column=1, pady=10)
         
         # get the existing progress for the user for the assignment
        self.existing_progress = db.get_assignment_progress_for_user(
            self.aid, self.uid, conn)
        
        self.gen_rows()
           
        Label(self, text="Problem", font=REGULAR_FONT).grid(row=1,column=0, pady=10)
        Label(self, text="Solution", font=REGULAR_FONT).grid(row=1,column=1, pady=10)
        
       
        
    def gen_rows(self):
        # get a list of all the problem ids for the user for that assignment
        ids = db.get_user_nth_attempt(self.aid, self.uid, -1, conn)[2]
        # set iterator for grid rows
        # print(db.get_user_nth_attempt(self.aid, self.uid, -1, conn)[2])
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

            # set each label with the corresponding value from the problem object
            question_label.config(text=db.get_problem_details(conn, qid)[0][2])

            # set each entry with the corresponding value from list of existing progress
            try:
                answer_entry.insert(0, self.existing_progress[i])
            except IndexError:
                print("no progress yet")
            
            i += 1
            
        # create submit and save progress buttons
        self.update_progress_button = ttk.Button(
            text="Save", command= lambda : self.update_progress())
        self.update_progress_button.pack()
        
        self.submit_button = ttk.Button(
            text="Submit", command= lambda : self.submit_progress())
        self.submit_button.pack()
                
        
        
            
    def refresh(self):
        for i in self.entries:
            i.destroy()
        for j in self.labels:
            j.destroy()
        self.update_progress_button.destroy()
        self.submit_button.destroy()
        self.entries=[]
        self.labels=[]
        self.cont.show_frame('ViewUserAssignments', self.uid)
        
        
    def get_entries(self):
        ''' 
        create a new list, iterate throgh the list of entries and
        add each text to the new list of texts, return that list
        '''
        answers = []
        for ent in self.entries:
            answers.append(ent.get())
            
        return answers
        
    def update_progress(self):
        '''
        takes a list of answers, creates a string in format:'ans1,ans2,ans3,...'
        and calles a database function to update the user's attempt row with the
        new progress
        '''
        answers = self.get_entries()
        progress = ""
        for ans in answers:
            progress += (str(ans)+',')
            
        db.update_assignment_progress_for_user(
            self.aid, self.uid, progress[:-1], conn)
        self.refresh()
        
    def submit_progress(self):
        # update progress
        answers = self.get_entries()
        progress = ""
        for ans in answers:
            progress += (str(ans)+',')
        progress = progress[:-1]
        db.update_assignment_progress_for_user_for_nth_attempt(
            self.aid, self.uid, len(db.get_user_attempts(
                    self.aid, self.uid, conn)), progress, conn)  
        
        # get problem set
        # get a list of all the problem ids for the user for that assignment
        problem_set = db.get_user_nth_attempt(self.aid, self.uid, -1, conn)[2]
        
        # get stored solutions according to the problem set
        solution_set = db.get_solution_set(problem_set ,conn)
        
        # get and update grade according to solution set
        try:
            grade = self.calc_grade(solution_set, progress)
            db.update_attempt_grade_for_user_for_nth_attempt(
                self.aid, self.uid, len(db.get_user_attempts(
                    self.aid, self.uid, conn)), grade, conn)
        except (IndexError,SyntaxError):
            print("not complete")
            
        # create the new attempt
        # create a problem set with same formula
        quests = self.create_problem_set(
            db.get_assignment_details(self.aid, conn)[2])
        new_problem_set = []
        # add all ids to the list
        for quest in quests:
            new_problem_set.append(quest[0])        
        
        self.update_submission_time()
        
        db.add_attempt('a'+str(self.aid), self.uid, new_problem_set, '', '', '', conn)
        
        self.refresh()
        

        
    def calc_grade(self, solution_set, progress):
        '''
        compares the users final progress with a solution set from the database
        and computes the real number that represents the grade in percents
        '''
        progress = ast.literal_eval(progress)
        grade = 0
        i = 0
        for s in solution_set:
            if int(s)==int(progress[i]):
                grade += 1
            i += 1
            
        return (grade/len(solution_set))*100
        
        
        
    def update_submission_time(self):
        '''
        gets the current time upon submission and calls a db function to update
        the user's attempt row with the new submission time
        '''
        now = time.strftime("%d/%m/%Y\n%H:%M:%S")
        db.update_assignment_submission_for_user_for_nth_attempt(
            self.aid, self.uid, len(
                db.get_user_attempts(self.aid, self.uid, conn)), now, conn)

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
    
class ViewAttempt(GUISkeleton):
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
        
    def set_uid(self, uid, aid=None, atid=None):
        self.uid = uid
        self.aid = aid
        self.atid = atid
            # label at top of the frame
        title = self.create_label(self, "A"+str(aid)+" Attempt",
                                  TITLE_FONT,
                                  "Red").grid(row=0, column=1, pady=10)
         
         # get the existing progress for the user for the assignment
        self.existing_progress = db.get_user_nth_attempt(
            self.aid, self.uid, (self.atid-1), conn)[3]
        self.existing_progress = self.existing_progress.split(",")
        self.gen_rows()
           
        Label(self, text="Problem", font=REGULAR_FONT).grid(row=1,column=0, pady=10)
        Label(self, text="Solution", font=REGULAR_FONT).grid(row=1,column=1, pady=10)
        
       
        
    def gen_rows(self):
        # get a list of all the problem ids for the user for that assignment
        ids = db.get_user_nth_attempt(self.aid, self.uid, (self.atid-1), conn)[2]
        # set iterator for grid rows
        ids = ast.literal_eval(ids)
        # for each id create a row
        i = 0
        for qid in ids:
            # create new entries 
            question_label = Label(self, font=REGULAR_FONT)
            answer_label = Label(self, font=REGULAR_FONT)
            self.labels.append(question_label)
            self.entries.append(answer_label)
            # add to corresponding dictonaries with problem ids as keys
            # self.subjects[qid] = subject_entry
            # self.questions[qid] = question_entry
            # self.answers[qid] = answer_entry
          
            # set everything nicely on the grid using an iterator i
            question_label.grid(row=i+3, column=0)
            answer_label.grid(row=i+3, column=1)

            # set each label with the corresponding value from the problem object
            question_label.config(text=db.get_problem_details(conn, qid)[0][2])

            # set each entry with the corresponding value from list of existing progress
            try:
                answer_label.config(text=self.existing_progress[i])
            except IndexError:
                print("no progress yet")
            
            i += 1      
            
    def refresh(self):
        for i in self.entries:
            i.destroy()
        for j in self.labels:
            j.destroy()
        self.entries=[]
        self.labels=[]
        self.cont.show_frame('ViewUserAssignments', self.uid)
        
   