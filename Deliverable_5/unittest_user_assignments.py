import unittest
from user_assignments import *
from tkinter import ttk, font,  Tk, Label, Button, Entry,\
                    StringVar, DISABLED, NORMAL, END, W, E
from tkinter.messagebox import showinfo
import database_api as db
import sqlite3

conn = sqlite3.connect('ace.db')
row = db.num_of_rows("assignments", conn)

class TestViewUserAssignments(unittest.TestCase):
    ''' Test cases for Viewing User Assignments
    '''

    # Sets up by adding a new assignment
    def setUp(self):
        db.add_assignment("a5", "subj1: 1+60", "2017/15/08", "0", conn)

    # Tests if correct assignment details returned
    def test_view_assign_details(self):
        test = db.get_assignment_details(conn, row+1)
        self.assertEqual(test, (row+1, "a5", "subj1: 1+60", "2017/15/08", 0))

    # Tests return type of assignment name
    def test_view_assign_name_type(self):
        test = db.get_assignment_details(conn, row+1)
        self.assertEqual(type(test[1]), str)

    # Tests return type of assignment formula
    def test_view_assign_formula_type(self):
        test = db.get_assignment_details(conn, row+1)
        self.assertEqual(type(test[2]), str)

    # Tests return type of assignment deadline
    def test_view_assign_deadline_type(self):
        test = db.get_assignment_details(conn, row+1)
        self.assertEqual(type(test[3]), str)

    # Tests return type of assignment visibility
    def test_view_assign_visibility_type(self):
        test = db.get_assignment_details(conn, row+1)
        self.assertEqual(type(test[4]), int)

    # Tests if non-existant assignment can be viewed
    def test_view_non_existant_assign(self):
        self.assertRaises(sqlite3.OperationalError, lambda:db.get_assignment_details(conn, "hello"))

    # Cleans up by removing the assignment after every test case
    def tearDown(self):
        db.remove_assign(row+1, conn)




class TestAddUserAttempts(unittest.TestCase):
    ''' Test cases for Adding User Attempts
    '''

    # Sets up by creating a new assignment table
    def setUp(self):
        # Create assignments a5
        db.create_assignment_table(row+1, conn)

    # Tests if a new attempt can be added
    def test_add_attempt(self):
        db.add_attempt("a"+str(row+1), 2, "[1,2,3]", "[60,0,2]", "100", "", conn)

    # Tests if an empty attempt can be added
    def test_add_empty_attempt(self):
        db.add_attempt("a"+str(row+1), 3, "[3,5,7]", "", "", "", conn)

    # Tests for duplicated submission dates
    def test_duplicate_submission_dates(self):
        db.add_attempt("a"+str(row+1), 3, "[3,5,7]", "[60,0,2]", "100", "2015/17/5/22", conn)
        db.add_attempt("a"+str(row+1), 3, "[5,5,5]", "[0,2,1]", "100", "2015/17/5/22", conn)

    # Tests adding an attempt for non-existing assignment
    def test_add_attempts_for_non_existant_assign(self):
        self.assertRaises(sqlite3.OperationalError, lambda:db.add_attempt("a"+str(row+10000), 3, "[3,5,7]", "[60,0,2]", "100", "2015/17/5/22", conn))

    # Cleans up by removing the assignment table created
    def tearDown(self):
        db.remove_table("a"+str(row+1), conn)


class TestViewUserAttempts(unittest.TestCase):
    ''' Test cases for Viewing User Attempts
    '''

    # Sets up by creating an assignment table and adding one attempt
    def setUp(self):
        db.create_assignment_table(row+1, conn)
        db.add_attempt("a"+str(row+1), 200, "[1,2,3]", "[60,0,2]", "100", "8", conn)

    # Tests if correct user attempts retrieved
    def test_get_user_attempts(self):
        test = db.get_user_attempts(str(row+1), 200, conn)
        self.assertEqual(test, [(1, 200, '[1,2,3]', '[60,0,2]', '100', '8')])

    # Tests if non-existant nth attempt is retrieved
    def test_get_non_existant_nth_attempt(self):
        self.assertRaises(IndexError, lambda:db.get_user_nth_attempt(row+1, 200, 10, conn))

    # Tests if correct nth attempt of user retrieved
    def get_user_nth_attempt(self):
        db.get_user_nth_attempt(row+1, 200, 1, conn)

    # Tests if correct progress info for an assignment is retrieved
    def test_get_user_assignment_progress(self):
        test = db.get_assignment_progress_for_user(row+1, 200, conn)
        self.assertEqual(test, ['[60', '0', '2]'])

    # Tests if grade and submission date exist together or not
    def test_view_graded_submission_upon_submit(self):

        test = db.get_user_attempts(str(row+1), 200, conn)
        for x in test:
            if x[4] != "":
                self.assertTrue(x[5] != "")
            if x[5] != "":
                self.assertTrue(x[4] != "")

    # Cleans up by removing the assignment table created
    def tearDown(self):
        db.remove_table("a"+str(row+1), conn)



