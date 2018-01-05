from tkinter import *
from tkinter import ttk
from tkinter import font

root = Tk()
root.title("Ace of Spades")

content = ttk.Frame(root)
frame = ttk.Frame(content, borderwidth=5, relief="sunken", width=300, height=300)


appHighlightFont = font.Font(family='Helvetica', size=14, weight='bold')
regularFont = font.Font(family='Helvetica', size=12, weight='normal')


loginlbl = ttk.Label(content, text ="Please Log In: ", font=appHighlightFont)
namelbl = ttk.Label(content, text="Username", font=regularFont)
name = ttk.Entry(content)
login = ttk.Button(content, text="Log in", font=regularFont)


content.grid(column=0, row=0)
frame.grid(column=0, row=0, columnspan=4, rowspan=3)
loginlbl.grid(column=1, row=0, columnspan=2, rowspan=1)
namelbl.grid(column=2, row=1, columnspan=1)
name.grid(column=3, row=1, columnspan=1)
login.grid(column=3, row=2)


root.mainloop()

