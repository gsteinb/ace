import unittest
import tkinter as tk
from tkinter import ttk, font,  Tk, Label, Button, Entry,\
                    StringVar, DISABLED, NORMAL, END, W, E
from tkinter.messagebox import showinfo
import database_api as db
from gui_skeleton import *
from problem import *
from main import *
import ast
from random import sample
import time
import sqlite3

conn = sqlite3.connect('ace.db')
row = db.num_of_rows("problems", conn)


class TestProblem(unittest.TestCase):

    ClassIsSetup = False
    TearedDown = False

    # Sets up by creating a problem and corresponding Problem Object
    def setUp(self):
        db.add_problem("math", "60+60", "120", conn)
        self.problem = Problem(row+1)

    # Test intialization of invalid problem objects
    def test_init(self):
        # Initialize a non-existant problem object
        self.assertRaises(IndexError, lambda: Problem(5000000))

        # Initialize a zero index problem object
        self.assertRaises(IndexError, lambda: Problem(0))

    def test_get_qid(self):
        # Retrieve the problem qid
        self.assertEqual(self.problem.get_qid(), row+1)

        # Test return type of problem qid
        self.assertEqual(isinstance(self.problem.get_qid(), int), True)


    def test_get_subject(self):
        # Retrieve the problem subject
        self.assertEqual(self.problem.get_subject(), "math")

        # Test return type of problem subject
        self.assertEqual(isinstance(self.problem.get_subject(), str), True)


    def test_get_question(self):
        # Retrieve the problem question
        self.assertEqual(self.problem.get_question(), "60+60")

        # Test return type of problem question
        self.assertEqual(isinstance(self.problem.get_question(), str), True)

    def test_get_answer(self):
        # Retrieve the problem answer
        self.assertEqual(self.problem.get_answer(), "120")

        # Test return type of problem asnwer
        self.assertEqual(isinstance(self.problem.get_answer(), str), True)

    # Clean up by removing problem after every method
    def tearDown(self):
        db.remove_problem(row+1, conn)



class TestAddingProblem(unittest.TestCase):
    ''' Test cases for Adding a Problem
    '''

    # Adds a problem with subject as empty string
    def test_empty_subject_add(self):
        db.add_problem("", "30+60", "42", conn)

    # Adds a problem with question as empty string
    def test_empty_question_add(self):
        db.add_problem("math", "", "42", conn)

    # Adds a problem with answer as empty string
    def test_empty_answer_add(self):
        db.add_problem("math", "30+60", "", conn)

    # Adds a valid problem
    def test_add_valid_problem(self):
        db.add_problem("math", "30+60", "42", conn)

    # Cleans up by removing added problems after every test case
    def tearDown(self):
        db.remove_problem(row+1, conn)


class TestRemovingProblem(unittest.TestCase):
    ''' Test cases for Removing a Problem
    '''

    # Adds and then deletes a valid problem
    def test_delete_problem(self):
        db.add_problem("math", "30+60", "42", conn)
        db.remove_problem(row+1, conn)

    # Tries to delete a non-existing problem
    def test_delete_non_existant_problem(self):
        self.assertRaises(sqlite3.OperationalError, lambda:db.remove_problem("hello", conn))


class TestUpdatingProblem(unittest.TestCase):
    ''' Test cases for Updating a Problem
    '''

    # Sets up by adding a new problem before every test case
    def setUp(self):
        db.add_problem("math", "30+60", "42", conn)

    # Updates the problem's subject with empty string
    def test_empty_subject_update(self):
        db.update_problem_subject(row+1, "", conn)

    # Updates the problem's question with empty string
    def test_empty_question_update(self):
        db.update_problem_question(row+1, "", conn)

    # Updates the problem's answer with empty string
    def test_empty_answer_update(self):
        db.update_problem_answer(row+1, "", conn)

    # Tries to update a non-existing problem's subject with empty string
    def test_update_non_existant_problem(self):
        self.assertRaises(sqlite3.OperationalError, lambda:db.update_problem_question("hello", "", conn))

    # Cleans up by removing the added problem after every test case
    def tearDown(self):
        db.remove_problem(row+1, conn)


if __name__ == "__main__":

    # Runs the test cases for Problem Object Getters
    unitTest = TestProblem()
    suite = unittest.TestLoader().loadTestsFromModule(unitTest)
    unittest.TextTestRunner().run(suite)

    # Runs the test cases for Adding New Problems
    unitTest1 = TestAddingProblem()
    suite = unittest.TestLoader().loadTestsFromModule(unitTest1)
    unittest.TextTestRunner().run(suite)

    # Runs the test cases for Removing Existing Problems
    unitTest2 = TestRemovingProblem()
    suite = unittest.TestLoader().loadTestsFromModule(unitTest2)
    unittest.TextTestRunner().run(suite)

    # Runs the test cases for Updating Existing Problems
    unitTest3 = TestUpdatingProblem()
    suite = unittest.TestLoader().loadTestsFromModule(unitTest3)
    unittest.TextTestRunner().run(suite)
