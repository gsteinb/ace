import sqlite3

conn = sqlite3.connect('ace.db')

# Create tables - only run once for each table
"""
c = conn.cursor()
c.execute('''CREATE TABLE users
          (id INTEGER PRIMARY KEY, role text, name text,
          email text, password text)''')

c.execute('''CREATE TABLE problems
          (id INTEGER PRIMARY KEY, subject text, question text, answer text)''')

c.execute('''CREATE TABLE assignments
          (id INTEGER PRIMARY KEY, name text, formula text, deadline text, visible int)''')
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

def add_problem(subject, question, answer, conn):
    '''
    Adds a problem to the database. Returns a message of success.
    '''
    # create a cursor to database conn
    c = conn.cursor()

    # Insert a row of data
    c.execute("INSERT INTO problems (subject,question,answer) VALUES ('" +
              subject + "','" + question + "','" + answer + "')")

    # Save (commit) the changes
    conn.commit()
    return "Added problem of subject " + subject + " to database!"

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
def add_assignment(name, formula, deadline, visible, conn):
    '''
    Adds an assignment to the database. Returns the id of the new assignment.
    '''
    # create a cursor to database conn
    c = conn.cursor()

    # Insert a row of data
    c.execute("INSERT INTO assignments (name,formula,deadline,visible) VALUES ('" +
              name + "','" + formula + "','" + deadline + "','" + visible + "')")

    # Save (commit) the changes
    conn.commit()
    
    # return the new assignment id
    return get_assignments_ids(conn)[-1]
    
def create_assignment_table(num, conn):
    # create a cursor to database conn
    c = conn.cursor()
    
    # create the table table query
    query = ("CREATE TABLE a" + str(num) + "(uid int, questions text, progress text, "+
             "grade text)")
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

def add_attempt(table_name, uid, problem_ids, conn):
    '''
    Adds an assignment to the database. Returns the id of the new assignment.
    '''
    # need to take in table name and build querry properly
    
    
    # create a cursor to database conn
    c = conn.cursor()

    # Insert a row of data
    c.execute("INSERT INTO " + str(table_name) + " (uid,questions,progress,grade)"+
              "VALUES ('" + str(uid) + "','" + str(problem_ids) + "','','')")

    # Save (commit) the changes
    conn.commit()
    
def get_user_attempts(table_name, uid, conn):
    '''
    return a list of user attempts entries for user with uid
    from the assignment with name table_name
    '''
    cur = conn.cursor()
    cur.execute("SELECT * FROM " + str(table_name) + " WHERE uid=" + str(uid))
    
    rows = cur.fetchall()
    
    return rows

def get_user_first_attempt(aid, uid, conn):

    return get_user_attempts("a"+str(aid), uid, conn)[0]

def get_assignment_details(aid, conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM assignments WHERE id=" + str(aid))
 
    rows = cur.fetchall()

        
    return rows[0]