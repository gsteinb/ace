import unittest
from main import *
import tkinter as tk
from tkinter import ttk, font,  Tk, Label, Button, Entry,\
                    StringVar, DISABLED, NORMAL, END, W, E
# from PIL import ImageTk, Image
from tkinter.messagebox import showinfo
import database_api as db
from gui_skeleton import *
from user import *
from problem import *
from user_assignments import *
from attempt import *
from assignments import *

class TestLogin(unittest.TestCase):
    '''
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)
    '''        
    def test_email_blank(self):
        '''
        If the email is left blank, the login function should return a proper 
        message
        '''
        # create the main program
        aos = AoS()
        # fill in an arbitrary password
        aos.frames["LoginScreen"].entry_fields["Password"].set('3')
        # use the login function with empty email entry, store returned message
        msg = aos.frames["LoginScreen"].verify_creds(aos)
        # check whether we got the desired message
        self.assertEqual(msg, "email not in system")
        # kill the program
        aos.destroy()
        
    def test_email_not_in_system(self):
        '''
        If the email is not in the system, the login function should return a 
        proper message
        '''
        # create the main program
        aos = AoS()
        # fill the email entry with non-existing database value
        aos.frames["LoginScreen"].entry_fields["Email"].set('3')
        # use the login function with filled email entry, store returned message
        msg = aos.frames["LoginScreen"].verify_creds(aos)
        # check whether we got the desired message
        self.assertEqual(msg, "email not in system")
        # kill the program
        aos.destroy()
        
    def test_password_blank(self):
        '''
        If the password field is left blank, the login function should return a 
        proper message
        '''
        # create the main program
        aos = AoS()
        # fill the email entry with existing database value
        aos.frames["LoginScreen"].entry_fields["Email"].set('1')
        # use the login function with blank password entry, store returned message
        msg = aos.frames["LoginScreen"].verify_creds(aos)
        # check whether we got the desired message
        self.assertEqual(msg, "bad combo")
        # kill the program
        aos.destroy()
        
    def test_password_wrong(self):
        '''
        If the provided password is wrong, the login function should return a 
        proper message
        '''
        # create the main program
        aos = AoS()
        # fill the email entry with existing database value
        aos.frames["LoginScreen"].entry_fields["Email"].set('1')
        # fill the password entry with wrong password value
        aos.frames["LoginScreen"].entry_fields["Password"].set('2')        
        # use the login function with blank password entry, store returned message
        msg = aos.frames["LoginScreen"].verify_creds(aos)
        # check whether we got the desired message
        self.assertEqual(msg, "bad combo")
        # kill the program
        aos.destroy()
        
    def test_both_email_password_blank(self):
        '''
        If both the email and the password entry fields are left blank, the 
        login function should return a proper message
        '''
        # create the main program
        aos = AoS()
        # use the login function with both entries blank, store returned message
        msg = aos.frames["LoginScreen"].verify_creds(aos)
        # check whether we got the desired message
        self.assertEqual(msg, "email not in system")
        # kill the program
        aos.destroy()   
        
    def test_correct_combo_admin(self):
        '''
        If the email/password combination is correct and corresponds to a user
        of type admin, the login function should indicate that it is directing
        the user to the admin main menu
        '''
        # create the main program
        aos = AoS()
        # fill the email entry with existing database value for admin
        aos.frames["LoginScreen"].entry_fields["Email"].set('1')
        # fill the password entry with the correct password value for that user
        aos.frames["LoginScreen"].entry_fields["Password"].set('1')           
        # use the login function with both entries blank, store returned message
        msg = aos.frames["LoginScreen"].verify_creds(aos)
        # check whether we got the desired message
        self.assertEqual(msg, "directing to admin")
        # kill the program
        aos.destroy()   
        
    def test_correct_combo_student(self):
        '''
        If the email/password combination is correct and corresponds to a user
        of type student, the login function should indicate that it is directing
        the user to the student main menu
        '''
        # create the main program
        aos = AoS()
        # fill the email entry with existing database value for admin
        aos.frames["LoginScreen"].entry_fields["Email"].set('2')
        # fill the password entry with the correct password value for that user
        aos.frames["LoginScreen"].entry_fields["Password"].set('2')           
        # use the login function with both entries blank, store returned message
        msg = aos.frames["LoginScreen"].verify_creds(aos)
        # check whether we got the desired message
        self.assertEqual(msg, "directing to student")
        # kill the program
        aos.destroy() 


if __name__ == '__main__':
    unittest.main()