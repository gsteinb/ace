=========================================================

			README

=========================================================

*********************************************************


		ACE OF SPADES v 0.6


*********************************************************

Instructions for setting up program for testing:

This folder contains 2 types of files:
1. .py files - Python files that correspond to the different screens
2. ace.db - an initialised database with a first user set to:
	 (id=1, role=admin, password=1)
	 (id=2, role=student, password=2)

Place all files in the same folder
Install PIL pillow library for Images with Tkinter
Install Latex
Run main.py using python3 with library Tkinter installed
Use credentials: 1, 1 in the login fields or 2, 2 to login as student or admin respectively

After login,
 as an admin: you can manage new users, add problems manual, add random problems, manage problems,
 view assignments, edit assignments, View grades, view Leaderboard
As a student : you can complete an assignment, and save progress, view past attempts, view current attempts,
view hints, download sets as PDF, view the leaderboards

Info is stored on a SQLITE database

****************************************************

	             TESTING

****************************************************

Ace of Spades comes with Automated Tests
To Run the automated tests:

	open folder named "testing"
	execute each testfile using Python 3.x
		test_user.py
		test_login.py
		unittest_problem.py
		unittest_user_assignments.py
 
****************************************************

                  KNOWN BUGS

****************************************************

- Assume that subject has to be in the database in order to create assignments
	-> So problems with specific subjects have to be created before an assignment with that
	   subject can be created
- When sorting or filtering without choosing an assignment, there may be an error
# ace
