import tkinter as tk
from tkinter import ttk, font,  Tk, Label, Button, Entry,\
                    StringVar, DISABLED, NORMAL, END, W, E
from tkinter.messagebox import showinfo
import database_api as db

APP_HIGHLIGHT_FONT = ("Helvetica", 14, "bold")
REGULAR_FONT = ("Helvetica", 12, "normal")



def create_empty_label(location, num):
    ''' creates an empty label with the designated number of newlines
    create_empty_label(self, 1)
    GUI: \n              <-- this is the label created
        widget
    '''
    txt = ""
    for i in range(num):
        txt += "\n"
    label = tk.Label(location)
    label["text"] = txt
    label.pack()


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
        for F in (LoginScreen, HomeScreen, Problems, AddProblems,
                  RemoveProblems, AddUser, UpdateProblems):
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
        self.items = ["Username", "Password"]
        self.credentials = {}        
        tk.Frame.__init__(self, parent)
        self.create_login_labels()
        self.create_entry_fields(controller)


    def create_login_labels(self):
        '''creates the beginning labels'''
        # login text
        loginlbl = ttk.Label(self)
        loginlbl["text"] = "Welcome to Ace! Please Log In: "
        loginlbl["font"] = APP_HIGHLIGHT_FONT
        loginlbl["foreground"] = "blue"
        #empty label for format
        # tk.Label(self, text="\n\n\n\n").pack()
        create_empty_label(self, 4)
        loginlbl.pack()
        
    def create_entry_fields(self, controller):
        ''' creates the entry fields for username and password'''
        # create the username and password fields
        for field in self.items:
            myframe = tk.Frame(self)
            self.credentials[field] = StringVar()
            field_label = tk.Label(myframe)
            field_label["text"] = field
            field_label["font"] = REGULAR_FONT
            field_label.pack({"side": "left"}, padx=10)
            enterbox = tk.Entry(myframe)
            if field == "Password":
                # the show field of the password window makes sure that we only
                # show '*' when somebody types in the password                
                enterbox["show"] = "*"
            enterbox.pack({"side": "left"})
            enterbox["textvariable"] = self.credentials[field]
            myframe.pack()   
        self.create_login(controller)

    def create_login(self, controller):
        '''creates login button'''
        button = ttk.Button(self)
        button["text"] = "Login"
        button["command"] = lambda : self.verify_creds(controller)
        button.pack(pady=20)
        
    def verify_creds(self, controller):
        ''' used to verify login credentials from the entry boxes
        of the LoginScreen '''
        i = 0;
        creds = ["", ""]
        for field in self.items:
            # get user's entries and store
            creds[i] = self.credentials[field].get()

            i += 1
        # try getting user's details from database according to entered email
        try :
            user_details = db.get_user_details(conn, creds[0])
            # if the provided password matches the one stored
            if (creds[1] == user_details[0][4]) :
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
        # empty_label = ttk.Label(self, text="\n").pack()
        create_empty_label(self, 1)
        homescreen_label.pack()
        self.create_add_user_button(controller)
        self.manage_problems_button(controller)
        self.create_logout_button(controller)

        
class Problems(tk.Frame):
    '''Creates a prob screen, which will
    used by admin to add/edit and remove problems from database'''
    def __init__(self, parent, controller):
        self.functions = ["Add", "Remove", "Update", "Logout", "Back"]
        tk.Frame.__init__(self, parent)
        self.init_window(controller)

    def create_problem_buttons(self, controller):
        '''initialises the problem buttons'''
        for function in self.functions:
            #initialise the buttons
            button = ttk.Button(self)
            if ((function != "Logout") and (function != "Back")):
                button["text"] = "%s a Problem" % function
            else:
                button["text"] = "%s" % function
            # creates add button
            if function == "Add":
                button["command"] = lambda : controller.show_frame(AddProblems)
                # creates Remove button
            elif function == "Remove":
                button["command"] = (lambda : 
                                     controller.show_frame(RemoveProblems))
                # creates update button
            elif function == "Update":
                button["command"] = (lambda :
                                     controller.show_frame(UpdateProblems))
                # creates logout button
            elif function == "Logout":
                button["command"] = (lambda :
                                     controller.show_frame(LoginScreen))
                # creates back button
            elif function == "Back":
                button["command"] = (lambda :
                                     controller.show_frame(HomeScreen))
            button.pack()
            
    def create_options_label(self):
        ''' creates options label with spacing'''
        # Create the question label
        options_label = tk.Label(self)
        options_label["text"] = '''To make changes to the Question Bank,
        please select from the options below: '''
        options_label["font"] = APP_HIGHLIGHT_FONT
        options_label["foreground"] = 'blue'
        options_label["wraplength"] = 300
        options_label.pack()


    def init_window(self, controller):
        '''Initialises the GUI window and its elements
        Sets the different widgets that will be on the screen '''
        create_empty_label(self, 1)    
        self.create_options_label()
        create_empty_label(self, 1)    
        self.create_problem_buttons(controller)


