import tkinter as tk
from tkinter import ttk, font,  Tk, Label, Button, Entry,\
     StringVar, DISABLED, NORMAL, END, W, E
#from PIL import ImageTk, Image
from tkinter.messagebox import showinfo
import database_api as db
from gui_skeleton import *
from assignments import *
from user import *
from problem import *
from user_assignments import *
from attempt import *
from all_grades import *
from ViewAssignments import *
from leaderboard import * # LEADERBOARD


APP_HIGHLIGHT_FONT = ("Helvetica", 14, "bold")
REGULAR_FONT = ("Helvetica", 12, "normal")
TITLE_FONT = ("Helvetica", 14, "normal")
NICE_BLUE = "#3399FF"
HOME_FONT = ("Comic Sans", 26, "bold")


class AoS(tk.Tk):
        '''Class that contains everything in the Application '''
        def __init__(self, *args, **kwargs):
                self.uid = ''
                tk.Tk.__init__(self, *args, **kwargs)
                # title of the software
                tk.Tk.wm_title(self, "Ace of Spades")
                tk.Tk.wm_minsize(self, width=350, height=350)
                self.container = tk.Frame(self)

                self.container.pack(side="top", fill="both", expand = True)

                # configuration for the grid (0 is the min row or column)
                self.container.grid_rowconfigure(0, weight=1)
                self.container.grid_columnconfigure(0, weight=1)

                # the frame that is on the top is the one that is on the screen
                # the dictionary will contain the different screens
                self.frames = {}
                for frame in {"LoginScreen":LoginScreen,
                              "HomeScreen":HomeScreen,
                              "ProblemInterface":ProblemInterface,
                              "UserHome":UserHome,
                              "UserInterface":UserInterface,
                              "ViewUserAssignments":ViewUserAssignments,
                              "Attempt":Attempt,
                              "ViewPastAttempt":ViewPastAttempt,
                              "ViewAttempt":ViewAttempt,
                        "ViewStudentGrades":ViewStudentGrades, "ViewAssignments": ViewAssignments, "Leaderboard":Leaderboard}.items():                        
                        new_frame = frame[1](self.container, self)
                        self.frames[frame[0]] = new_frame
                        new_frame.grid(row=0, column=1, sticky="nsew")


                self.show_frame("LoginScreen")

        def show_frame(self, cont, uid=None, aid=None, atid=None):
                ''' function that determines which of the screens will be viewed by
                the user. This function uses tkraise, in order to bring the
                wanted screen to the front
                @param cont - name of the screen that needs to be displayed
                this is stored in the frames dictionary in self'''
                # get the frame from the dictionary
                frame = self.frames[cont]
                frame.tkraise()


                frame.set_uid(uid, aid, atid)

class LoginScreen(GUISkeleton):
        '''Creates a login screen, which will be the
        first screen of our Application'''
        def __init__(self, parent, controller):
                self.entry_keys = ["Email", "Password"]
                GUISkeleton.__init__(self, parent)
                # img = "logo2.jpg"
                # self.add_pic_panel(img)
                self.create_login_labels()
                self.create_entry_fields(controller)

        ''' 
    def add_pic_panel(self, pic):
        img = ImageTk.PhotoImage(Image.open(pic))
        label = Label(self, image=img)
        label.img = img # to keep the reference for the image.
        label.pack(side="left") # <--- pack
    '''
        def create_login_labels(self):
                '''creates the beginning labels'''
                # login text
                login_label = self.create_label(self, "Welcome to Ace! Please Log In: ",
                                                HOME_FONT, "Blue")
                #empty label for format
                # tk.Label(self, text="\n\n\n\n").pack()
                self.create_empty_label(5)
                login_label.pack(side="top", padx=10)

        def create_entry_fields(self, controller):
                ''' creates the entry fields for username and password'''
                # create the username and password fields
                i = 0
                myframe = ttk.Frame(self)       
                for field in self.entry_keys:
                        new_label = self.create_label(myframe, field, REGULAR_FONT)
                        new_label.grid(row=i, column=0, padx=10, sticky="W")
                        enterbox = self.create_entry(myframe, field)
                        if field == "Password":
                                # the show field of the password window makes sure that we only
                                # show '*' when somebody types in the password
                                enterbox["show"] = "*"
                        enterbox.grid(row=i, column=1)
                        i += 1
                self.create_login(myframe, controller)
                myframe.pack()

        def create_login(self, location, controller):
                '''creates login button'''
                button = self.create_button(location, "Login")
                button["command"] = lambda : self.verify_creds(controller)
                button.grid(row=3, column=1,pady=10, sticky="E")

        def verify_creds(self, controller):
                ''' used to verify  login credentials from the entry boxes
                of the LoginScreen '''
                i = 0;
                creds = []
                for field in self.entry_keys:
                        # get user's entries and store
                        creds.append(self.entry_fields[field].get())
                        i += 1
                # try getting user's details from database according to entered email
                try :
                        user_details = db.get_user_details_by_email(conn, creds[0])
                        # if the provided password matches the one stored
                        if (creds[1] == user_details[0][4]):
                                # check if user or admin
                                # print(user_details)
                                if (user_details[0][1] == 'student'):
                                        controller.show_frame('UserHome', user_details[0])
                                # move to home screen
                                elif (user_details[0][1] == 'admin'):
                                        controller.show_frame('HomeScreen',user_details[0])
                                else:
                                        showinfo("Fail", "User has no role")
                        else :
                                # otherwise pop msg to terminal
                                showinfo("Fail", "Wrong combo")
                        self.entry_fields["Email"].set('')
                        self.entry_fields["Password"].set('')
                # print msg to terminal if email doesnt exist
                except IndexError:
                        showinfo("Fail", "This email address is not in the system")

