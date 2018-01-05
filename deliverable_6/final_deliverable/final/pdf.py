import argparse
import os
import subprocess
import sqlite3
import database_api as db
import ast
from tkinter.messagebox import showinfo

conn = sqlite3.connect('ace.db')

''' Class that creates the Latex PDF from generated .tex file'''
class CreatePDF():

    def __init__(self, uid, aid, atid):
        self.uid = uid
        self.aid = aid
        self.atid = atid

        # The template latex for the pdf document
        self.content = r'''\documentclass[a4paper, 11pt]{article}
        \usepackage[margin=1.0in]{geometry}
        \usepackage{tikz}
        \usepackage{amsmath}
        \usepackage{amsfonts}
        \usepackage{amssymb}
        \begin{document}
        \noindent
        \large\textbf{\large %(course)s \hfill \textbf{\large Deadline: \underline{%(deadline)s \\}}}
        \newline
        \newline
        \textbf{\large %(title)s \hfill \textbf{\large Name: \underline{%(name)s \\}}}
        \newline
        \newline
        \newline
        \textbf{\large Problems: }
        \newline
        \newline
        '''

    def substitue_values(self):
        ''' This method substitutes values such as course, assign #, deadline,
        and name into the latex expression and ends it. Then it proceeds to
        create the '.tex' file.
        '''

        # Substitues values into latex expression
        parser = argparse.ArgumentParser()
        parser.add_argument('-c', '--course', default='STAB22')
        parser.add_argument('-t', '--title', default='Assignment: ' + str(self.aid))
        parser.add_argument('-n', '--name', default = db.get_user_details(conn, self.uid)[0][2])
        parser.add_argument('-d', '--deadline', default=db.get_assignment_details(self.aid, conn)[3])

        args = parser.parse_args()

        # End the document
        self.content += r'\end{document}'
        self.createTexFile(args)


    def createTexFile(self, args):
        # Create the .tex file
        with open('assign' + str(self.aid) + '.tex','w') as f:
            f.write(self.content%args.__dict__)

        self.createPDF()

    def addOnLatex(self):
        '''This method takes problems from the database and attaches them
        to the latex expression.
        '''
        # Fetch the user attempts for assignment
        ids = db.get_user_nth_attempt(self.aid, self.uid, -1, conn)[2]
        ids = ast.literal_eval(ids)

        # Loop through problems
        for qid in ids:

            # For each problem, append it to latex expression
            problem = db.get_problem_details(conn, qid)[0][2]

            self.content += problem + r'\newline\newline' + r'\begin{tikzpicture}' + r'\draw (0,0) -- (17,0) -- (17,3) -- (0,3) -- (0,0);' +r'\end{tikzpicture}' + r'\newline\newline\newline\newline'

        self.substitue_values()


    def createPDF(self):
        ''' This method alerts the operating system to execute pdflatex
        command on the ".tex" file that was created.
        '''

        # Enters the pdf-convert commands into cmd line.
        cmd = ['pdflatex', '-interaction', 'nonstopmode', 'assign' + str(self.aid) + '.tex']
        proc = subprocess.Popen(cmd)
        proc.communicate()
        retcode = proc.returncode

        # Check if anything went wrong:
        if not retcode == 0:
            # If so, delete the bad pdf and raise error
            os.unlink('assign' + str(self.aid) + '.pdf')
            raise ValueError('Error {} executing command: {}'.format(retcode, ' '.join(cmd)))

        # If all good, then remove the un-needed .tex, .log and .aux files
        os.unlink('assign' + str(self.aid) + '.tex')
        os.unlink('assign' + str(self.aid) + '.log')
        os.unlink('assign' + str(self.aid) + '.aux')

        showinfo("Downloaded", "The assignment has downloaded to your computer")
