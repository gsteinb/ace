=========================================================

			README

=========================================================

*********************************************************


		ACE OF SPADES v 0.5


*********************************************************

Instructions for setting up program for testing:

This folder contains 2 types of files:
1. .py files - Python files that correspond to the different screens
2. ace.db - an initialised database with a first user set to:
	 (id=1, role=admin, password=1)
	 (id=2, role=student, password=2)

Place all files in the same folder
Run main.py using python3 with library Tkinter installed
Use credentials: 1, 1 in the login fields or 2, 2 to login as student or admin respectively
After login,
 as an admin: you can add new users, add problems, remove problems and edit problems,
 view assignments, edit assignments, View grades
As a student : you can submit, and save progress, view the leaderboards


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

- Leaderboard: Leaderboard is not functioning at this moment
- When sorting or filtering without choosing an assignment, there may be an error
# ace
