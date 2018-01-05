import sqlite3
import ast

conn = sqlite3.connect('ace.db')

# Create tables - only run once for each table
"""
c = conn.cursor()
c.execute('''CREATE TABLE users
          (id INTEGER PRIMARY KEY, role text, name text,
          email text, password text)''')

c.execute('''CREATE TABLE problems
          (id INTEGER PRIMARY KEY, subject text, question text, answer text, hint text)''')

c.execute('''CREATE TABLE assignments
          (id INTEGER PRIMARY KEY, name text, formula text, start text, deadline text, visible int)''') # LEADERBOARD
"""
def get_problem_details(conn, qid):
    """
    returns an array of arrays containing rows' values for each column
    conn is the is the sqlite3 connection objects, qid is the problem id
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM problems WHERE id=?", (qid,))

    rows = cur.fetchall()
    return rows

def get_problems_by_subj(subj, conn):
    """
    returns an array of arrays containing rows' values for each column
    conn is the is the sqlite3 connection objects, qid is the problem id
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM problems WHERE subject=?", (subj,))

    rows = cur.fetchall()

    return rows

def get_problems_by_subj(subj, conn):
    """
    returns an array of arrays containing rows' values for each column
    conn is the is the sqlite3 connection objects, qid is the problem id
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM problems WHERE subject=?", (subj,))

    rows = cur.fetchall()

    return rows

def get_user_details_by_email(conn, email):
    """
    returns an array of arrays containing rows' values for each column
    conn is the is the sqlite3 connection objects, uid is the user id
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email=?", (email,))

    rows = cur.fetchall()

    return rows

""" Problems Functions """
def get_problem_ids(conn):
    """
    returns an array of arrays containing rows' values for each column
    conn is the is the sqlite3 connection objects, qid is the problem id
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM problems")

    rows = cur.fetchall()
    ids = []
    for row in rows:
        ids.append(row[0])

    return ids

def add_problem(subject, question, answer, hint, conn):
    '''
    Adds a problem to the database. Returns a message of success.
    '''
    # create a cursor to database conn
    c = conn.cursor()

    # Insert a row of data
    c.execute("INSERT INTO problems (subject,question,answer,hint) VALUES ('" +
              subject + "','" + question + "','" + answer + "','" + hint + "')")

    # Save (commit) the changes
    conn.commit()
    return get_problem_ids(conn)[-1]

def remove_problem(qid, conn):
    '''
    Removes a problem from the database. Returns a message of success.
    '''
    c = conn.cursor()
    # Deletes a row of data
    c.execute("DELETE FROM problems WHERE id = " + str(qid))
    conn.commit()
    return "Removed problem " + str(qid) + " from database!"

def update_problem_question(qid, new_question, conn):
    '''
    Updates a problem's question on the database. Returns a message of success.
    '''
    c = conn.cursor()
    # Updates a question
    c.execute("UPDATE problems SET question = '" + new_question +
              "' WHERE id = " + str(qid))
    conn.commit()
    return "Updated problem " + str(qid) + " on database!"

def update_problem_answer(qid, new_ans, conn):
    '''
    Updates a problem's answer on the database. Returns a message of success.
    '''
    c = conn.cursor()
    # Updates an answer
    c.execute("UPDATE problems SET answer = '" + new_ans +
              "' WHERE id = " + str(qid))
    conn.commit()
    return "Updated answer to problem " + str(qid) + " on database!"

def update_problem_subject(qid, new_sub, conn):
    '''
    Updates a problem's subject on the database. Returns a message of success.
    '''
    c = conn.cursor()
    # Updates a subject
    c.execute("UPDATE problems SET subject = '" + new_sub +
              "' WHERE id = " + str(qid))
    conn.commit()
    return "Updated subject of problem " + str(qid) + " on database!"

def update_problem_hint(qid, new_hint, conn):
    '''
    Updates a problem's subject on the database. Returns a message of success.
    '''
    c = conn.cursor()
    # Updates a subject
    c.execute("UPDATE problems SET hint = '" + new_hint +
              "' WHERE id = " + str(qid))
    conn.commit()
    return "Updated hints for problem " + str(qid) + " on database!"

def get_question_details(conn, qid):
    """
    Returns an array of arrays containing rows' values for each column
    conn is the is the sqlite3 connection objects, qid is the question id
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM problems WHERE id=?", (qid,))

    rows = cur.fetchall()

    return rows

