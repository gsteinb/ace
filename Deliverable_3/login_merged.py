import tkinter as tk
import database_api
from tkinter import ttk, font,  Tk, Label, Button, Entry, StringVar, DISABLED, NORMAL, END, W, E
from tkinter.messagebox import showinfo
from database_api import *

APP_HIGHLIGHT_FONT = ("Helvetica", 14, "bold")
REGULAR_FONT = ("Helvetica", 12, "normal")


class AoS(tk.Tk):
    '''Class that contains everything in the Application '''
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # title of the software
        tk.Tk.wm_title(self, "Ace of Spades")
        tk.Tk.wm_minsize(self, width=350, height=350)
        container = tk.Frame(self)
        
        container.pack(side="top", fill="both", expand = True)
        
        # configuration for the grid (0 is the min row or column)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        # the frame that is on the top is the one that is on the screen
        # the dictionary will contain the different screens
        self.frames = {}
        
        # this loop adds screens to the dictionary,
        # once we build more screens, add them to the tuple 
        # for F in TUPLE e.g. (LoginScreen, HomeScreen, DataBlaBLa)
        for F in (LoginScreen, HomeScreen, Problems, AddProblems, RemoveProblems, AddUser, UpdateProblems):
            # here F is the name of the Screen
            frame = F(container, self)
            self.frames[F] = frame
            # with grid you can assign columns and rows to your
            # sticky determines (alignment + stretch) 
            # stretch the window to north south east or west (n,s,e,w)
            frame.grid(row=0, column=0, sticky="nsew")            
            
        self.show_frame(LoginScreen)


    def show_frame(self, cont):
        ''' function that determines which of the screens will be viewed by
        the user. This function uses tkraise, in order to bring the
        wanted screen to the front
        @param cont - name of the screen that needs to be displayed
        this is stored in the frames dictionary in self'''
        # get the frame from the dictionary
        frame = self.frames[cont]
        frame.tkraise()
        


class LoginScreen(tk.Frame):
    '''Creates a login screen, which will be the 
    first screen of our Application'''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.credentials = {'Username' : '','Password': ''}
        
        '''creates the entry fields for username and password'''
        # login text
        loginlbl = ttk.Label(self, text ="Welcome to Ace! Please Log In: ",
                             font=APP_HIGHLIGHT_FONT, foreground="blue")  
        tk.Label(self, text="\n\n\n\n").pack()
        # create the username and password fields
        username_label = tk.Label(self, text="Username", font=REGULAR_FONT)
        self.username_entry = tk.Entry(self)
        password_label = tk.Label(self, text="Password", font=REGULAR_FONT)
        # the show field of the password window makes sure that we only
        # show '*' when somebody types in the password
        self.password_entry = tk.Entry(self, show="*")
        loginlbl.pack()
        username_label.pack()
        self.username_entry.pack()
        password_label.pack()
        self.password_entry.pack()      
        self.create_login(controller)

        
    def create_login(self, controller):
        '''creates login button'''
        button = ttk.Button(self)
        button["text"] = "Login"
        button["command"] = lambda : self.verify_creds(controller)
        button.pack(pady=20)
        
    def verify_creds(self, controller):
        # get user's entries and store
        u_email = self.username_entry.get()
        u_pass = self.password_entry.get()
        # reset the entry bars
        self.username_entry.delete(0, END)
        self.password_entry.delete(0, END)
        # try getting user's details from database according to entered email
        try :
            user_details = get_user_details(conn, u_email)
            # if the provided password matches the one stored
            if (u_pass == user_details[0][4]) :
                # move to home screen
                controller.show_frame(HomeScreen)
            else :
                # otherwise pop msg to terminal
                showinfo("Fail", "Wrong combo")
        # print msg to terminal if email doesnt exist
        except IndexError :
            showinfo("Fail", "This email address is not in the system")
  
    



class HomeScreen(tk.Frame):
    ''' Homescreen that appears after the user logs in
    at the moment the homescreen is just a placeholder for some buttons'''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.init_window(controller)
    
    def create_logout_button(self, controller):
        ''' creates logout button'''
        # button will go to login screen
        logout_btn = ttk.Button(self)
        logout_btn["text"] = "Logout"
        logout_btn["command"] = lambda : controller.show_frame(LoginScreen)
        logout_btn.pack()
    
    def manage_problems_button(self, controller):
        ''' creates edit problem button'''
        button = ttk.Button(self)
        button["text"] = "Manage Question Bank"
        button["command"] = lambda : controller.show_frame(Problems)
        button.pack()
        
    def create_add_user_button(self, controller):
        ''' creates add user button'''
        button = ttk.Button(self)
        button["text"] = "Add User"
        button["command"] = lambda : controller.show_frame(AddUser)
        button.pack()
    
    def init_window(self, controller):
        ''' initialises the homescreen and its elements'''
        homescreen_label = ttk.Label(self, text="Home", font=APP_HIGHLIGHT_FONT)
        # just to get the formatting correct
        empty_label = ttk.Label(self, text="\n").pack()
        homescreen_label.pack()
        self.create_add_user_button(controller)
        self.manage_problems_button(controller)
        self.create_logout_button(controller)

        
