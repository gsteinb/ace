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
TITLE_FONT = ("Helvetica", 16, "normal")
NICE_BLUE = "#3399FF"
HOME_FONT = ("Comic Sans", 26, "bold")

class ViewUserAssignments(GUISkeleton):
    '''
    Objects of this type are used to generate the GUI for the user to see all Assignments screen
    '''
    def __init__(self, parent, controller, uid=None):
        GUISkeleton.__init__(self, parent)
        self.labels = ["Name", "Deadline", "Grade"]
        # label at top of the frame
        '''initiate the buttons on the screen'''
        new_frame = ttk.Frame(self)
        #back button
        self.create_label(new_frame, "Current Assignments",
                              TITLE_FONT, "Red").pack(side="left", padx=40)	
        back_button = self.create_button(new_frame, "Back")
        back_button["command"] = lambda: controller.show_frame('UserHome', self.real_uid)
        back_button.pack(side="right", padx=10)
        new_frame.grid(row=0, column=0, pady=20, sticky="E", columnspan=3)

        # dictionaries to contain the widgets and associate widget to
        # correspondin assignment id
        self.names = {}
        self.deadlines = {}
        self.grades = {}
        # the buttons
        self.past_attempts = {}
        self.new_attempts = {}
        self.cont = controller

        i = 0
        for label in self.labels:
            new_label = self.create_label(self, label, APP_HIGHLIGHT_FONT,
                                          NICE_BLUE).grid(row=2, column=i)
            i+=1

    def set_uid(self, uid, aid=None, atid=None):
        self.real_uid = uid
        self.uid = uid[0]
        self.atid = atid
        self.gen_rows()

    def gen_rows(self):
        ids = db.get_assignments_ids(conn)
        # set iterator for grid rows
        i = 0

        # for each id create a row
        for aid in ids:
            # get the attempts for the user
            attempts = db.get_user_attempts(str(aid), self.uid, conn)
            # get the assignment details
            dets = db.get_assignment_details(aid, conn)
            # create new entries

            name_label = self.create_label(self, text=dets[1], font=REGULAR_FONT)
            deadline_label = self.create_label(self, text=dets[4], font=REGULAR_FONT)
            try :
                grade_label = self.create_label(self, text=attempts[-2][4], font=REGULAR_FONT)
            except IndexError:
                grade_label = self.create_label(self, text=attempts[-1][4], font=REGULAR_FONT)

            # add to corresponding dictonaries with user ids as keys
            self.names[aid] = name_label
            self.deadlines[aid] = deadline_label
            self.grades[aid] = grade_label

            # create new buttons
            past_attempt_button = self.create_button(self, "Past Attempts")
            new_attempt_button = self.create_button(self, "Current Attempt")
            new_attempt_button.config(command=lambda j=[aid, self.atid]: self.cont.show_frame("Attempt" ,self.real_uid, j[0], j[1]))
            past_attempt_button.config(command=lambda j=[aid, self.atid]: self.cont.show_frame("ViewPastAttempt", self.real_uid, j[0], j[1]))

            # add to corresponding dictonaries with user ids as keys
            self.past_attempts[aid] = past_attempt_button
            self.new_attempts[aid] = new_attempt_button

            # set everything nicely on the grid using an iterator i
            name_label.grid(row=i+3, column=0)
            deadline_label.grid(row=i+3, column=1)
            grade_label.grid(row=i+3, column=2)
            new_attempt_button.grid(row=i+3, column=3)
            past_attempt_button.grid(row=i+3, column=4)

            i += 1


class ViewPastAttempt(GUISkeleton):
    def __init__(self, parent, controller, uid=None, aid=None):
        GUISkeleton.__init__(self, parent)
        self.labels = ["Date of Submission  ", "Grade", "View Attempt"]
        # label at top of the frame
        title = self.create_label(self, "Your Attempts",
                                  TITLE_FONT,
                                  "Red").grid(row=0, column=1, pady=10, columnspan=2)
        # dictionaries to contain the widgets and associate widget to
        # correspondin assignment id


        back_button = self.create_button(self, "Back")
        back_button["command"] = lambda: self.refresh()
        back_button.grid(row=0, column=3)

        self.submissions = []
        self.grades = []
        self.buttons = []

        # the buttons
        self.view_attempts = {}
        self.cont = controller

        i = 1
        for label in self.labels:
            new_label = self.create_label(self, label, APP_HIGHLIGHT_FONT).grid(row=2, column=i)
            i+=1


        # generate all the dynamically generated widget rows


        # enable clicking functionality for all the buttons
        #self.enable_buttons()


    def set_uid(self, uid, aid=None, atid=None):
        self.real_uid = uid
        self.uid = uid[0]
        self.atid = atid
        self.gen_rows(self.uid, aid)

    def gen_rows(self, uid, aid):
        
        all_attempts = db.get_user_attempts(str(aid), uid, conn)
        # set iterator for grid rows
        i = 1
        atid = 1

        # for each id create a row
        for attempts in all_attempts:
            # create new entries

            submission_label = self.create_label(self, text=attempts[5], font=REGULAR_FONT)
            grade_label = self.create_label(self, text=attempts[4], font=REGULAR_FONT)

            # add to corresponding dictonaries with user ids as keys
            self.submissions.append(submission_label)
            self.grades.append(grade_label)

            # create new buttons
            view_attempt_button = self.create_button(self, "View")
            view_attempt_button.config(
                command = lambda j=atid: self.cont.show_frame("ViewAttempt" , self.real_uid, aid, j))
            self.buttons.append(view_attempt_button)

            # add to corresponding dictonaries with user ids as keys


            # set everything nicely on the grid using an iterator i
            submission_label.grid(row=i+3, column=1)
            grade_label.grid(row=i+3, column=2)
            view_attempt_button.grid(row=i+3, column=3)

            atid += 1
            i += 1

    def refresh(self):
        for i in self.submissions:
            i.destroy()
        for j in self.grades:
            j.destroy()
        for k in self.buttons:
            k.destroy()
        self.cont.show_frame('ViewUserAssignments', self.real_uid)



class Assignment():
    '''
    A problem object which is used to interact with assignment's data,
    and perform actions that affect assignment's data
    '''
    def __init__(self,aid):
        '''
        aid is the assignment id of the assignment we want to create
        '''
        # get user details from database
        assignment = db.get_assignment_details(conn, aid)[0]
        # assign corresponding values to variables
        self.aid = assignment[0]
        self.topic = assignment[1]
        self.deadline = assignment[2]
        self.visible = assignment[3]
        self.questions = assignment[4]
        self.length = assignment[5]

    # getters and setters
    def get_aid(self):
        return self.aid
    def get_deadline(self):
        return self.deadline
    def get_length(self):
        return self.length
    def get_topic(self):
        return self.topic
    def get_questions(self):
        return self.questions
    def get_visible(self):
        return self.visible