class UserHome(GUISkeleton):
        '''HomeScreen that appears if login person is user'''
        def __init__(self, parent, controller, uid=None):
                GUISkeleton.__init__(self, parent)
                self.buttons = ["View Assignments", "Logout"]
                self.init_window(controller)
                self.cont = controller

        def create_buttons(self, controller):
                for button in self.buttons:
                        new_button = self.create_button(self, button)
                        if button == "View Assignments":
                                new_button["command"] = lambda : controller.show_frame("ViewUserAssignments", self.uid)
                        elif (button == "Logout"):
                                new_button["command"] = (lambda :
                                                         controller.show_frame("LoginScreen"))
                        new_button.pack()


        def init_window(self, controller):
                '''initialises the window'''
                homescreen_label = self.create_label(self, "Home", HOME_FONT, "blue")
                self.create_empty_label(1)
                homescreen_label.pack()
                self.create_empty_label(2)
                self.create_buttons(controller)



        def set_uid(self, uid, aid=None, atid=None):
                self.uid = uid

class HomeScreen(GUISkeleton):
        ''' Homescreen that appears after the user logs in
        at the moment the homescreen is just a placeholder for some buttons'''
        def __init__(self, parent, controller, uid=None):
                GUISkeleton.__init__(self, parent)
                self.buttons = ["Add User", "Manage Question Bank","View Assignments",
                                "Student Grades", "Leaderboard", "Logout"]
                self.init_window(controller)

        def create_buttons(self, controller):
                ''' creates logout button'''
                # button will go to login screen
                for button in self.buttons:
                        new_button = self.create_button(self, button)
                        if button == "Add User":
                                new_button["command"] = lambda : controller.show_frame('UserInterface')
                        elif button == "Manage Question Bank":
                                new_button["command"] = lambda : controller.show_frame('ProblemInterface')
                        elif button == "View Assignments":
                                new_button["command"] = (lambda :
                                                         controller.show_frame('ViewAssignments'))
                        elif button == "Student Grades":
                                new_button["command"] = (lambda: 
                                                         controller.show_frame("ViewStudentGrades", self.uid))
                                
                        elif button == "Leaderboard": # LEADERBOARD
                                new_button["command"] = (lambda : controller.show_frame('Leaderboard'))
                    
                        elif button == "Logout":
                                new_button["command"] = (lambda :
                                                         controller.show_frame('LoginScreen'))
                        new_button.pack()

        def init_window(self, controller):
                ''' initialises the homescreen and its elements'''
                homescreen_label = self.create_label(self, "Home", HOME_FONT, "blue")
                # just to get the formatting correct
                # empty_label = ttk.Label(self, text="\n").pack()
                self.create_empty_label(1)
                homescreen_label.pack()
                self.create_empty_label(2)
                self.create_buttons(controller)
                

        def set_uid(self, uid, aid=None, atid=None):
                # del4_separated
                self.uid = uid
      

if __name__ == "__main__":
        conn = db.sqlite3.connect('ace.db')
        app = AoS()
        app.mainloop()