class Problems(tk.Frame):
    '''Creates a prob screen, which will used by admin to add/edit and remove problems from '''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.init_window(controller)

    def init_window(self, controller):
        '''Initialises the GUI window and its elements
        Sets the different widgets that will be on the screen '''

        # Create the question label
        options_label = tk.Label(self, text="To make changes to the Question Bank, please select from the options below: ",
                                 font=APP_HIGHLIGHT_FONT, foreground="blue", wraplength=300)

        # Creates the Problem-Set Methods
        add_btn = tk.Button(self, text="Add a Problem", command=lambda: controller.show_frame(AddProblems))
        remove_btn = tk.Button(self, text="Remove a Problem", command=lambda: controller.show_frame(RemoveProblems))
        update_btn = tk.Button(self, text="Update a Problem", command=lambda: controller.show_frame(UpdateProblems))
        # Creates Logout Button
        logout_btn = tk.Button(self, text="Logout", command=lambda: controller.show_frame(LoginScreen))
        # empty label to create some space between the top
        # the entry labels
        empty_label = tk.Label(self, text="\n").pack()
        # place our created label inside the

        options_label.pack()
        empty2_label = tk.Label(self, text="\n").pack()
        update_btn.pack()
        remove_btn.pack()
        add_btn.pack()
        logout_btn.pack()


class AddProblems(tk.Frame):
    '''Creates a prob screen, which will used by admin to add/edit and remove problems from '''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.init_window(controller)
        feedback_label = tk.Label(self, text="")
        feedback_label.pack()

    def init_window(self, controller):
        '''Initialises the GUI window and its elements
        Sets the different widgets that will be on the screen '''

        # creates a back button
        back_btn = tk.Button(self, text="Back", command=lambda: controller.show_frame(Problems))
        back_btn.pack(pady=20)
        # creates the subject label
        add_problem_label = tk.Label(self, text="Please enter the subject", font=REGULAR_FONT, foreground="red")
        self.problem_entry = tk.Entry(self)

        self.feedback_label = tk.Label(self, text="")

        # creates the question label
        add_problem_label1 = tk.Label(self, text="Please enter a new question", font=REGULAR_FONT, foreground="red")
        self.problem_entry1 = tk.Entry(self)
        self.feedback_label1 = tk.Label(self, text="")

        # creates the answer label
        add_problem_label2 = tk.Label(self, text="Please enter the answer", font=REGULAR_FONT, foreground="red")
        self.problem_entry2 = tk.Entry(self)
        self.feedback_label2 = tk.Label(self, text="")


        # empty label to create some space between the top
        # the entry labels
        empty_label = tk.Label(self, text="\n").pack()

        # Displays subject label on grid
        add_problem_label.pack()
        self.problem_entry.pack()
        self.problem_entry.focus_set()

        # Displays question label on grid
        add_problem_label1.pack()
        self.problem_entry1.pack()

        # Displays answer label on grid
        add_problem_label2.pack()
        self.problem_entry2.pack()
        self.problem_entry2.focus_set()

        # If "Add Button" is clicked, retrieves input values
        add_btn = ttk.Button(self, text="Add", command=self.press)
        # Displays Add Button on grid
        add_btn.pack(pady=20)

        self.feedback_label.pack()
        self.feedback_label1.pack()
        self.feedback_label2.pack()


    def press(self):
        #calls a function that tells the user if add was sucessfully,
        #displays appropriate message on label

        subject = self.problem_entry.get()
        question = self.problem_entry1.get()
        answer = self.problem_entry2.get()

        message = database_api.add_problem(subject, question, answer, sqlite3.connect('ace.db'))
        print(message)

        self.feedback_label.config(text="Added Successfully!")

class RemoveProblems(tk.Frame):
    '''Screen to remove a problem from database'''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.init_window(controller)

    def init_window(self, controller):
        '''Initialises the GUI window and its elements
        Sets the different widgets that will be on the screen '''
        back_btn = tk.Button(self, text="Back", command=lambda: controller.show_frame(Problems))
        back_btn.pack(pady=20)

        # remove the question label and button
        remove_problem_label = tk.Label(self, text="Enter question ID to remove", font=REGULAR_FONT, foreground="red")
        self.problem_entry = tk.Entry(self)
        remove_btn = ttk.Button(self, text="Remove", command=self.press)
        #this label will display the result from a function that tells the user if remove was sucessful
        self.feedback_label = tk.Label(self, text = "")
        # empty label to create some space between the top
        # the entry labels
        empty_label = tk.Label(self, text="\n").pack()
        # place widges inside the grid
        remove_problem_label.pack()
        self.problem_entry.pack()
        remove_btn.pack(pady=20)
        self.feedback_label.pack()

    def press(self):
        #calls a function that tells the user if add was sucessfully,
        #displays appropriate message on label

        qid = self.problem_entry.get()

        message = database_api.remove_problem(qid, sqlite3.connect('ace.db'))
        print(message)

        self.feedback_label.config(text="Removed Successfully!")
        
