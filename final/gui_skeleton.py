import tkinter as tk
from tkinter import ttk, font,  Tk, Label, Button, Entry,\
                    StringVar, DISABLED, NORMAL, END, W, E
from tkinter.messagebox import showinfo
import database_api as db

MONOSPACE_FONT = ("Courier", 10 , "normal")
APP_HIGHLIGHT_FONT = ("Helvetica", 14, "bold")
REGULAR_FONT = ("Helvetica", 12, "normal")
NICE_BLUE = "#3399FF"

class GUISkeleton(ttk.Frame):
	
	'''Skeleton for creating frames in Tkinter'''
	def __init__(self, parent):
		self.entry_fields = {}
		self.list_box = {}
		ttk.Frame.__init__(self, parent)

	def create_label(self, location, text, font=None, foreground=None):
		'''creates a label the programmer will be able to assign
		this to a variable, edit the parameters, and pack to their liking'''
		label = ttk.Label(location)
		label["text"] = text
		if (font != None):
			label["font"] = font
		if (foreground != None):
			label["foreground"] = "white"
		return label

	def create_entry(self, location, key, font=None):
		''' Returns an entry box that the programmer is able to pack'''
		# create an entrybox
		new_entry = ttk.Entry(location)
		if (font != None):
			new_entry["font"] = font
		# assign a stringvar to the Entry
		self.entry_fields[key] = StringVar()
		new_entry["textvariable"] = self.entry_fields[key]
		return new_entry

	def create_button(self, location, text):
		''' creates a button with the wanted text that the programmer
		can customize'''
		new_button = ttk.Button(location)
		new_button["text"] = text
		return new_button   


	def create_empty_label(location, num):
		''' creates an empty label with the designated number of newlines
		create_empty_label(self, 1)
		GUI: \n              <-- this is the label created
		widget
		'''
		txt = ""
		for i in range(num):
			txt += "\n"
			label = ttk.Label(location)
			label["text"] = txt
			label["foreground"] = "white"
		label.pack()

	def create_list_box(self, key, row, column, width=40, height=8, span=1):
		'''method that creates a frame that has a listbox with vertical
		scrollbar, it has default width and height parameters that
		can be changed, it automatically places the listbox in the row
		and column you want it placed in. The Master frame of the listbox
		MUST use grid as the pack-manager
		@param key -> key you want the listbox to have. The listbox will
		automatically be added to a dictionary of listboxes, the key is used
		to call it
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
		                      width=width, height=height,
		                      font=MONOSPACE_FONT)
		#configure the scrollbar
		scrollbar.config(command=list_box.yview)
		scrollbar.pack(side="right", fill="y")
		# adds the listbox to a listbox dictionary with given key
		self.list_box[key] = list_box        
		list_box.pack(side="left", fill="both")
		new_frame.grid(row=row, column=column, columnspan=span)
		
		
	def create_list_box_loc(self, location, key, width=40,
	                        height=8, mode=None):
		'''method that creates a frame that has a listbox with vertical
		scrollbar, it has default width and height parameters that
		can be changed, it automatically places the listbox in the row
		and column you want it placed in. The Master frame of the listbox
		MUST use grid as the pack-manager
		@param location -> location you want to create the listbox
		@param key -> key you want the listbox to have. The listbox will
		automatically be added to a dictionary of listboxes, the key is used
		to call it
		@param width -> the width of the listbox by default is 40
		@param height -> the height of the listbox by default is 8
		@param mode-> the mode of the box
		@returns -> Frame object'''
		# create a new frame
		new_frame = ttk.Frame(location)
		# create a new scrollbar
		scrollbar = ttk.Scrollbar(new_frame, orient='vertical')
		# create a listbox widget
		list_box = tk.Listbox(new_frame,
		                      yscrollcommand=scrollbar.set,
		                      width=width, height=height,
		                      font=MONOSPACE_FONT)
		if (mode != None):
			list_box["selectmode"] = mode
		#configure the scrollbar
		scrollbar.config(command=list_box.yview)
		scrollbar.pack(side="right", fill="y")
		# adds the listbox to a listbox dictionary with given key
		self.list_box[key] = list_box        
		list_box.pack(side="left", fill="both")
		return new_frame
		
	def create_tab(self, num=4):
		'''returns a string that is equivalent to the tab character
		used for formatting purposes
		@param num-> The number of spaces you
		want the tab to be default is 4
		'''
		res = ''
		i = 0
		while i < num:
			res += ' '
			i += 1
		return res	
	    
	def set_uid(self, uid, aid=None, atid=None):
		'''sets the UID for the current user'''
		self.uid = uid
		self.aid = aid
		self.atid = atid
	
