#This script takes a message written without punctuation or spaces and separates it into words.

import string

WORDLIST_FILENAME = '/Users/brandon.arnold/Documents/Python Projects/Message Decrypter/words.txt'
LOWERCASE_LETTERS = list(string.ascii_lowercase)

def load_words(file_name):
    """loads a .txt file of valid words, returns it as a list of individual words."""

    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    # print(inFile)
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    # print("  ", len(wordlist), "words loaded.")
    return wordlist


def is_word(word_list_dict, word):
    """takes a dict with keys of every valid English word (each word value = True), and a test word.
    Returns true if test word is in the dict (a valid word)."""
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|:;'<>?,./\"")
    # print("word = ", word)
    try:
        if word_list_dict[word]:
            return True
    except:
        return False



class Message(object):
    def __init__(self, text):
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)
        self.message_list = self.get_message_list()
        self.word_dict = self.get_word_dict()
        self.score = 0


    def get_message_text(self):
        # self.message_text = text
        return self.message_text

    def split_message_text(self):
        self.split_text = self.message_text.split()

    def get_valid_words(self):
        return self.valid_words.copy()
    
    def get_message_list(self):
        """converts message into a list of individual characters. Returns list"""
        message_list = list(self.message_text)
        return message_list
    
    def get_word_dict(self):
        """converts list of valid words into a Dict, returns Dict"""
        word_dict = {}
        for word in self.valid_words:
            word_dict[word] = True
        return word_dict

    def divide_message(self, lyst):
        """
        :type lyst: List[letters]
        :type message: List[words]
        Takes lyst (a list of letters to make words) and message (a list of valid words so far)
        Splits lyst until the first part makes a valid word.
        Sends remaining lyst to a new divide message method.
        Returns a valid word or None.
        """
        # print("Dividing Message")
        word = "".join(lyst)
        message = ""
        if is_word(self.word_dict, word):
            message += word
            self.score += 1
            return message
        else:
            test_list = []
            space_index = 1
            validWord = False
            # print("Testing ")
            while not validWord and space_index < len(lyst)-1:
                word = "".join(lyst[:space_index])
                # print(word)
                if is_word(self.word_dict, word):
                    test_list.append(word)
                    last_valid_index = space_index
                    validWord = True
                    nextWord = self.divide_message(lyst[space_index:])
                    if not nextWord:
                        validWord = False
                        # test_list.pop()
                    else:
                        self.score += 1
                        message += word
                        message += " " + nextWord
                        test_list.append(nextWord)
                        return message
                space_index += 1
                # print("space index = ", space_index)
            return None




