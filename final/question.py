class Question:
    ''' a question object that will be used to produce Questions with parts
    that are variable, that the random generator will then be able
    to change'''
    
    def __init__(self, question, variables=None):
        '''init method, if there are no variables, we will keep the empty
        list in the storage'''
        # this is a list of variables that the user will be able to enter
        # when parsing the strings this is what is used
        # if using a text question, do not use the variable a or I,
        # try to use variables that are not words by themselves
        self.variables = []   
        # string where the question is
        self.question = question
        if (variables != None):
            self.variables = variables
    
    
    def __str__(self):
        ''' the string method of the Question Object, this will ensure
        that we are printing the question if we all print on a question object
        @returns -> string representing the question
        '''
        return self.question
    
    
    def get_variables(self):
        '''getter that gets the variables in the question
        @returns -> list of variables'''
        return self.variables
    
    
    def get_question(self):
        '''getter for the question of the Question object
        @returns -> string representing the question'''
        return self.question
