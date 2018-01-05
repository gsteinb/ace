import tkinter as tk
from tkinter import ttk, font,  Tk, Label, Button, Entry,\
     StringVar, DISABLED, NORMAL, END, W, E
from tkinter.messagebox import showinfo
import database_api as db
from assignments import *
from gui_skeleton import *
from ViewAssignments import *
from all_grades import *
from filtergrades import *


APP_HIGHLIGHT_FONT = ("Helvetica", 14, "bold")
REGULAR_FONT = ("Helvetica", 14, "normal")
TITLE_FONT = ("Helvetica", 16, "normal")
NICE_BLUE = "#3399FF"
HOME_FONT = ("Comic Sans", 26, "bold")

conn = sqlite3.connect('ace.db')

class FilterGrade(GUISkeleton):
	'''Class for an admin to view a specific student grade'''        
	def __init__(self, parent, controller, uid=None, aid=None, student_id=None):
		'''Initialises the window'''
		self.controller = controller			
		GUISkeleton.__init__(self, parent)	

		self.stu_grade = 0
		self.stu_name = ""
		self._init_buttons(controller)
		
	def set_uid(self, uid, aid=None,student_id=None):
		self.uid = uid
		self.aid= aid
		self.student_id = student_id
		
		self.display_attempts(self.student_id,aid)
		self.display_labels()

	def _init_buttons(self, controller):
		'''Initiate the buttons on the screen'''
		#back button
		back_button = self.create_button(self, "Back")
		back_button["command"] = lambda: controller.show_frame('HomeScreen')
		back_button.grid(row=1, column=4)
		#filter by student Uid button
		edit_button = self.create_button(self, "Edit Grade")
		edit_entry = self.create_entry(self, "edit")
		edit_button["command"] = lambda: controller.show_frame('UserHome')
		edit_button.grid(row=1, column=3)
		edit_entry.grid(row=2, column=3)
		
	def display_labels(self):
		'''
		Function that displays current Student and current Grade 
		from filtered screen "ViewStudentGrades"
		'''
		self.student_name =  self.create_label(self,"Student: " + self.stu_name, TITLE_FONT, NICE_BLUE)
		self.grade = self.create_label(self, "Current Assignment Grade: " + str(self.stu_grade), APP_HIGHLIGHT_FONT)		
		self.student_name.grid(row=1, column=2, padx=10, pady=10)
		self.grade.grid(row=2,column=2, pady=10)
		
	def display_attempts(self, uid, aid):
		'''
		Create a listbox to display student attempts for assignment
		selected on the screen ViewStudentGrades
		'''
		#split the selection strng to get the 'aid' 
		user_attempts = db.get_user_attempts(aid, uid, conn)
		filter_frame = ttk.Frame(self)
		# create a new scrollbar
		scrollbar = ttk.Scrollbar(filter_frame, orient='vertical')
		# create a listbox widget
		self.list_box = tk.Listbox(filter_frame,yscrollcommand=scrollbar.set,
		                           width=30, height=8)
		#configure the scrollbar
		scrollbar.config(command=self.list_box.yview)
		scrollbar.pack(side="right", fill="y")
		# adds the listbox to a listbox dictionary with given key     
		self.list_box.pack(side="left", fill="both")

		last_a = user_attempts[-1]
		self.stu_grade = int(last_a[3])
		a_num = 1
		for attempt in user_attempts:
			# go through each of the user's attempt
			list_entry = self.update_attempts_table(self, *attempt, a_num)
			self.list_box.insert(END, list_entry)
			a_num+=1
		self.display_labels()
		filter_frame.grid(row=4, column=2,padx=10)
	
	def update_attempts_table(self, row, uid, questions, progress, grade, attempt_num):
		''' 
		Insert a new row to the student attempts table with the details
		'''
		student_details = db.get_user_details(conn, uid)
		self.stu_name = student_details[0][2]		
		user_row = []
		user_row.append(attempt_num)
		user_row.append(questions)
		user_row.append(progress)
		user_row.append(grade)
		i = 0
		#check for empty content
		for item in user_row:
			if (item == ""):
				user_row[i] = "Not Available"
			i+=1
		return user_row

	def edit_grade(self,uid):
		'''Function for admin to edit the student's current grade'''
		#use edit button
		#change database grade of the last attempt
		#update list
		#pop up of success!