""" Users Functions """

def add_user(role, name, email, password, conn):
    '''
    Adds a user to the database. Returns a message of success.
    '''
    # create a cursor to database conn
    c = conn.cursor()

    # Insert a row of data
    c.execute("INSERT INTO users (role,name,email,password) VALUES ('" +
              role + "','" + name + "','" + email + "','" + password + "')")

    # Save (commit) the changes
    conn.commit()

    # return number of new user
    return get_user_details_by_email(conn, email)[0][0]

def remove_user(uid, conn):
    '''
    Removes a user from the database. Returns a message of success.
    '''
    c = conn.cursor()
    # Deletes a row of data
    c.execute("DELETE FROM users WHERE id = " + str(uid))
    conn.commit()
    return "Removed user " + str(uid) + " from database!"

def update_user_role(uid, new_role, conn):
    '''
    Updates a user role on the database. Returns a message of success.
    '''
    c = conn.cursor()
    # Updates a question
    c.execute("UPDATE users SET role = '" + new_role +
              "' WHERE id = " + str(uid))
    conn.commit()
    return "Updated user " + str(uid) + " to " + new_role + "!"

def update_user_name(uid, new_name, conn):
    '''
    Updates a username on the database. Returns a message of success.
    '''
    c = conn.cursor()
    # Updates a question
    c.execute("UPDATE users SET name = '" + new_name +
              "' WHERE id = " + str(uid))
    conn.commit()
    return "Updated user " + str(uid) + "'s username to " + new_name + "!"

def update_user_email(uid, new_email, conn):
    '''
    Updates a user's email on the database. Returns a message of success.
    '''
    c = conn.cursor()
    # Updates an answer
    c.execute("UPDATE users SET email = '" + new_email +
              "' WHERE id = " + str(uid))
    conn.commit()
    return "Updated user " + str(uid) + "'s email to " + new_email + "!"

def update_user_password(uid, new_password, conn):
    '''
    Updates a problem on the database. Returns a message of success.
    '''
    c = conn.cursor()
    # Updates a subject
    c.execute("UPDATE users SET password = '" + new_password +
              "' WHERE id = " + str(uid))
    conn.commit()
    return "Updated user " + str(uid) + "'s password to " + new_password + "!"


def get_user_details(conn, uid):
    """
    returns an array of arrays containing rows' values for each column
    conn is the is the sqlite3 connection objects, uid is the user id
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id=?", (uid,))

    rows = cur.fetchall()

    return rows

def get_user_details_by_email(conn, email):
    """
    returns an array of arrays containing rows' values for each column
    conn is the is the sqlite3 connection objects, uid is the user id
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email=?", (email,))

    rows = cur.fetchall()

    return rows

