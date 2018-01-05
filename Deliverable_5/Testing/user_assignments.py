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

class ViewUserAssignments(GUISkeleton):
    '''
    Objects of this type are used to generate the GUI for the user to see all Assignments screen
    '''
    def __init__(self, parent, controller, uid=None):
        GUISkeleton.__init__(self, parent)
        self.labels = ["Name", "Deadline", "Grade"]
        # label at top of the frame
        title = self.create_label(self, "Your Assignments\n",
                                  TITLE_FONT,
                                  "Red").grid(row=1, column=1, pady=10)
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
            new_label = self.create_label(self, label, REGULAR_FONT,
                                          NICE_BLUE).grid(row=2, column=i)
            i+=1
        #back_button = self.create_button(self, "Back")
        # set button method to go back
        back_button = self.create_button(self, "Back")
        back_button["command"] = lambda: controller.show_frame('UserHome')
        back_button.grid(row=1, column=4)

        # generate all the dynamically generated widget rows


        # enable clicking functionality for all the buttons
        #self.enable_buttons()

    '''
    def enable_buttons(self):
        # get a list of all existing problem ids
        assignment_ids = db.get_assignment_ids(conn)
        # configure clicking function for all the delete buttons
        for aid in assignment_ids:
            self.past_attempts[aid].config(command=lambda j=qid: self.del_problem(j))
        # configure clicking function for all the update buttons
        for qid in problem_ids:
            self.updates[qid].config(command=lambda j=qid: self.up_problem(j))
    '''
    def set_uid(self, uid, aid=None, atid=None):
        self.uid = uid
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
            name_label = Label(self, font=REGULAR_FONT, text=dets[1])
            deadline_label = Label(self, font=REGULAR_FONT, text=dets[3])
            try :
                grade_label = Label(self, font=REGULAR_FONT, text=attempts[-2][4])
            except IndexError:
                grade_label = Label(self, font=REGULAR_FONT, text=attempts[-1][4])
            # add to corresponding dictonaries with user ids as keys
            self.names[aid] = name_label
            self.deadlines[aid] = deadline_label
            self.grades[aid] = grade_label

            # create new buttons
            past_attempt_button = self.create_button(self, "Past Attempts")
            new_attempt_button = self.create_button(self, "Current Attempt")
            new_attempt_button.config(command=lambda j=[aid, self.atid]: self.cont.show_frame("Attempt" ,self.uid, j[0], j[1]))
            past_attempt_button.config(command=lambda j=[aid, self.atid]: self.cont.show_frame("ViewPastAttempt", self.uid, j[0], j[1]))

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
        self.labels = ["Date of Submission", "Grade", "View Attempt"]
        # label at top of the frame
        title = self.create_label(self, "Your Attempts\n",
                                  TITLE_FONT,
                                  "Red").grid(row=1, column=4, pady=10)
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

        i = 0
        for label in self.labels:
            new_label = self.create_label(self, label, REGULAR_FONT,
                                          NICE_BLUE).grid(row=2, column=i)
            i+=1


        # generate all the dynamically generated widget rows


        # enable clicking functionality for all the buttons
        #self.enable_buttons()


    def set_uid(self, uid, aid=None, atid=None):
        self.uid = uid
        self.atid = atid
        self.gen_rows(uid, aid)

    def gen_rows(self, uid, aid):

        all_attempts = db.get_user_attempts(str(aid), uid, conn)
        # set iterator for grid rows
        i = 0
        atid = 1

        # for each id create a row
        for attempts in all_attempts:

            # create new entries
            submission_label = Label(self, font=REGULAR_FONT, text=attempts[5])
            grade_label = Label(self, font=REGULAR_FONT, text=attempts[4])

            # add to corresponding dictonaries with user ids as keys
            self.submissions.append(submission_label)
            self.grades.append(grade_label)

            # create new buttons
            view_attempt_button = self.create_button(self, "View")
            view_attempt_button.config(
                command = lambda j=atid: self.cont.show_frame("ViewAttempt" , uid, aid, j))
            self.buttons.append(view_attempt_button)

            # add to corresponding dictonaries with user ids as keys


            # set everything nicely on the grid using an iterator i
            submission_label.grid(row=i+3, column=0)
            grade_label.grid(row=i+3, column=1)
            view_attempt_button.grid(row=i+3, column=2)
            
            atid += 1
            i += 1

    def refresh(self):
        for i in self.submissions:
            i.destroy()
        for j in self.grades:
            j.destroy()
        for k in self.buttons:
            k.destroy()
        self.cont.show_frame('ViewUserAssignments', self.uid)



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