class TestUpdateUserAttempts(unittest.TestCase):
    ''' Test cases for Updating User Attempts
    '''

    # Sets up by creating an assignment table and two attempts
    def setUp(self):
        db.create_assignment_table(row+1, conn)
        db.add_attempt("a"+str(row+1), 200, "[1,2,3]", "[60,0,2]", "10", "8", conn)
        db.add_attempt("a"+str(row+1), 200, "[2,22,5]", "[0,0,0]", "15", "8", conn)

    # Tests updating the nth attempt grade only
    def test_update_user_nth_attempt_grade(self):
        db.update_attempt_grade_for_user_for_nth_attempt(row+1, 200, 1, "20", conn)
        test = db.get_user_attempts(str(row+1), 200, conn)
        self.assertEqual(test[0][4], "20")

    # Tests updating grades of all of user's attempts
    def test_update_all_user_attempt_grades(self):
        db.update_attempt_grade_for_user(row+1, 200, "100", conn)
        test = db.get_user_attempts(str(row+1), 200, conn)
        self.assertEqual(test[0][4], "100")
        self.assertEqual(test[1][4], "100")

    # Tests updating progress info of all of user's attempt's
    def test_update_all_user_assignment_progress(self):
        db.update_assignment_progress_for_user(row+1, 200, "[42,42,42]", conn)
        test = db.get_user_attempts(str(row+1), 200, conn)
        self.assertEqual(test[0][3], "[42,42,42]")
        self.assertEqual(test[1][3], "[42,42,42]")

    # Tests updating a user's nth attempt progress info
    def test_update_user_nth_attempt_assignment_progress(self):
        db.update_assignment_progress_for_user_for_nth_attempt(row+1, 200, 1, "[1,1,4]", conn)
        test = db.get_user_attempts(str(row+1), 200, conn)
        self.assertEqual(test[0][3], "[1,1,4]")
        self.assertEqual(test[1][3], "[0,0,0]")

    # Tests updating a user's nth attempt submission date
    def test_update_user_nth_attempt_assignment_submission(self):
        db.update_assignment_submission_for_user_for_nth_attempt(row+1, 200, 2, "2018/15/04", conn)
        test = db.get_user_attempts(str(row+1), 200, conn)
        self.assertEqual(test[0][5], "8")
        self.assertEqual(test[1][5], "2018/15/04")

    # Cleans up by removing the added assignment table
    def tearDown(self):
        db.remove_table("a"+str(row+1), conn)



if __name__ == "__main__":
    # Runs the test cases for Viewing User Assignments
    unitTest = TestViewUserAssignments()
    suite = unittest.TestLoader().loadTestsFromModule(unitTest)
    unittest.TextTestRunner().run(suite)

    # Runs the test cases for Adding User Attempts
    unitTest1 = TestAddUserAttempts()
    suite = unittest.TestLoader().loadTestsFromModule(unitTest1)
    unittest.TextTestRunner().run(suite)

    # Runs the test cases for Viewing User Attempts
    unitTest2 = TestViewUserAttempts()
    suite = unittest.TestLoader().loadTestsFromModule(unitTest2)
    unittest.TextTestRunner().run(suite)

    # Runs the test cases for Updating User Attempts
    unitTest3 = TestUpdateUserAttempts()
    suite = unittest.TestLoader().loadTestsFromModule(unitTest3)
    unittest.TextTestRunner().run(suite)
