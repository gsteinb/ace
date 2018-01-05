import tkinter as tk
from tkinter import ttk, font,  Tk, Label, Button, Entry,\
                    StringVar, DISABLED, NORMAL, END, W, E
from tkinter.messagebox import showinfo
import database_api as db
from assignments import *
from gui_skeleton import *
from problem import *
from user import *
import ast

APP_HIGHLIGHT_FONT = ("Helvetica", 14, "bold")
REGULAR_FONT = ("Helvetica", 12, "normal")
TITLE_FONT = ("Helvetica", 14, "normal")
NICE_BLUE = "#3399FF"
HOME_FONT = ("Comic Sans", 26, "bold")

conn = sqlite3.connect('ace.db')

class Leaderboard(GUISkeleton):
    '''
    Objects of this type are used to generate the GUI displaying a leaderboard
    '''
    def __init__(self, parent, controller):
        GUISkeleton.__init__(self, parent)
        self.cont = controller
        ##self.labels = ["Role", "Name", "Email"]
        self.labels = ["Rank", "Name", "Email", "Grade", "Time"]
        # label at top of the frame
        new_label = self.create_label(self, "Leaderboard\n",
                                      TITLE_FONT,
                                      "Red").grid(row=0, column=1,pady=10) 
        # dictionaries to contain the widgets and associate widget to
        # corresponding user id
        self.names = {}
        self.emails = {}
        self.grades = {}
        self.times = {}
        
        ##self.updates = {}
        ##self.deletes = {}
        
        # the 3 static lables that are always there
        i = 0
        for label in self.labels:
            new_label = self.create_label(self, label, REGULAR_FONT,
                                          NICE_BLUE).grid(row=1, column=i)
            # create first row of entries for add_problem function
            # set everything nicely on the grid
            # create first row of entries for add_user function
            # set everything nicely on the grid            
            ##new_entry = self.create_entry(self, label,
            ##                              REGULAR_FONT).grid(row=2, column=i)
            i += 1         
        ## create add user button
        ##add_user_button = self.create_button(self, "Add User")
        ## set button method to add_user  
        ##add_user_button["command"] = lambda : self.add_user()        
        ##add_user_button.grid(row=2, column=3)
        back_button = self.create_button(self, "Back")
        back_button["command"] = lambda : controller.show_frame('HomeScreen')
        back_button.grid(row=0, column=3)
        # generate all the dynamically generaterd widget rows
        self.gen_rows()
        
        # enable clicking functionality for all the buttons
        self.enable_buttons()
        
          
        
    def gen_rows(self):
        # get a list of all the user ids in the database
        ids = db.get_user_by_grade(conn)
        # set iterator for grid rows
        i = 0
        # for each id create a row
        for uid in ids:
            # create new entries
            user = db.get_user_details(conn, uid)
            rank_label = Label(self, font=REGULAR_FONT, text=i+1)
            name_label = Label(self, font=REGULAR_FONT, text=user[0][2])
            email_label = Label(self, font=REGULAR_FONT, text=user[0][3])
            grade_label = Label(self, font=REGULAR_FONT, text=user[0][5])
            time_label = Label(self, font=REGULAR_FONT, text=user[0][6])
            # add to corresponding dictonaries with user ids as keys
            self.names[uid] = name_label
            self.emails[uid] = email_label    
            self.grades[uid] = grade_label
            self.times[uid] = time_label
          
            ## create new buttons
            ##update_button = self.create_button(self, "Update")
            ##delete_button = self.create_button(self, "Delete")
            ## add to corresponding dictonaries with user ids as keys        
            ##self.deletes[uid] = delete_button
            ##self.updates[uid] = update_button
            
            # set everything nicely on the grid using an iterator i
            rank_label.grid(row=i+3, column=0)
            name_label.grid(row=i+3, column=1)
            email_label.grid(row=i+3, column=2)
            grade_label.grid(row=i+3, column=3)
            time_label.grid(row=i+3, column=4)
            ##update_button.grid(row=i+3, column=3)
            ##delete_button.grid(row=i+3, column=4)
            i += 1
            
            """# create new user object to contain user info
            user = User(uid)
            # set each entry with the corresponding value from the user object
            name_label.insert(0, user.get_name())
            email_label.insert(0, user.get_email())
            grade_label.insert(0, user.get_grade())
            time_label.insert(0, user.get_time())"""
            ##print(user.get_name())
            ##print(user.get_grade())
            
        
            
    """def del_user(self, button):
        '''
        delete a user from the database and show a success popup
        '''
        # remove user from databse
        db.remove_user(button, conn)
        
        self.refresh()
        
        # show popup
        showinfo("Success", "User #" + str(button) + " has been deleted")
    
    def up_user(self, button):
        '''
        delete a user details in the database and show a success popup
        '''        
        # get new parameters from entry widgets in the dictionaries
        new_role = self.names[button].get()
        new_name = self.emails[button].get()
        new_email = self.grades[button].get()
        # update the database with new entries
        db.update_user_role(button, new_role, conn)
        db.update_user_name(button, new_name, conn)
        db.update_user_email(button, new_email, conn)
        
        self.refresh()
        
        # show popup
        showinfo("Success", "User #" + str(button) + " has been updated")
        
    def add_user(self):
        '''
        delete a user from the database and show a success popup
        '''
        # get new parameters from entry widgets in the dictionaries
        new_role = self.entry_fields["Role"].get()
        new_name = self.entry_fields["Name"].get()
        new_email = self.entry_fields["Email"].get()        
        # add new user to databse and save his id number
        uid = db.add_user(new_role, new_name, new_email, "", conn)
        # show popup
        self.refresh()
        # clear entries
        self.entry_fields["Role"].set('')
        self.entry_fields["Name"].set('')
        self.entry_fields["Email"].set('')        
        showinfo("Success", "User #" + str(uid ) + " has been added to database")"""
        

    def refresh(self):
        for name in list(self.names.items()):
            name[1].destroy()
        for email in list(self.emails.items()):
            email[1].destroy()
        for grade in list(self.grades.items()):
            grade[1].destroy()
        for time in list(self.times.items()):
            time[1].destroy()
        ##for update in list(self.updates.items()):
        ##    update[1].destroy()
        ##for delete in list(self.deletes.items()):
        ##    delete[1].destroy()
        self.gen_rows()
        self.enable_buttons()
        
    def enable_buttons(self):
        # get a list of all existing user ids
        user_ids = db.get_user_ids(conn)        
        # configure clicking function for all the delete buttons
        ##for uid in user_ids:
        ##    self.deletes[uid].config(command=lambda j=uid: self.del_user(j))
        # configure clicking function for all the update buttons
        ##for uid in user_ids:
        ##    self.updates[uid].config(command=lambda j=uid: self.up_user(j))
