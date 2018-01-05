import tkinter as tk
from tkinter import ttk, font,  Tk, Label, Button, Entry,\
                    StringVar, DISABLED, NORMAL, END, W, E
from tkinter.messagebox import showinfo
import database_api as db
from gui_skeleton import *
APP_HIGHLIGHT_FONT = ("Helvetica", 14, "bold")
REGULAR_FONT = ("Helvetica", 12, "normal")
NICE_BLUE = "#3399FF"


class UserSkeleton(GUISkeleton):
    ''' class that inherits from GUISkeleton
    but comes with a set_uid method that the user screens are going use'''
    def __init__(self, parent):
        GUISkeleton.__init__(self, parent)


    def set_uid(self, uid=None, aid=None, atid=None):
	    '''sets the UID for the current user'''
	    self.uid = uid
	    self.aid = aid
	    self.atid = atid    
	    self.gen_rows(uid, aid, atid)


    def pass_ids(self, screen, uid=None, aid=None, atid=None):
	    '''shows the ViewUserAssignment screen and passes the 
	    uid from the controller to the screen'''
	    self.controller.show_frame(screen)
	    self.controller.frames[screen].set_uid(uid, aid, atid)    