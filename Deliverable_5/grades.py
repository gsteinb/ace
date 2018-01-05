import tkinter as tk
from tkinter import ttk, font,  Tk, Label, Button, Entry,\
     StringVar, DISABLED, NORMAL, END, W, E
from tkinter.messagebox import showinfo
import database_api as db
from assignments import *
from gui_skeleton import *
from ViewAssignments import *

APP_HIGHLIGHT_FONT = ("Helvetica", 14, "bold")
REGULAR_FONT = ("Helvetica", 14, "normal")
TITLE_FONT = ("Helvetica", 16, "normal")
NICE_BLUE = "#3399FF"
HOME_FONT = ("Comic Sans", 26, "bold")

conn = sqlite3.connect('ace.db')


class ViewStudentGrades(GUISkeleton):
	'''class for an admin to view student grades'''
	def __init__(self, parent, controller):
		'''initialises the window'''
		GUISkeleton.__init__(self, parent)
	

		# create the title label
		self.title = self.create_label(self, "View Student Grades",
		                               TITLE_FONT, "Red").grid(row=0, column=1,
		                                                       pady=10, padx=20)

		self.create_dropdown()
			

	def create_dropdown(self):
		'''create  a drop down menu with the assignment options currently in database'''
		self.counter = 0
		self.tkvar = StringVar()
		self.choices = []
		# Dictionary with options
		aids = db.get_assignments_ids(conn) # this returns a list
		for aid in aids:	
			assignment = db.get_assignment_details(aid, conn)
			assign_str = "Assignment " + str(assignment[0])
			self.choices.append(assign_str)

		self.title = self.create_label(self, "Please select the Assignment to view Grades",
	                                       REGULAR_FONT, NICE_BLUE).grid(row=1, column=1,
	                                                                   pady=10, padx=20)			
		
		self.dropdown = ttk.Combobox(self, textvariable=self.tkvar)
		self.dropdown['values'] = self.choices
		self.dropdown.bind('<<ComboboxSelected>>', self.create_listbox)
		self.dropdown.grid(row = 2, column =1)
	
	def create_listbox(self, eventObject):
		self.all_grades = 0
		self.num_users = 0
		self.drop_down_selection = self.dropdown.get()
		#split the selection strng to get the 'aid' 
		result = self.drop_down_selection.split() 
		aid = int(result[1])
		user_ids = db.get_users_ids_assignment(aid,conn)
		new_frame = ttk.Frame(self)
		# create a new scrollbar
		scrollbar = ttk.Scrollbar(new_frame, orient='vertical')
		# create a listbox widget
		self.list_box = tk.Listbox(new_frame,yscrollcommand=scrollbar.set,
			                      width=40, height=8)
		#configure the scrollbar
		scrollbar.config(command=self.list_box.yview)
		scrollbar.pack(side="right", fill="y")
		# adds the listbox to a listbox dictionary with given key     
		self.list_box.pack(side="left", fill="both")
		new_frame.grid(row=4, column=1, padx=15)				
		for uid in user_ids:
			# get all the attempts for the user id
			attempts = db.get_user_attempts(aid, uid, conn)
			# get the last attempt
			last_a = attempts[-1]
			user_result = self.update_grades_table(self, *last_a)
			# return it
			self.list_box.insert(END, user_result)	
			
		self.show_average()
		
	def update_grades_table(self, row, uid, questions, progress, grade):
		''' 
		insert a new row to the grades table with the details
		'''
		user_row = []
		student_details = db.get_user_details(conn, uid)
		name = student_details[0][2]
		user_row.append(name)
		user_row.append(uid)
		if (grade == ''):
			user_row.append("Grade Not Available")
		else:
			self.num_users = self.num_users + 1
			self.all_grades = self.all_grades + int(grade)
			user_row.append(grade)
		return user_row
	
	
	def average_grade(self):
		print(self.all_grades)
		if (self.all_grades == 0 and self.num_users == 0):
			return "No Grades Available"
		elif (self.num_users != 0 and self.all_grades == 0):
			return "0"
		else:
			return str(int(self.all_grades/self.num_users))

	
	
	def show_average(self):
		self.grades = self.create_label(self, "Average Grade", APP_HIGHLIGHT_FONT).grid(row=4, column=3)
		self.average = self.create_label(self, self.average_grade(), REGULAR_FONT).grid(row=4, column=4)
		