from question import Question
import random

class SimpleMathQuestion(Question):
    '''Question that is string representing a simple math question
    A simple math question is a question where every variable must correspond
    to a specific range or all variables correspond to one range of values
    This is also simple arithmetic questions,
    however brackets and nesting can be used but this class cannot solve for x
    There also can be no equal signs in the question'''
    
    def __init__(self, question, variables=None, var_range=None, specific=False):
        super().__init__(question, variables)
        # if we have given a variable range
        # then we want to set a range for the variables
        self.var_range = {}
        self.values_used = []
        self.is_parsed = False
        if (var_range != None and specific == False):
            self.set_var_range(var_range[0])
        elif (var_range != None and specific == True):
            self.set_var_specific(var_range)
            
            
    def set_var_range(self, var_range):
        '''sets the variable range. this is a list with the first element being
        the start, and the last element being the end of the interval inclusive
        @param var_range -> a list with a range of variables
        i.e. [0,100] means range 0 to 100
        '''
        for var in self.variables:
            self.var_range[var] = var_range
            
        
    def set_var_specific(self, var_range):
        '''sets the variable range based on a dictionary where the key is
        the name of the variable, and the variable ranges are a list
        @param var_range -> a nested list of variable ranges,
        each element in the nested list is a tuple of variable ranges
        i.e. [(0,2), (1,1000), (3,5)]'''
        if (self.variables != []):
            i = 0
            var = self.variables
            # set each variable to one of the var ranges
            for i in range(i, len(self.variables)):
                self.var_range[var[i]] = var_range[i]
                i += 1
                
        
    def parse_question(self):
        ''' a funtion that parses the question, and replaces any variables
        with the ranges that are given it only parses the question once'''
        if (self.is_parsed == False):
            question = self.question
            var = self.variables
            # check if the inputted ranges are valid
            if (self.are_ranges_valid()):
                for variable in var:
                    # find a replacement value as a string
                    new_value = self.produce_valid_value(variable)
                    question = question.replace(variable, new_value)
                self.question = question
                self.is_parsed = True
            else:       
                print("Sorry, the ranges you entered" +
                      " are too small for the number of variables")
    
    
    def are_ranges_valid(self):
        '''checks if the ranges given in the intiialisation are valid ranges,
        and the ranges do not overlap to a point where no unique values can be
        produced for the number unique variables given
        @return -> boolean if valid or not'''
        is_valid = False
        # get the number of variables
        num_vars = len(self.variables)
        # check the size of the var_ranges list
        size_ranges = len(self.var_range)
        # if var_ranges is empty, we cannot produce a valid parse 
        # for the question
        if (num_vars == size_ranges and size_ranges != 0):
            # create a set with the ranges
            range_set = self.ranges_set()
            # if the size of the set is the same as the number of variables
            # we have unique ranges for each variable
            # otherwise we want to check that we have unique ranges
            # set the range_of_values to num_vars
            range_of_values = num_vars
            if (len(range_set) == num_vars):
                range_of_values = 0
            else:
                # subtract the range of each element from range_of_values
                # if the !(range <= 0) then it is False 
                for element in range_set:
                    # we add the extra -1 because element 1 is inclusive
                    # if we have a valid range where element[0] <= element[1]
                    # we get a value of 0 or lower
                    rnge = element[0] - element[1] - 1 
                    range_of_values += rnge
            is_valid = (range_of_values <= 0) 
        return is_valid
            
    def ranges_set(self):
        '''creates a set of all the ranges that the user entered,
        this is used for verification, because the set ensures that each
        element is unique
        @returns -> unique set of ranges'''
        new_set = set([])
        for variable in self.variables:
            print(self.var_range[variable])
            new_set.add(self.var_range[variable])
        return new_set
            
        
    def produce_valid_value(self, variable):
        '''returns a value that is not already in the used values list
        as a result each variable will have a different value
        @param -> variable which is the variable needs a value 
        @return -> value not already used'''
        # the value range for this variable
        var_range = self.var_range[variable]
        value = ''
        # if we havent used any values
        if (self.values_used == []):
            # we can add any value to it
            value = random.randrange(var_range[0], var_range[1] + 1)
        else: 
            # get a new value given a range
            value = random.randrange(var_range[0], var_range[1] + 1)
            # check if we have this value already
            if (value in self.values_used):
                # get a new value until it is valid
                value = self.produce_valid_value(variable)
        # put the new value in the used list
        self.values_used.append(value)
        # turn the value into a string
        value = str(value)
        return value
    
    
    def get_answer(self):
        '''getter for the answer of the question
        @return -> the answer'''
        return self.answer
    
    
    def evaluate_answer(self):
        '''a function that determines the answer to the randomly
        generated question, and sets self.answer this function is only called
        after parsing'''
        try:
            self.answer = eval(self.question)
        except SyntaxError:
            self.answer = ''
 