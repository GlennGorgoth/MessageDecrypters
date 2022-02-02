"""guest_dict.py
author: Glenn Gorgoth

description: to save multiple versions of the code dictionary
for guessing different letters
"""

class GuessDictList():
    """a temp dictionary for guessing code words"""
    def __init__(self, dyct = None):
        self.dict_lyst = []
        if dyct is not None:
            self.dict_lyst.append(dyct)
        self.correct = False
    
    def add_dict(self, new_dict):
        """add a new dict of possible guesses to the list"""
        self.dict_lyst.append(new_dict)
    
    def remove_dict(self, old_dict):
        """remove a dict of possible guesses from the list"""
        self.dict_lyst.remove(old_dict)
    
    def get_lyst(self):
        return self.dict_lyst
    
    def get_dict(self, index):
        return self.dict_lyst[index]
    
    def get_size(self):
        return len(self.dict_lyst)
    
    def set_correct(self, correct_dict):
        if len(self.dict_lyst) > 1:
            self.dict_lyst = []
            self.dict_lyst.append(correct_dict)
        self.correct = True

class GuessDict():

    def __init__(self, old_dict, key = None, new_value = None):
        self.dyct = old_dict.copy()
        if key is not None and new_value is not None:
            self.dyct[key] = new_value
        self.score = 0
        self.highest = False
        self.one_words = {}
        self.correct = False

    def get_dict(self):
        return self.dyct
    
    def replace(self, key, new_value):
        self.dyct[key] = new_value
    
    def add_one_word(self, key, new_value = None):
        self.one_words[key] = new_value
