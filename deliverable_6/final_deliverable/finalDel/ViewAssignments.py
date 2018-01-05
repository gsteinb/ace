import tkinter as tk
from tkinter import ttk, font,  Tk, Label, Button, Entry,\
                    StringVar, DISABLED, NORMAL, END, W, E
from tkinter.messagebox import showinfo
import database_api as db
from assignments import *
from gui_skeleton import *
from random import sample

APP_HIGHLIGHT_FONT = ("Helvetica", 14, "bold")
REGULAR_FONT = ("Helvetica", 12, "normal")
TITLE_FONT = ("Helvetica", 16, "normal")
NICE_BLUE = "#3399FF"
HOME_FONT = ("Comic Sans", 26, "bold")

conn = sqlite3.connect('ace.db')

class ViewAssignments(GUISkeleton):
    '''class for an admin to view assignments'''
    def __init__(self, parent, controller):
        '''initialises the window'''
        self.add_pressed = False
        self.subj_pressed = False
        self.controller = controller
        self.titles = []
        # name of the buttons for the first assignments box
        self.buttons = ["Add New", "Delete", "Back"]
        # the name of the buttons for the subject box if its created
        self.subject_buttons = ["Delete", "Done"]
        '''the names of the entry boxes these are stored as keys
        in the dictionary self.entry_fields which
        is inherited from GUISkeleton'''
        self.entries = ["Assignment Name", "Due Date", "Visible", "Subject",
                        "Number of Questions"]
        GUISkeleton.__init__(self, parent)
        # create the title label
      
        '''initiate the buttons on the screen'''
        new_frame = ttk.Frame(self)
        #back button
        self.create_label(new_frame, "Manage Assignments",
                                      TITLE_FONT, "Red").pack(side="left", padx=40)	
        back_button = self.create_button(new_frame, "Back")
        back_button["command"] = lambda: controller.show_frame('HomeScreen')
        back_button.pack(side="right", padx=10)
        new_frame.grid(row=0, column=0, pady=20, sticky="E")
        
        
        # we will fill this in with the listbox after
        self.subject_box = None
        self.list_box = None
        # the functions to initialise the buttons and the widgets
        # the numbers are the row and the column to place the widgets in
        self.create_frame(2, 0)
        self.init_buttons(3, 0)
        # add the assignments currently in the database to the list
        aids = db.get_assignments_ids(conn) # this returns a list
        for aid in aids:
            self.add_assign_to_lb(aid)
        # list that will hold all the frames of the widgets created 
        self.frames = []
        
    def create_tab(self, num=4):
        '''returns a string that is equivalent to the tab character
        used for formatting purposes
        @param num-> The number of spaces you want the tab to be default is 4
        '''
        res = ''
        i = 0
        while i < num:
            res += ' '
            i += 1
        return res
    
    def subject_buttons_init(self, row, column):
        '''creates the buttons for the add subject box
        @param row-> The row to place the buttons in
        @param column -> the column to place the buttons in'''
        # create a new frame
        frame = ttk.Frame(self)
        for button in self.subject_buttons:
            # create a new button
            new_button = self.create_button(frame, button)
            # choose a command
            if button == "Delete":
                # deletes currently selected item
                new_button["command"] = (lambda lb=self.subject_box : 
                                         lb.delete('anchor'))
            elif button == "Done":
                new_button["command"] = lambda : self.done()
            new_button.pack(side="left")
        frame.grid(row=row, column=column)
        self.frames.append(frame)
    
    def add_subject_list(self, row, column, width=20, height=8):
        '''creates a listbox to display the subjects for adding an assignment
        the parameters adjust the dimensions of the frame
        @param row-> the row to place the widget in
        @param column-> the column to place the widget in
        @param width-> the width of the widget by default is 20
        @param height -> the height of the widget by default is 8
        '''
        # create a new frame
        frame = ttk.Frame(self)
        # config the scrollbar
        scrollbar = ttk.Scrollbar(frame, orient='vertical')
        # create listbox widget
        listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set,
                             width=width, height=height)
        #configure the scrollbar
        scrollbar.config(command=listbox.yview)
        scrollbar.pack(side="right", fill="y")
        # set the self parameter to the listbox
        self.subject_box = listbox        
        listbox.pack(side="left", fill="both")
        frame.grid(row=row, column=column)
        self.frames.append(frame)

    def add_assignment(self, row, column):
        '''creates the frame for adding assignments to the system
        @param row-> The row you want to place the frame in the grid
        @param column -> the column you want to place the frame in'''
        if self.add_pressed == False:
            # create the title label
            title = self.create_label(self,"Add Assignment", APP_HIGHLIGHT_FONT, NICE_BLUE)
            # we need to append it because we want to delete this later
            self.titles.append(title)
            title.grid(row=1, column=1)
            # create a new frame
            # this is the main frame that will house all the other frames
            main_frame = ttk.Frame(self)
            rw = 0
            col = 0
            for entry in self.entries:
                # create a new label and place it in the frame
                label = self.create_label(main_frame, entry)
                # create a new entry
                new_enterbox = self.create_entry(main_frame, entry)
                # pack the label and the entry box into the frame
                label.grid(row=rw, column=col)
                new_enterbox.grid(row=rw, column=col+1)
                rw += 1 
            # create the add button that will be in the bottom of the grid
            new_button = self.create_button(main_frame, "Add Subject")
            new_button["command"] = lambda : self.add_subject()
            new_button.grid(row=rw, column=col+1)
            main_frame.grid(row=row, column=column)
            self.frames.append(main_frame)
            self.add_pressed = True
        
    def add_subject(self):
        '''the method that the add button calls to display the subjects
        in the box on the side'''
        if self.subj_pressed == False:
            # create the title
            title = self.create_label(self, "Subjects", TITLE_FONT)
            self.titles.append(title)
            title.grid(row=1, column=2)
            # create the box
            self.add_subject_list(2, 2)
            # create the buttons
            self.subject_buttons_init(3, 2)
            self.subj_pressed = True
        # get the values from the subject and number of question enterboxes
        subject = self.entry_fields["Subject"].get()
        question_num = self.entry_fields["Number of Questions"].get()
        if (subject != '' and question_num != ''):
            tab = self.create_tab()
            self.add_to_list(self.subject_box, subject + tab + question_num)
            
    def done(self):
        '''the command that happens when the done button is pressed
        This will add the assignment to the database and remove
        the widgets for creating the assignment'''
        # start by getting the info from the entry boxes
        # this does not include the subject and number fields, because
        # those are stored in the listbox
        name = self.entry_fields["Assignment Name"].get()
        deadline = self.entry_fields["Due Date"].get()
        visible = self.entry_fields["Visible"].get()
        # we want to make sure that none of the fields are empty
        if (name != '' and deadline != '' and visible != ''):
            formula = ''
            # get the values from the listbox as a list
            lb = self.subject_box
            contents = lb.get(0, lb.size())
            # this returns a tuple that looks like this
            # ('1    1', '2    2') where the separator is the tab we created
            for i in range(len(contents)):
                # first we want to split the string
                sep = self.create_tab()
                items = contents[i].split(sep)
                formula += items[0] + ":" + items[1]
                formula += ","
            formula = formula[:-1]
            # update the database
            num = self.update_assignments_table(name, formula, deadline, visible)
            self.table_functions(num, formula)
            # check to make sure that the assignment is in the db
            aids = db.get_assignments_ids(conn)
            if num in aids:
                # add assignment to the listbox
                self.add_assign_to_lb(num)
                # want to destroy the widget after
                for frame in self.frames:
                    frame.destroy()
                # destroy labels
                for title in self.titles:
                    title.destroy()
                self.subj_pressed = False
                self.add_pressed = False
                # display message of success
                showinfo("Info", "Assignment successfully added")
            else:
                showinfo("Fail", "Could not add assignment")
            
    def add_assign_to_lb(self, aid):
        '''adds an assignment to the listbox to be able to be viewed
        @param aid-> the assignment id of the assignment to be added'''
        # update the other listbox that displays assignments
        # get the info by AID
        assignment = db.get_assignment_details(aid, conn)
        assign_string = ''
        tab = self.create_tab()
        for col in assignment:
            assign_string += str(col) + tab
        # add the assignment to the list box
        self.add_to_list(self.list_box, assign_string)

    def update_assignments_table(self, name, formula, deadline, visible):
        ''' 
        insert a new row to the assignments table with the details
        '''
        num = db.add_assignment(name, formula, "", deadline, visible, conn)
        # return id of new assignment
        return num
        
    def table_functions(self, num, formula):
        '''
        create formula, update table, 
        create new assignment table->add row for each user
        '''
        # create the assignment table with it's proper name in the format: a#
        db.create_assignment_table(num, conn)
        # get a list of currently existing user ids in the system
        ids = db.get_user_ids(conn)
        # for each user id, create a first attempt entry using a unique set 
        # of questions
        for uid in ids:
            # unique set of questions
            quests = self.create_problem_set(formula)
            # extract a list of problem ids
            prob_ids = []
            # add all ids to the list
            for quest in quests:
                prob_ids.append(quest[0])   
            # create the user attempt entry
            db.add_attempt("a"+str(num), uid, prob_ids, "","","", conn)
        
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
    
    def delete_assignment(self):
        '''deletes a selected assignment from the database'''
        tab = self.create_tab()
        lb = self.list_box
        # creates a list of the currently clicked assignment
        assignment_string = lb.get('anchor').split(tab)
        # anchor will delete the currently selected item
        # check to make sure that there is something selected
        if (len(assignment_string) != 1): 
            # remove assignment from database by AID
            db.remove_assignment(assignment_string[0], conn)
            # remove assignment from the list
            lb.delete('anchor')
        
    
    def init_buttons(self, row, column):
        '''initialises the buttons in a loop'''
        # create a new frame
        frame = ttk.Frame(self)
        # column counter for each item in the loop
        # col = 0
        for button in self.buttons:
            # create a button using the method from GUISkeleton
            new_button = self.create_button(frame, button)
            # intialise the buttons
            if button == "Add New":
                lb = self.list_box
                new_button["command"] = lambda : self.add_assignment(2, 1)
            elif button == "Delete":
                new_button["command"] = lambda :self.delete_assignment()
            elif button == "Back":
                new_button["command"] = lambda : self.back()
            new_button.pack(side='left')
            # increment the column number
            # col += 1
        frame.grid(row=row, column=column)
    
    def back(self):
        '''the back method, this will destroy any widgets we didnt use'''
        for title in self.titles:
            title.destroy()
        for frame in self.frames:
            frame.destroy()
        self.add_pressed = False
        self.subj_pressed = False
        self.controller.show_frame("HomeScreen")        
        
    def create_frame(self, row, column, width=50, height=8):
        '''method that creates the frame where the assignments are going
        to be listed
        @param row -> The row where you want the frame to be placed
        @param column -> the column where you want the frame to be placed
        @param width -> the width of the listbox by default is 40
        @param height -> the height of the listbox by default is 8'''
        # create a new frame
        new_frame = ttk.Frame(self)
        # create a new scrollbar
        scrollbar = ttk.Scrollbar(new_frame, orient='vertical')
        # create a listbox widget
        list_box = tk.Listbox(new_frame,
                              yscrollcommand=scrollbar.set,
                              width=width, height=height)
        #configure the scrollbar
        scrollbar.config(command=list_box.yview)
        scrollbar.pack(side="right", fill="y")
        # set the self parameter to the listbox
        self.list_box = list_box 
        list_box.pack(side="left", fill="both")
        new_frame.grid(row=row, column=column, pady=15)

        
    def add_to_list(self, box, assignment):
        '''adds an assignment to the listbox, where the assignment is a string
        which represents the name of the assignment. e.g. Assignment 1'''
        box.insert(END, assignment)
        

