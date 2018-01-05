import tkinter as tk
from tkinter import ttk, font,  Tk, Label, Button, Entry,\
                    StringVar, DISABLED, NORMAL, END, W, E
from tkinter.messagebox import showinfo
import database_api as db
from math_question import *
from assignments import *
from gui_skeleton import *

APP_HIGHLIGHT_FONT = ("Helvetica", 14, "bold")
REGULAR_FONT = ("Helvetica", 12, "normal")
TITLE_FONT = ("Helvetica", 16, "normal")
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
        self.hint = problem[4]
    # getters and setters
    def get_qid(self):
        return self.qid
    def get_subject(self):
        return self.subject      
    def get_question(self):
        return self.question
    def get_answer(self):
        return self.answer
    def get_hint(self):
        return self.hint
    

class ProblemInterface(GUISkeleton):
    '''
    Objects of this type are used to genereate the GUI for the problem Database
    Management screen
    '''
    def __init__(self, parent, controller):
        GUISkeleton.__init__(self, parent)
        self.cont = controller
        self.is_random = False
        self.labels = ["Subject", "Question", "Answer"]
        # label at top of the frame
     
        '''initiate the buttons on the screen'''
        new_frame = ttk.Frame(self)
        #back button
        self.create_label(new_frame, "Problem Database Management",
                              TITLE_FONT, "Red").pack(side="left", padx=40)	
        back_button = self.create_button(new_frame, "Back")
        back_button["command"] = lambda: controller.show_frame('HomeScreen')
        back_button.pack(side="right", padx=10)
        new_frame.grid(row=0, column=0, pady=20, sticky="E")

        self.init_window()
        # generate all the dynamically generated widget rows
        #self.gen_rows()
        
        # enable clicking functionality for all the buttons
       # self.enable_buttons()
       
    def init_window(self):
        '''intialises the GUI window'''
        self.create_list_box("problems", 2, 1)
        self.create_entries(2,0)
        self.problem_db_buttons()
        self.init_problems_in_lb()
        
        
    def create_entries(self, row, column):
        '''creates the entry boxes where the problem is going to add problems into'''
        # create a new_frame
        frame = ttk.Frame(self)
        # create an entry for each 
        # the 3 static lables that are always there
        i = 0
        for label in self.labels:
            new_label = self.create_label(frame, label, REGULAR_FONT,
                                          NICE_BLUE).grid(row=i, column=0,
                                                          padx=10)
            # create first row of entries for add_problem function
            # set everything nicely on the grid
            # create first row of entries for add_problem function
            # set everything nicely on the grid            
            new_entry = self.create_entry(frame, label,
                                          REGULAR_FONT).grid(row=i, column=1, columnspan=3,sticky="NSEW")
            i += 1
            # add the buttons to the frame
        new_frame = ttk.Frame(frame)
        add_button = self.create_button(new_frame, "Add")
        add_button["command"] = lambda : self.add_problem()
        add_button.grid(row=0, column=0, sticky="NSEW")
        update_button = self.create_button(new_frame, "Update")
        update_button["command"] = lambda : self.up_problem()
        update_button.grid(row=0, column=1, sticky="NSEW")
        random_button = self.create_button(new_frame, "Random")
        random_button["command"] = lambda : self.switch()
        random_button.grid(row=0, column=2)
        new_frame.grid(row=i, column=1)
        self.frame = frame
        frame.grid(row=row, column=column, padx=10)        

            
    def problem_db_buttons(self):
        '''create the buttons to interact with the database'''
        # create a button
        delete_button = self.create_button(self, "Delete")
        delete_button["command"] = lambda : self.del_problem()
        delete_button.grid(row=3, column=1, stick="E")
        
        
    def init_problems_in_lb(self):
        '''initialises the problems and puts them in the list box'''
        lb = self.list_box["problems"]
        # create a label_string
        label_string = "qid    subject    question    answer"
        lb.insert(END, label_string)
        # get all the problem ids
        ids = db.get_problem_ids(conn)
        for qid in ids:
            problem_string = self.string_qid(qid)
            lb.insert(END, problem_string)
    
    
    def string_qid(self, qid):
        '''creates a string to add to list box based on the uid'''
        problem_string = "{:<3}    {:<7}    {:<10}    {:<15}"
        # get the problem from the id
        problem = Problem(qid)
        # create a string to hold the result of the problem
        problem_string = problem_string.format(qid, problem.get_subject(), 
                           problem.get_question(), problem.get_answer())
        # place the string inside the list_box
        return problem_string    
        
 
    def del_problem(self):
        '''
        delete a problem from the database and show a success popup
        '''
        lb = self.list_box["problems"]
        # get the index of the selected item
        selection = lb.curselection()
        if (selection != ()):
            # get the item at the index
            problem = lb.get(selection[0]).split()
            # remove problem from database
            db.remove_problem(problem[0], conn)
            # remove from the list box
            lb.delete(selection[0])
            # show popup
            showinfo("Success", "problem #" + 
                     str(problem[0]) + " has been deleted")
    
    
    def up_problem(self):
        '''
        updates a problem details in the database and show a success popup
        '''        
        lb = self.list_box["problems"]
        selection = lb.curselection()
        
        # check to make sure that we have something selected
        if (selection != ()):
            # get new parameters from entry widgets in the dictionaries
            new_subject = self.entry_fields[self.labels[0]].get()
            new_question = self.entry_fields[self.labels[1]].get()
            new_answer = self.entry_fields[self.labels[2]].get()
            
            verified = self.verify_problem_input(new_subject, new_question,
                                                 new_answer)
            if (verified):
                qid = lb.get(selection[0]).split()
                # update the database with new entries
                db.update_problem_subject(qid[0], new_subject, conn)
                db.update_problem_question(qid[0], new_question, conn)
                db.update_problem_answer(qid[0], new_answer, conn)
                # create a string representation to put in the listbox
                problem_string = self.string_qid(qid[0])
                # clear entry boxes
                self.clear_entries()
                # delete from listbox and readd at same index
                lb.delete(selection[0])
                lb.insert(selection[0], problem_string)
                # show popup
                showinfo("Success", "problem #" + str(qid[0]) + " has been updated")


    def verify_problem_input(self, subject, question, answer):
        '''verifies whether a problem is a valid problem'''
        result = True
        # if any of the entries is blank, return a msg
        if ((subject == '') or (question == '') or (answer == '')) :
            result = False
        return result
    
    
    def clear_entries(self):
        ''' clears the entry fields that have the information'''
        for key in self.entry_fields:
            self.entry_fields[key].set('')
    
    
    def add_problem(self):
        '''
        add a problem from the database and show a success popup
        '''
        # get new parameters from entry widgets in the dictionaries
        new_subject = self.entry_fields[self.labels[0]].get()
        new_question = self.entry_fields[self.labels[1]].get()
        new_answer = self.entry_fields[self.labels[2]].get() 
        added = self.add_question_to_db(new_subject, new_question, new_answer)
        if (added):
            lb = self.list_box["problems"]
            qid = lb.get(lb.size()-1).split()
            print(qid)
            showinfo("Success", "problem #" +
                     qid[0] + " has been added to database")
            
    def create_randomized_ui(self):
        '''creates the interface for the create random questions'''
        labels = ["Subject", "Question", "Variables", "Ranges"]
        # create the labels and entry boxes
        frame = ttk.Frame(self)
        i = 0
        for label in labels:
            # create label
            new_label = self.create_label(frame, label, REGULAR_FONT, NICE_BLUE)
            new_label.grid(row=i, column=0)
            # create entry
            new_entry = self.create_entry(frame, label)
            new_entry.grid(row=i, column=1, padx=10, columnspan=2, sticky="NSEW")
            i += 1
        # separate label and entry, since we need to customize the width
        num_label = self.create_label(frame, "Num", REGULAR_FONT, NICE_BLUE)
        num_entry = self.create_entry(frame, "Num")
        num_label.grid(row=i, column=0)
        num_entry.grid(row=i, column=1, padx=10, columnspan=2, sticky="NSEW")
        # create the buttons
        #put buttons in a frame
        new_frame = ttk.Frame(frame)
        add_button = self.create_button(new_frame, "Add")
        add_button["command"] = lambda : self.add_random()
        add_button.grid(row=0, column=0, sticky="NSEW")
        switch_button = self.create_button(new_frame, "Basic")
        switch_button["command"] = lambda : self.switch()
        switch_button.grid(row=0, column=1, sticky="NSEW")
        new_frame.grid(row=i+1, column=1)
        self.frame = frame
        frame.grid(row=2, column=0)
        
    def add_random(self):
        ''' creates a number of unique random questions
        based on parameters given if possible, if it is not possible,
        returns the number of unique problems that it can create'''
        # get the parameters from the entries
        subject = self.entry_fields["Subject"].get()
        question = self.entry_fields["Question"].get()
        variables = self.entry_fields["Variables"].get()
        ranges = self.entry_fields["Ranges"].get()
        num = self.entry_fields["Num"].get()
        # create the math question based on the parameters
        # get rid of the whitespace some reason split doesnt work for 
        # variables??
        variables = variables.replace(' ', '')
        variables = variables.split(',')
        ranges = ranges.strip()
        ranges = ranges.split(',')
        # otherwise we dont want to split
        if len(ranges) > 1:
            i = 0
            while i < len(ranges):
                # put the ranges in a tuple
                ranges[i] = ranges[i].split('-')
                ranges[i] = (int(ranges[i][0]), int(ranges[i][1]))
                i += 1
        else:
            ranges = ranges[0].split('-')
            ranges = (int(ranges[0]), int(ranges[1]))
            # formatting
            new_list = []
            new_list.append(ranges)
            ranges = new_list
        # check if the length is the same
        unique_questions = {}
        if (len(ranges) == 1):
            unique_questions = self.create_random_questions(question, variables,
                                                        ranges, int(num))        
        elif (len(variables) == len(ranges)):
            # then we want to call the specified class
            unique_questions = self.create_random_questions(question, variables,
                                                            ranges, int(num),
                                                            True)
        added = False
        # add questions to database
        for key in unique_questions:
            added = self.add_question_to_db(subject, key, unique_questions[key])
        self.clear_entries()
        # display message of success or failure
        if (added):
            showinfo("Success", "problems have been added to database")
        else:
            showinfo("Failure", "Some problems not added to database")
        
            
    def add_question_to_db(self, subject, question, answer):
        '''takes a question and adds it to the db and list box
        @param subject ->subject of the question
        @param question -> question of the question
        @param answer-> answer of the question
        @returns -> True if successfully added False otherwise
        '''
        lb = self.list_box["problems"]
        # verify the inputs
        verified = self.verify_problem_input(subject, question, answer)  
        if (verified):
            # add new problem to databse and save his id number
            qid = db.add_problem(subject, question, str(answer), '', conn)
            # create a string representation to put in the listbox
            problem_string = self.string_qid(qid)
            # clear entry boxes
            self.clear_entries()
            # add problem to list box
            lb.insert(END, problem_string)
            # show popup
        return verified

    
    def create_random_questions(self, question, variables, ranges,
                                num, specified=False):
        '''
        create a number of random questions based on the parameters given
        @param question-> string representing the question
        @param variables-> variables in the question that will be replaced
        @param ranges-> ranges of those variables
        @param num-> number of questions to create
        @param specified-> optional parameter that determines whether there are
        ranges for each variable, or one range for all variables
        @returns a dictionary with the questions as keys and answers as values
        '''
        # create a dictionary, this ensures that every question is unique
        unique_questions = {}        
        for i in range(num):
            # create a new math question
            q = SimpleMathQuestion(question, variables, ranges, specified)
            # parse the string and make new variables
            q.parse_question()
            # evaluate the new question
            q.evaluate_answer()
            unique_questions[q.get_question()] = q.get_answer()
        return unique_questions
    
    
    def switch(self):
        ''' switches from creating random questions to manually
        adding questions'''
        # destroy the frame that is currently using the space
        self.frame.destroy()
        # switch to the other frame
        if (self.is_random == False):
            self.create_randomized_ui()
            self.is_random = True
        else:
            self.create_entries(2, 0)
            self.is_random = False