def get_user_ids(conn):
    """
    returns an array of arrays containing rows' values for each column
    conn is the is the sqlite3 connection objects, uid is the user id
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")

    rows = cur.fetchall()
    ids = []
    for row in rows:
        ids.append(row[0])

    return ids


''' *************** Assignments ********************* '''
def add_assignment(name, formula, start, deadline, visible, conn): # LEADERBOARD: ADDED start
    '''
    Adds an assignment to the database. Returns the id of the new assignment.
    '''
    # create a cursor to database conn
    c = conn.cursor()

    # Insert a row of data
    c.execute("INSERT INTO assignments (name,formula,start,deadline,visible) VALUES ('" +
              name + "','" + formula + "','" + start + "','" + deadline + "','" + visible + "')")

    # Save (commit) the changes
    conn.commit()

    # return the new assignment id
    return get_assignments_ids(conn)[-1]

def create_assignment_table(num, conn):
    # create a cursor to database conn
    c = conn.cursor()

    # create the table table query
    query = ("CREATE TABLE a" + str(num) + "(id INTEGER PRIMARY KEY, uid int, questions text, progress text, "+
             "grade text, submission_date text)")
    # execute querry
    c.execute(query)

    # Save (commit) the changes
    conn.commit()

def get_assignments_ids(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM assignments")

    rows = cur.fetchall()
    ids = []
    for row in rows:
        ids.append(row[0])

    return ids

def add_attempt(table_name, uid, problem_ids, progress, grade, submission_date, conn):
    '''
    Adds an assignment to the database. Returns the id of the new assignment.
    '''
    # need to take in table name and build querry properly


    # create a cursor to database conn
    c = conn.cursor()

    # Insert a row of data
    com = ("INSERT INTO " + str(table_name) + " (uid,questions,progress,grade,submission_date)"+
              "VALUES ('" + str(uid) + "','" + str(problem_ids) + "','" + str(progress) + "','" + str(grade) + "','" + str(submission_date) + "')")

    c.execute(com)

    # Save (commit) the changes
    conn.commit()

def get_user_attempts(table_name, uid, conn):
    '''
    return a list of user attempts entries for user with uid
    from the assignment with name table_nam
    '''
    cur = conn.cursor()
    cur.execute("SELECT * FROM " + 'a'+str(table_name) + " WHERE uid=" + str(uid))

    rows = cur.fetchall()

    return rows

def get_user_nth_attempt(aid, uid, n, conn):

    return get_user_attempts(str(aid), uid, conn)[n]

def get_assignment_details(aid, conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM assignments WHERE id=" + str(aid))

    rows = cur.fetchall()
    return rows[0]


def get_users_ids_assignment(aid, conn):
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT uid FROM " + "a"+str(aid))
    users = cur.fetchall()
    user_ids = []
    for user in users:
        user_ids.append(user[0])
    return user_ids	


def update_assignment_submission_for_user_for_nth_attempt(aid, uid, n, submission, conn):

    c = conn.cursor()
    # get id of the nth atempt
    atid = get_nth_attempt_id_for_user(aid, uid, n, conn)
    c.execute("UPDATE " + 'a'+str(aid) + " SET submission_date = '" + str(submission).
              split('.', 1)[0] +
              "' WHERE id = " + str(atid))
    conn.commit()  

def update_assignment_progress_for_user(aid, uid, new_progress, conn):

    c = conn.cursor()

    c.execute("UPDATE " + 'a'+str(aid) + " SET progress = '" + new_progress +
              "' WHERE uid = " + str(uid))
    conn.commit()
    
def update_assignment_progress_for_user_for_nth_attempt(aid, uid, n, new_progress, conn):

    c = conn.cursor()
    # get id of the nth atempt
    atid = get_nth_attempt_id_for_user(aid, uid, n, conn)
    c.execute("UPDATE " + 'a'+str(aid) + " SET progress = '" + str(new_progress).
              split('.', 1)[0] +
              "' WHERE id = " + str(atid))
    conn.commit()  
        

def get_assignment_progress_for_user(aid, uid, conn):

    cur = conn.cursor()
    cur.execute("SELECT * FROM " + 'a'+str(aid) + " WHERE uid=" + str(uid))

    rows = cur.fetchall()
    
    rows = rows[-1][3].split(',')    
    return rows

def get_solution_set(problem_set ,conn):
    cur = conn.cursor()
    solution_set = []
    problem_set = ast.literal_eval(problem_set)
    for p in problem_set:
        # get the solution stored for the problem with id p from the list of
        # problem_set
        s = get_problem_details(conn, p)[0][3]
        # add that solution to solution_set
        solution_set.append(s)
    
    #return solution_set
    return solution_set
        
def update_attempt_grade_for_user(aid, uid, new_grade, conn):

    c = conn.cursor()

    c.execute("UPDATE " + 'a'+str(aid) + " SET grade = '" + str(new_grade).
              split('.', 1)[0] +
              "' WHERE uid = " + str(uid))
    conn.commit()    
    
def update_attempt_grade_for_user_for_nth_attempt(aid, uid, n, new_grade, conn):

    c = conn.cursor()
    # get id of the nth atempt
    atid = get_nth_attempt_id_for_user(aid, uid, n, conn)
    c.execute("UPDATE " + 'a'+str(aid) + " SET grade = '" + str(new_grade).
              split('.', 1)[0] +
              "' WHERE id = " + str(atid))
    conn.commit()    
    
def get_nth_attempt_id_for_user(aid, uid, n, conn):
    # get all the attempts for the user id
    attempts = get_user_attempts(aid, uid, conn)
    # get the nth attempt
    a = attempts[n-1]
    # return it's id ([0])
    return a[0]

''' Leaderboard functionality '''
def get_user_by_grade(conn):
    """
    returns an array of arrays containing rows' values for each column
    conn is the is the sqlite3 connection objects, uid is the user id
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE role = 'student' ORDER BY grade DESC, time ASC")

    rows = cur.fetchall()
    ids = []
    for row in rows:
        ids.append(row[0])

    return ids

