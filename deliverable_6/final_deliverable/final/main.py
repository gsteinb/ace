import tkinter as tk
from tkinter import ttk, font,  Tk, Label, Button, Entry,\
     StringVar, DISABLED, NORMAL, END, W, E
from PIL import ImageTk, Image
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
<<<<<<< HEAD
                        "ViewStudentGrades":ViewStudentGrades, "ViewAssignments": ViewAssignments, "Leaderboard":Leaderboard}.items():                        
=======
                              "ViewStudentGrades":ViewStudentGrades, "ViewAssignments": ViewAssignments, "Leaderboard":Leaderboard}.items():                        
>>>>>>> working_final
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
                img = "logo1.jpg"
                self.add_pic_panel(img)
                self.create_login_labels()
                self.create_entry_fields(controller)
<<<<<<< HEAD
        
=======

>>>>>>> working_final
        def add_pic_panel(self, pic):
                img = ImageTk.PhotoImage(Image.open(pic))
                label = Label(self, image=img, bg="blue")
                label.img = img # to keep the reference for the image.
                label.pack(side="left", padx=15) 
        def create_login_labels(self):
                '''creates the beginning labels'''
                # login text
                login_label = self.create_label(self, "Welcome to Ace! Please Log In: ",
                                                HOME_FONT, "Blue")
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
                # show error if email doesnt exist
                except IndexError:
                        showinfo("Fail", "This email address is not in the system")

class UserHome(GUISkeleton):
        '''HomeScreen that appears if login person is user'''
        def __init__(self, parent, controller, uid=None):
                GUISkeleton.__init__(self, parent)
                self.buttons = ["View Assignments", "Leaderboard", "Logout"]
                self.init_window(controller)
                self.cont = controller
<<<<<<< HEAD
                
=======

>>>>>>> working_final
        def add_pic_panel(self, pic):
                img = ImageTk.PhotoImage(Image.open(pic))
                label = Label(self, image=img, bg="black")
                label.img = img # to keep the reference for the image.
                label.pack(side="right", padx=80)         

        def create_buttons(self, controller):
                frame3 = ttk.Frame(self)
                i = 1
                for button in self.buttons:
                        new_button = self.create_button(frame3, button)
                        if button == "View Assignments":
                                new_button["command"] = lambda : controller.show_frame("ViewUserAssignments", self.uid)

                        elif button == "Leaderboard": # LEADERBOARD
                                new_button["command"] = (lambda : self.leaderboard_refresh(controller))    
<<<<<<< HEAD
                                
=======

>>>>>>> working_final
                        elif (button == "Logout"):
                                new_button["command"] = (lambda :
                                                         controller.show_frame("LoginScreen"))
                        new_button.grid(row=i, column=1, padx=10, pady=2, sticky="NSEW")
                        i+=1    
                frame3.pack()

        def init_window(self, controller):
                '''initialises the window'''
                homescreen_label = self.create_label(self, "Home", HOME_FONT, "blue")
                self.create_empty_label(1)
                img = "student.jpg"
                self.add_pic_panel(img)                
                homescreen_label.pack()
                self.create_empty_label(2)
                self.create_buttons(controller)



        def set_uid(self, uid, aid=None, atid=None):
                self.uid = uid
<<<<<<< HEAD
                
=======

>>>>>>> working_final

        def leaderboard_refresh(self, controller):
                controller.show_frame('Leaderboard', self.uid)
                controller.frames['Leaderboard'].refresh()
                controller.frames['Leaderboard'].set_back("UserHome")
<<<<<<< HEAD
                
=======

>>>>>>> working_final

class HomeScreen(GUISkeleton):
        ''' Homescreen that appears after the user logs in
        at the moment the homescreen is just a placeholder for some buttons'''
        def __init__(self, parent, controller, uid=None):
                GUISkeleton.__init__(self, parent)
                self.buttons = ["Manage Users", "Manage Question Bank","View Assignments",
                                "Student Grades", "Leaderboard", "Logout"]
                self.init_window(controller)
<<<<<<< HEAD
                       
=======

>>>>>>> working_final
        def add_pic_panel(self, pic):
                img = ImageTk.PhotoImage(Image.open(pic))
                label = Label(self, image=img, bg="black")
                label.img = img # to keep the reference for the image.
                label.pack(side="right", padx=80) 
<<<<<<< HEAD
                
=======

>>>>>>> working_final
        def create_buttons(self, controller):
                button_frame = ttk.Frame(self)
                ''' creates logout button'''
                # button will go to login screen
                i = 1
                for button in self.buttons:
                        new_button = self.create_button(button_frame, button)
                        if button == "Manage Users":
                                new_button["command"] = lambda : controller.show_frame('UserInterface')
                        elif button == "Manage Question Bank":
                                new_button["command"] = lambda : controller.show_frame('ProblemInterface')
                        elif button == "View Assignments":
                                new_button["command"] = (lambda :
                                                         controller.show_frame('ViewAssignments'))
                        elif button == "Student Grades":
                                new_button["command"] = (lambda: 
                                                         controller.show_frame("ViewStudentGrades", self.uid))
<<<<<<< HEAD
                                
                        elif button == "Leaderboard": # LEADERBOARD
                                new_button["command"] = (lambda : self.leaderboard_refresh(controller))                
                    
                        elif button == "Logout":
                                new_button["command"] = (lambda :
                                                         controller.show_frame('LoginScreen'))
                                
=======

                        elif button == "Leaderboard": # LEADERBOARD
                                new_button["command"] = (lambda : self.leaderboard_refresh(controller))                

                        elif button == "Logout":
                                new_button["command"] = (lambda :
                                                         controller.show_frame('LoginScreen'))

>>>>>>> working_final
                        new_button.grid(row=i, column=1, padx=10, pady=2, sticky="NSEW")
                        i+=1 
                button_frame.pack()

        def init_window(self, controller):
                ''' initialises the homescreen and its elements'''
                homescreen_label = self.create_label(self, "Home", HOME_FONT, "blue")
                # just to get the formatting correct
                img = "admin2.jpg"
                self.add_pic_panel(img)
                self.create_empty_label(1)
                homescreen_label.pack()
                self.create_empty_label(1)
                self.create_buttons(controller)
<<<<<<< HEAD
                
=======

>>>>>>> working_final

        def set_uid(self, uid, aid=None, atid=None):
                # del4_separated
                self.uid = uid
<<<<<<< HEAD
        
=======

>>>>>>> working_final

        def leaderboard_refresh(self, controller):
                controller.show_frame('Leaderboard')
                controller.frames['Leaderboard'].refresh()
                controller.frames['Leaderboard'].set_back("HomeScreen")        
<<<<<<< HEAD
      

if __name__ == "__main__":
	conn = db.sqlite3.connect('ace.db')
	app = AoS()
	style = ttk.Style()
	style.configure('TFrame', background='#182F52')
	style.configure('TLabel' , background='#182F52', foreground='white')
	app.mainloop()
=======


if __name__ == "__main__":
        conn = db.sqlite3.connect('ace.db')
        app = AoS()
        style = ttk.Style()
        style.theme_use('classic') # Any style other than aqua
        style.configure('TFrame', background='#182F52')
        style.configure('TLabel' , background='#182F52', foreground='white')
        app.mainloop()
>>>>>>> working_final

