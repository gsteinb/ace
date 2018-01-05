import unittest
from main import *


class TestUser(unittest.TestCase):
        
    def test_all_fields_empty(self):
        # create the main program
        aos = AoS()        
        # use the add user function with all entries blank, store returned message
        msg = aos.frames["UserInterface"].add_user()
        # check whether we got the desired message
        self.assertEqual(msg, "blank entry")
        # kill the program
        aos.destroy() 
    
    def test_empty_role_add(self):
        # create the main program
        aos = AoS()        
        # set the name and email entries to contain string values
        aos.frames["UserInterface"].entry_fields["Name"].set('a')
        aos.frames["UserInterface"].entry_fields["Email"].set('a@')
        # use the add user function with blank role entry, store returned message
        msg = aos.frames["UserInterface"].add_user()
        # check whether we got the desired message
        self.assertEqual(msg, "blank entry")
        # kill the program
        aos.destroy() 
        
    def test_empty_name_add(self):
        # create the main program
        aos = AoS()        
        # set the role and email entries to contain string values
        aos.frames["UserInterface"].entry_fields["Role"].set('a')
        aos.frames["UserInterface"].entry_fields["Email"].set('a@')
        # use the add user function with blank name entry, store returned message
        msg = aos.frames["UserInterface"].add_user()
        # check whether we got the desired message
        self.assertEqual(msg, "blank entry")
        # kill the program
        aos.destroy() 
        
    def test_empty_email_add(self):
        # create the main program
        aos = AoS()        
        # set the role and name entries to contain string values
        aos.frames["UserInterface"].entry_fields["Role"].set('a')
        aos.frames["UserInterface"].entry_fields["Name"].set('a@')
        # use the add user function with blank email entry, store returned message
        msg = aos.frames["UserInterface"].add_user()
        # check whether we got the desired message
        self.assertEqual(msg, "blank entry")
        # kill the program
        aos.destroy() 
        
    def test_empty_role_update(self):
        # create the main program
        aos = AoS()        
        # clear the role entry for third user (test user)
        aos.frames["UserInterface"].roles[3].delete(0, 'end')
        # use the update user function with blank role entry, store returned message
        msg = aos.frames["UserInterface"].up_user(3)
        # check whether we got the desired message
        self.assertEqual(msg, "blank entry")
        
        # set the entry back
        aos.frames["UserInterface"].roles[3].insert(0, '1')
        
        # kill the program
        aos.destroy() 
        
    def test_empty_name_update(self):
        # create the main program
        aos = AoS()        
        # clear the name entry for third user (test user)
        aos.frames["UserInterface"].names[3].delete(0, 'end')
        # use the update user function with blank name entry, store returned message
        msg = aos.frames["UserInterface"].up_user(3)
        # check whether we got the desired message
        self.assertEqual(msg, "blank entry")
        
        # set the entry back
        aos.frames["UserInterface"].names[3].insert(0, '2')        
        
        # kill the program
        aos.destroy() 
    
    def test_empty_email_update(self):
        # create the main program
        aos = AoS()        
        # clear the email entry for third user (test user)
        aos.frames["UserInterface"].emails[3].delete(0, 'end')
        # use the update user function with blank email entry, store returned message
        msg = aos.frames["UserInterface"].up_user(3)
        # check whether we got the desired message
        self.assertEqual(msg, "blank entry")
        
        # set the entry back
        aos.frames["UserInterface"].emails[3].insert(0, '3')        
                
        # kill the program
        aos.destroy() 
        
    def test_invalid_role_add(self):
        # create the main program
        aos = AoS()        
        # set the name and email entries to contain string values
        aos.frames["UserInterface"].entry_fields["Name"].set('a')
        aos.frames["UserInterface"].entry_fields["Email"].set('a@')
        # set the role entriy to contain invalid value
        aos.frames["UserInterface"].entry_fields["Role"].set('1')
        # use the add user function with blank role entry, store returned message
        msg = aos.frames["UserInterface"].add_user()
        # check whether we got the desired message
        self.assertEqual(msg, "invalid role")
        # kill the program
        aos.destroy() 
    
    def test_invalid_role_update(self):
        # create the main program
        aos = AoS()        
        # fill the role entry with invalid value for third user (test user)
        aos.frames["UserInterface"].roles[3].delete(0, 'end')
        aos.frames["UserInterface"].roles[3].insert(0, '1')
        # use the update user function with blank role entry, store returned message
        msg = aos.frames["UserInterface"].up_user(3)
        # check whether we got the desired message
        self.assertEqual(msg, "invalid role")
        
        # set the entry back
        aos.frames["UserInterface"].roles[3].insert(0, 'student')
        
        # kill the program
        aos.destroy()
        
    def test_delete_user(self):
        pass
    
    def test_add_user(self):
        pass


if __name__ == '__main__':
    unittest.main(exit= False)