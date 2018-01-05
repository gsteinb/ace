from tkinter import *

# create a new TK window
window = Tk()
# we dont want people to be able to change the size of the actual window
window.resizable(width=False, height=False)
window.title("Login")
# dimensions of the window
window.geometry("300x200")

# create the username and password fields
username_label = Label(window, text="Username")
username_entry = Entry(window)
password_label = Label(window, text="Password")
password_entry = Entry(window, show="*")

login_btn = Button(text="Login")

# use the grid layout managing function
# customize columns and rows
# empty label to create some space between the top 
# the entry labels
empty_label = Label(window, text="").grid(row=0, column=0, columnspan=5)
# place our created label inside the 
username_label.grid(row=1, column=2, columnspan=2)
username_entry.grid(row=1, column=4)
password_label.grid(row=2, column=2, columnspan=2)
password_entry.grid(row=2, column=4)
login_btn.grid(row=3, column=3)

window.mainloop()