def get_latest_user_attempts(table_name, uid, conn):
    '''
    return a list of user attempts entries for user with uid
    from the assignment with name table_name
    '''
    cur = conn.cursor()
    cur.execute("SELECT * FROM " + 'a' + str(table_name) + " WHERE uid=" + str(uid) + " ORDER BY id DESC")

    rows = cur.fetchall()
    print(rows[0][5])
    return rows

def get_solution_set(problem_set ,conn):
    cur = conn.cursor()
    solution_set = []
    problem_set = ast.literal_eval(problem_set)
    for p in problem_set:
        # get the solution stored for the problem with id p from the list of
        # problem_set
        s = get_problem_details(conn, p)[0][3]
        # add that solution to solution_set
        solution_set.append(s)
    
    #return solution_set
    return solution_set
        
def update_attempt_grade_for_user(aid, uid, new_grade, conn):

    c = conn.cursor()

    c.execute("UPDATE " + 'a'+str(aid) + " SET grade = '" + str(new_grade).
              split('.', 1)[0] +
              "' WHERE uid = " + str(uid))
    conn.commit()    
    
def update_attempt_grade_for_user_for_nth_attempt(aid, uid, n, new_grade, conn):

    c = conn.cursor()
    # get id of the nth atempt
    atid = get_nth_attempt_id_for_user(aid, uid, n, conn)
    c.execute("UPDATE " + 'a'+str(aid) + " SET grade = '" + str(new_grade).
              split('.', 1)[0] +
              "' WHERE id = " + str(atid))
    conn.commit()    
    
def get_nth_attempt_id_for_user(aid, uid, n, conn):
    # get all the attempts for the user id
    attempts = get_user_attempts(aid, uid, conn)
    # get the nth attempt
    a = attempts[n-1]
    # return it's id ([0])
    return a[0]

def update_user_grade(uid, new_grade, conn):
    '''
    Updates a user's grade on the database. Returns a message of success.
    '''
    c = conn.cursor()
    # Updates a subject
    c.execute("UPDATE users SET grade = '" + str(new_grade) +
              "' WHERE id = " + str(uid))
    conn.commit()
    return "Updated user " + str(uid) + "'s grade to " + str(new_grade) + "!"

def update_user_time(uid, new_time, conn):
    '''
    Updates a user's time on the database. Returns a message of success.
    '''
    c = conn.cursor()
    # Updates a subject
    c.execute("UPDATE users SET time = '" + str(new_time) +
              "' WHERE id = " + str(uid))
    conn.commit()
    return "Updated user " + str(uid) + "'s time to " + str(new_time) + "!"

"""Testing"""

def remove_table(table_name, conn):
    cur = conn.cursor()
    cur.execute("DROP TABLE " + table_name)

    conn.commit()

def remove_assign(aid, conn):
    cur = conn.cursor()
    cur.execute("DELETE FROM assignments WHERE id=" + str(aid))

    conn.commit()