class AddProblems(tk.Frame):
    '''Creates a prob screen, which will used
    by admin to add/edit and remove problems from '''
    def __init__(self, parent, controller):
        self.headers = ["subject", "question", "answer"]
        self.buttons = ["Add", "Back"]
        self.hentries = {}
        tk.Frame.__init__(self, parent)    
        self.init_window(controller)


    def create_entries(self):
        ''' creates entry boxes and their labels'''
        for header in self.headers:
            myframe = tk.Frame(self)
            self.hentries[header] = StringVar()
            # create the label
            header_label = tk.Label(myframe)
            # just to stay grammatically correct....
            if header != "answer":
                header_label["text"] = "Please enter a %s" % header
            else:
                header_label["text"] = "Please enter an %s" % header
            header_label["font"] = REGULAR_FONT
            header_label["foreground"] = "red"
            header_label.pack({"side": "left"})
            # create the entry box
            enterbox = Entry(myframe)
            enterbox.pack({"side" : "left"})
            enterbox["textvariable"] = self.hentries[header]
            myframe.pack()
    
    def create_buttons(self, controller):
        ''' creates the buttons for the Add Problem Screen'''
        myframe = tk.Frame(self)
        for button in self.buttons:
            # create a new frame
            new_button = ttk.Button(myframe)
            new_button["text"] = button
            if button == "Back":
                new_button["command"] = (lambda :
                                         controller.show_frame(Problems))
            elif button == "Add":
                # if add button is clicked retrieves input values
                new_button["command"] = self.press
            new_button.pack({"side": "left"}, pady=4, padx=5)
        myframe.pack()
            
    
    def init_window(self, controller):
        '''Initialises the GUI window and its elements
        Sets the different widgets that will be on the screen '''
        # empty label to create some space between the top
        # the entry labels
        create_empty_label(self, 2)
        self.create_entries()
        self.create_buttons(controller)
        self.feedback_label = tk.Label(self, text="")
        self.feedback_label.pack()            


    def press(self):
        #calls a function that tells the user if add was sucessfully,
        #displays appropriate message on label
        subjects = []
        for subject in self.headers:
            subjects.append(self.hentries[subject].get())
        message = db.add_problem(subjects[0], subjects[1],
                                 subjects[2], db.sqlite3.connect('ace.db'))
        print(message)
        self.feedback_label.config(text="Added Successfully!")

class RemoveProblems(tk.Frame):
    '''Screen to remove a problem from database'''
    def __init__(self, parent, controller):
        self.entries = {}
        self.buttons = ["Remove", "Back"]
        tk.Frame.__init__(self, parent)
        self.init_window(controller)
        
    def create_entries(self):
        '''creates label and entry side by side'''
        myframe = tk.Frame(self)
        self.entries["qid"] = StringVar()
        label = tk.Label(myframe)
        label["text"] = "Enter question ID to remove"
        label["font"] = REGULAR_FONT
        label.pack({"side": "left"})
        new_entry = tk.Entry(myframe)
        new_entry.pack({"side" : "left"})
        new_entry["textvariable"] = self.entries["qid"]
        myframe.pack()
        
    def create_buttons(self, controller):
        ''' adds the buttons for the RemoveProblem Screen'''
        myframe = tk.Frame(self)
        for button in self.buttons:
            new_button = ttk.Button(myframe)
            new_button["text"] = button
            if button == "Back":
                new_button["command"] = lambda : controller.show_frame(Problems)
            elif button == "Remove":
                new_button["command"] = self.press
            new_button.pack({"side" : "left"})
        myframe.pack()

    def init_window(self, controller):
        '''Initialises the GUI window and its elements
        Sets the different widgets that will be on the screen '''
        self.create_entries()
        self.create_buttons(controller)
        # this label will display the result from
        # a function that tells the user if remove was sucessful
        self.feedback_label = tk.Label(self, text = "")
        # place widges inside the grid
        self.feedback_label.pack()

    def press(self):
        #calls a function that tells the user if add was sucessfully,
        #displays appropriate message on label

        qid = self.entries["qid"].get()

        message = db.remove_problem(qid, db.sqlite3.connect('ace.db'))
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

        message = db.update_problem_question(qid, new_question, db.sqlite3.connect('ace.db'))
        print(message)

        self.feedback_label.config(text="Updated Successfully!")

    def press1(self):
        '''calls a function that tells the user if update of subject was sucessful
        and displays appropriate message on label'''

        qid = self.problem_entry.get()
        new_subject = self.problem_entry2.get()

        message = db.update_problem_subject(qid, new_subject, db.sqlite3.connect('ace.db'))
        print(message)

        self.feedback_label.config(text="Updated Successfully!")

    def press2(self):
        '''calls a function that tells the user if update of answer was sucessful
        and displays appropriate message on label'''

        qid = self.problem_entry.get()
        new_answer = self.problem_entry3.get()

        message = db.update_problem_answer(qid, new_answer, db.sqlite3.connect('ace.db'))
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
        number = db.add_user(self.role_entry.get(), self.name_entry.get(),
                      self.email_entry.get(), self.password_entry.get(), conn)
        self.role_entry.delete(0, END)
        self.name_entry.delete(0, END)
        self.email_entry.delete(0, END)
        self.password_entry.delete(0, END)   
        showinfo("Success", "ID of new user is: " + str(number))
        self.cont.show_frame(HomeScreen)

        
       

if __name__ == "__main__":
    conn = db.sqlite3.connect('ace.db')
    app = AoS()
    app.mainloop()
    