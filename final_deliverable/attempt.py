import tkinter as tk
from tkinter import ttk, font,  Tk, Label, Button, Entry,\
     StringVar, DISABLED, NORMAL, END, W, E
from tkinter.messagebox import showinfo
import database_api as db
from user_skeleton import *
from problem import *
import ast
from random import sample
from main import *
from pdf import *
import time

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.pyplot import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

from main import *

import re # LEADERBOARD
import datetime # LEADERBOARD

APP_HIGHLIGHT_FONT = ("Helvetica", 14, "bold")
REGULAR_FONT = ("Helvetica", 12, "normal")
TITLE_FONT = ("Helvetica", 14, "normal")
NICE_BLUE = "#3399FF"
HOME_FONT = ("Comic Sans", 26, "bold")

# Constants for converting time units to seconds
YRSEC = 31556952
MONSEC = 2629746
DAYSEC = 86400
HRSEC = 3600
MINSEC = 60

conn = sqlite3.connect('ace.db')


class Attempt(UserSkeleton):
    '''
    Objects of this type are used to genereate the GUI for the problem Database
    Management screen
    '''
    def __init__(self, parent, controller, uid=None, aid=None):
        UserSkeleton.__init__(self, parent)
        self.cont = controller
        self.texes= []
        self.labels = ["Subject", "Question", "Answer"]
        # dictionaries/lists to contain the widgets and associate widget to
        # correspondin problem id
        self.entries = []
        self.labels = []
        self.hint_buttons = {}
        self.hints_labels = {}
        #store questions student needs to complete
        self.problem_ids = []
        #counter for number of hints student is allowed to use
        self.hints_left = 3
        back_button = self.create_button(self, "Back")
        back_button["command"] = lambda: self.refresh()
        back_button.grid(row=0, column=3)


    def set_uid(self, uid, aid=None, atid=None):
        self.real_uid = uid
        self.uid = uid[0]
        self.aid = aid
        self.atid = atid

        self.conv = CreatePDF(self.uid, self.aid, self.atid)

            # label at top of the frame
        title = self.create_label(self, "A"+str(aid)+" Attempt",
                                  TITLE_FONT,
                                  "Red").grid(row=0, column=1, pady=10, columnspan=2)

         # get the existing progress for the user for the assignment
        self.existing_progress = db.get_assignment_progress_for_user(
            self.aid, self.uid, conn)

        # generate all the dynamically generated widget rows
        self.gen_rows()

        # enable clicking functionality for all the buttons
        self.enable_buttons()


    def enable_buttons(self):

        # configure clicking function for all the delete buttons
        for qid in self.problem_ids:
            self.hint_buttons[qid].config(command=lambda j=qid: self.show_hint(j))

    def show_hint(self, qid):
        '''
        Set the label text to the hint for that question
        '''
        if (self.hints_left <= 0):
            showinfo("Sorry", "No hints left!")
        else:
            problem = Problem(qid)
            self.hints_labels[qid]["text"] = problem.get_hint()
            self.hints_left -= 1

    def gen_rows(self, uid=None, aid=None, atid=None):

        title_hints = self.create_label(self, "You have "+str(self.hints_left)+" hints",
                                      APP_HIGHLIGHT_FONT, NICE_BLUE)
        self.labels.append(title_hints)
        # get a list of all the problem ids for the user for that assignment
        ids = db.get_user_nth_attempt(self.aid, self.uid, -1, conn)[2]
        # set iterator for grid rows
        ids = ast.literal_eval(ids)
        # for each id create a row
        self.i = 0
        for qid in ids:
            # create new entries
            self.problem_ids.append(qid)
            hint_button = self.create_button(self, "Hint!")
            #question_label = self.create_label(self, "", REGULAR_FONT)
            answer_entry = ttk.Entry(self, font=REGULAR_FONT)
            hint_label = self.create_label(self, "", REGULAR_FONT, NICE_BLUE)
            self.labels.append(hint_label)
            self.entries.append(answer_entry)
            self.hint_buttons[qid] = hint_button
            self.hints_labels[qid] = hint_label

            # set everything nicely on the grid using an iterator i
            answer_entry.grid(row=self.i+4, column=2)
            hint_button.grid(row=self.i+4, column=3)
            hint_label.grid(row=self.i+4, column=4)

            # set each label with the corresponding value from the problem object
            #question_label.config(text=db.get_problem_details(conn, qid)[0][2])

            # set each entry with the corresponding value from list of existing progress
            try:
                answer_entry.insert(0, self.existing_progress[self.i])
            except IndexError:
                print("no progress yet")

            # NEW (latex feature) create the canvas with the latex problem
            self.latex_row(db.get_problem_details(conn, qid)[0][2])

            self.i += 1

        title_hints.grid(row=1, column=2, pady=10)
        # create submit and save progress buttons
        self.update_progress_button = self.create_button(self, "Save")
        self.update_progress_button["command"] = lambda : self.update_progress()
        self.update_progress_button.grid(row=0, column=4, padx=5)

        self.submit_button = self.create_button(self,"Submit")
        self.submit_button["command"] = lambda : self.submit_progress()
        self.submit_button.grid(row=0, column=5, padx=5)

        self.pdf_button = self.create_button(self, "Convert to PDF")
        self.pdf_button["command"]= lambda : self.conv.addOnLatex()
        self.pdf_button.grid(row=0, column=6, padx=5)

    # NEW (latex feature) create the canvas with the latex problem
    def latex_row(self, txt=""):
        label = Label(self)
        label.grid(row=self.i+4, column=0)
        self.texes.append(label)

        fig = matplotlib.figure.Figure(figsize=(4,2), dpi=50)
        ax = fig.add_subplot(111)

        canvas = FigureCanvasTkAgg(fig, master=label)
        canvas.get_tk_widget().grid(row=self.i+4, column=0)
        canvas._tkcanvas.grid(row=self.i+4, column=0)

        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        ax.clear()
        ax.text(0.1, 0.3, txt, fontsize = 30)
        canvas.draw()


    def refresh(self):
        '''
        Delete all widgets on screen, reset all data structures
        '''
        for i in self.entries:
            i.destroy()
        for j in self.labels:
            j.destroy()
        for button in list(self.hint_buttons.items()):
            button[1].destroy()
        for label in list(self.hints_labels.items()):
            button[1].destroy()
        for tex in self.texes:
            tex.destroy()
        self.pdf_button.destroy()
        self.update_progress_button.destroy()
        self.submit_button.destroy()
        self.entries=[]
        self.labels=[]
        self.texes = []
        self.hint_buttons = {}
        self.hints_labels = {}
        self.problem_ids = []
        self.cont.show_frame('ViewUserAssignments', self.real_uid)


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
        and calls a database function to update the user's attempt row with the
        new progress

        Also adds completion time (in seconds) to user's records in database.
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

       # LEADERBOARD
        # Update user's time
        user_attempts = db.get_user_attempts(self.aid, self.uid, conn)
        assignment_start = db.get_assignment_details(self.aid, conn)[3]

        # Update user's overall grade and time from recalculating all latest
        # submissions they made for all assignments
        ##num_of_assignments = len(db.get_assignments_ids(conn))
        all_assignments = db.get_assignments_ids(conn)
        user_total_grade = 0
        user_total_time = 0

        i = 1
        for assignment in all_assignments:
            assignment_start = db.get_assignment_details(i, conn)[3]

            # Ensure current user's attempt is not one that has 0 attempt.
            if (db.get_latest_user_attempts(i, self.uid, conn)[0][5] != '0'):
                # Ensure data from latest submission is retrieved
                if (db.get_latest_user_attempts(i, self.uid, conn)[0][5] != ''):
                    latest_id = 0
                else:
                    latest_id = 1
                curr_aid_time = self.start_to_end_sec(assignment_start, db.get_latest_user_attempts(i, self.uid, conn)[latest_id][5])
                user_total_grade += int(db.get_latest_user_attempts(i, self.uid, conn)[latest_id][4])
                user_total_time += int(curr_aid_time)
                i+=1

        average_grade = user_total_grade/len(all_assignments)

        db.update_user_grade(self.uid, round(average_grade, 2), conn)
        db.update_user_time(self.uid, user_total_time, conn)


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

    def start_to_end_sec(self, start, now): # LEADERBOARD
        da0, mon0, yr0 = start.split("/")
        curr_time = re.split(':|\n|/', str(now)) # "%d/%m/%Y\n%H:%M:%S"
        da1, mon1, yr1, hr1, min1, sec1 = curr_time[0], curr_time[1], curr_time[2], curr_time[3], curr_time[4], curr_time[5]
        start_sec = int(yr0) * YRSEC + int(mon0) * 2629746 + int(da0)
        end_sec = int(yr1) * YRSEC + int(mon1) * 2629746 + int(da1) * DAYSEC + int(hr1) * HRSEC + int(min1) * MINSEC + int(float(sec1))
        net_sec = end_sec - start_sec
        return net_sec


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
        self.real_uid = uid
        self.uid = uid[0]
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

        problem = self.create_label(self, "Problem", APP_HIGHLIGHT_FONT, NICE_BLUE)
        solution = self.create_label(self, "Solution", APP_HIGHLIGHT_FONT, NICE_BLUE)
        problems.grid(row=1,column=1, pady=10)
        solution.grid(row=1,column=2, pady=10)


    def gen_rows(self):
        # get a list of all the problem ids for the user for that assignment
        ids = db.get_user_nth_attempt(self.aid, self.uid, (self.atid-1), conn)[2]
        # set iterator for grid rows
        ids = ast.literal_eval(ids)
        # for each id create a row
        i = 0
        for qid in ids:
            # create new entries
            question_label = self.create_label(self, text="", font=REGULAR_FONT)
            answer_label = self.create_label(self, text="", font=REGULAR_FONT)
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
        self.cont.show_frame('ViewPastAttempt', self.real_uid, self.aid)