class UpdateProblems(tk.Frame):
    '''Screen to update a problem from database'''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.init_window(controller)

    def init_window(self, controller):
        '''Initialises the GUI window and its elements
        Sets the different widgets that will be on the screen '''
        back_btn = tk.Button(self, text="Back", command=lambda: controller.show_frame(Problems))
        back_btn.pack(pady=20)

        # creates "Update" buttons and labels
        update_problem_label = tk.Label(self, text="Enter question ID to update", font=REGULAR_FONT, foreground="red")
        self.problem_entry = tk.Entry(self)
        update_question_btn = ttk.Button(self, text="Update Question", command=self.press)
        self.problem_entry1 = tk.Entry(self)
        update_subject_btn = ttk.Button(self, text="Update Subject", command=self.press1)
        self.problem_entry2 = tk.Entry(self)
        update_answer_btn = ttk.Button(self, text="Update Answer", command=self.press2)
        self.problem_entry3 = tk.Entry(self)

        #this label will display the result from a function that tells the user if update was sucessful
        self.feedback_label = tk.Label(self, text = "")
        self.feedback_label1 = tk.Label(self, text = "")
        self.feedback_label2 = tk.Label(self, text = "")
        self.feedback_label3 = tk.Label(self, text = "")
        # empty label to create some space between the top
        # the entry labels
        empty_label = tk.Label(self, text="\n").pack()
        empty_label1 = tk.Label(self, text="\n").pack()
        empty_label2 = tk.Label(self, text="\n").pack()
        empty_label3 = tk.Label(self, text="\n").pack()

        # display id label on grid
        update_problem_label.pack()
        self.problem_entry.pack()

        # display question label on grid
        update_question_btn.pack()
        self.problem_entry1.pack()

        # display subject label on grid
        update_subject_btn.pack()
        self.problem_entry2.pack()

        # display answer label on grid
        update_answer_btn.pack()
        self.problem_entry3.pack()

        # display if update was successful
        self.feedback_label.pack()
        self.feedback_label1.pack()
        self.feedback_label2.pack()
        self.feedback_label3.pack()


    def press(self):
        '''calls a function that tells the user if update  of question was
        sucessful and displays appropriate message on label'''

        qid = self.problem_entry.get()
        new_question = self.problem_entry1.get()

        message = database_api.update_problem_question(qid, new_question, sqlite3.connect('ace.db'))
        print(message)

        self.feedback_label.config(text="Updated Successfully!")

    def press1(self):
        '''calls a function that tells the user if update of subject was sucessful
        and displays appropriate message on label'''

        qid = self.problem_entry.get()
        new_subject = self.problem_entry2.get()

        message = database_api.update_problem_subject(qid, new_subject, sqlite3.connect('ace.db'))
        print(message)

        self.feedback_label.config(text="Updated Successfully!")

    def press2(self):
        '''calls a function that tells the user if update of answer was sucessful
        and displays appropriate message on label'''

        qid = self.problem_entry.get()
        new_answer = self.problem_entry3.get()

        message = database_api.update_problem_answer(qid, new_answer, sqlite3.connect('ace.db'))
        print(message)

        self.feedback_label.config(text="Updated Successfully!")
        
class AddUser(tk.Frame):
    '''Creates a login screen, which will be the 
    first screen of our Application'''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.cont = controller
        self.credentials = {'Username' : '','Password': ''}
        
        '''creates the entry fields'''
        # login text
        loginlbl = ttk.Label(self, text="Please enter details for new user",
                             font=REGULAR_FONT, foreground="red")     
        
        # create the username and password lables and entries
        role_label = tk.Label(self, text="Role", font=REGULAR_FONT)
        name_label = tk.Label(self, text="Name", font=REGULAR_FONT)
        email_label = tk.Label(self, text="Email", font=REGULAR_FONT)
        password_label = tk.Label(self, text="Password", font=REGULAR_FONT) 
        
        self.role_entry = tk.Entry(self)
        self.name_entry = tk.Entry(self)
        self.email_entry = tk.Entry(self)
        self.password_entry = tk.Entry(self)
        
        self.add_user_button = Button(self, text="Add User", font=REGULAR_FONT, 
                                      command=self.add_user)
        
        # pack elements
        loginlbl.pack() 
        role_label.pack()
        self.role_entry.pack()
        name_label.pack()
        self.name_entry.pack()
        email_label.pack()
        self.email_entry.pack()
        password_label.pack()
        self.password_entry.pack()
        tk.Label(self, text="\n\n\n\n").pack()
        self.add_user_button.pack()
        
    def add_user(self):
        # print(self.user_name)
        number = add_user(self.role_entry.get(), self.name_entry.get(),
                      self.email_entry.get(), self.password_entry.get(), conn)
        self.role_entry.delete(0, END)
        self.name_entry.delete(0, END)
        self.email_entry.delete(0, END)
        self.password_entry.delete(0, END)   
        showinfo("Success", "ID of new user is: " + str(number))
        self.cont.show_frame(HomeScreen)

        
       

if __name__ == "__main__":
    conn = sqlite3.connect('ace.db')
    app = AoS()
    app.mainloop()
    
    logout

