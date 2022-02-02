"""
Message Decrypter
author: Glenn Gorgoth
date: Sept 1, 2020

Takes a letter-swap coded message (such as those found in newspaper cryptochallenges)
and decrypts it.

"""

import string
import time
import collections
from guess_dict import GuessDict 

WORDLIST_FILENAME = 'words.txt'
LOWERCASE_LETTERS = list(string.ascii_lowercase)


def load_words(file_name):
    """loads a .txt file of valid words, returns it as a list of individual words."""

    inFile = open(file_name, 'r')
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    return wordlist


def is_word(word_list_dict, word):
    """takes a dict with keys of every valid English word (each word value = True), and a test word.
    Returns true if test word is in the dict (a valid word)."""
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|:;'<>?,./\"")
    try:
        if word_list_dict[word]:
            return True
    except:
        return False

def sort_by_highest_score(lyst):
    """takes a lyst of guess_dicts, compares their scores,
    returns a list of dicts in order of score from highest to lowest"""
    dyct_of_dycts = {}
    for dyct in lyst:
        dyct_of_dycts[dyct] = dyct.score
    sorted_dycts = sorted(dyct_of_dycts.items(), key=lambda x: x[1], reverse=True)
    list_of_dycts = []
    for dyct in sorted_dycts:
        list_of_dycts.append(dyct[0])
    return list_of_dycts

class Message(object):
    def __init__(self, text):
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def get_message_text(self):
        # self.message_text = text
        return self.message_text

    def split_message_text(self):
        self.split_text = self.message_text.split()

    def get_valid_words(self):
        return self.valid_words.copy()

class CiphertextMessage(Message):
    def __init__(self, text):
        Message.__init__(self, text)
        self.message_text = text.lower()
        self.valid_words = self.get_valid_words()
        self.lists_of_valid_words = self.make_word_lists()
        self.valid_words_dict = self.make_word_dict()
        self.lowercase_letters = list(string.ascii_lowercase)
        self.uppercase_letters = list(string.ascii_uppercase)
        self.char_list = list(self.message_text)
        self.letter_list = list(filter((" ").__ne__, self.char_list))
        self.frequency_counter = dict(collections.Counter(self.letter_list))
        self.split_words = self.message_text.split()
        self.list_of_words = []
        for i in self.split_words:
            no_punct = i.strip(" ,.")
            self.list_of_words.append(no_punct)
        self.list_of_words_by_length = self.sort_words_by_length()
        self.next_word_index = 0
        self.guess_letters = []
        self.longest_word = self.list_of_words_by_length[-1]
        self.score = 0

    def make_word_dict(self):
        """takes list of valid words, creates a dict with those words as keys, 
        and values set to True."""
        valid_word_dict = {}
        for word in self.valid_words:
            valid_word_dict[word] = True
        return valid_word_dict

    def make_word_lists(self):
        """divides all valid words into separate lists of words of the same length.
        returns a list of those lists"""
        size = 1
        lists_of_words = []
        list_of_same_size = []
        for word in self.valid_words:
            if len(word) == size:
                list_of_same_size.append(word)
            else:
                lists_of_words.append(list_of_same_size.copy())
                size = len(word)
                list_of_same_size = []
                list_of_same_size.append(word)
        lists_of_words.pop(0)
        lists_of_words.pop(0)
        return lists_of_words

    def get_list_of_words(self):
        return self.list_of_words.copy()

    def match_with_gaps(self, test_word, real_word, letters_guessed):
        """takes a test word, a valid word, and a list of known values. 
        If all characters in the test word match those in valid word, 
        or haven't been solved yet (represented by '!'), returns true. If
        real word contains any letters currently used as values for something else,
        returns False.
        """
        l = len(test_word)
        count = 0
        has_letter = False
        char_index = 0
        for new_letter in test_word:
            real_letter = real_word[char_index]
            if new_letter == real_letter:
                count += 1
                has_letter = True
            elif new_letter == "!":
                if real_letter not in letters_guessed:
                    count += 1
            char_index += 1
        return l == count

    def show_possible_matches(self, test_word, test_dict):
        """takes a code word, and a dict of values, translates the word using those values,
        returns a list of possible valid words that might match with the currently known values."""
        test_list = list(test_word)
        dict_key = list(test_dict.keys())
        dict_values = list(test_dict.values())
        display_word = []
        possible_matches = []
        for i in test_list:
            if test_dict[i] != '*':
                i_index = dict_key.index(i)
                display_word.append(dict_values[i_index])
            else:
                display_word.append("!")
        dis_word_str = "".join(display_word)
        for j in self.lists_of_valid_words[len(test_word)-1]:
            if self.match_with_gaps(dis_word_str, j, dict_values) == True:
                if self.no_reused_letters(test_word, dis_word_str, j, dict_values):
                    possible_matches.append(j)
        return possible_matches
    
    def no_reused_letters(self, org_word, code, word, lyst):
        """takes a code word, a translation of that word, a valid word, and a list of current values for the dict.
        if the valid word contains letters already represented as values elsewhere in the dict,
        but not used in the code word, returns false."""
        score = 0
        used_letters = {}
        code_word_dict = dict(zip(org_word, code))
        i = 0
        for c in word:
            if c in lyst:
                if c not in code:
                    return False
                if code[i] != word[i]:
                    return False
            i += 1
        return True
    
    def build_next_word_dicts(self, code_word, old_dyct):
        """takes in a str of a word in the code, 
        returns a list of dictionaries with all possible values 
        for the letters in the word"""
        word_len = len(code_word)
        letters = list(code_word)
        # builds list of all letters in code word without duplicates
        letters_only_once = collections.Counter(letters).most_common()
        letters_list = []
        for i in letters_only_once:
            letters_list.append(i[0])
        unique_letters_len = len(letters_list)
        dict_list = []
        use_possible_matches = False
        value_list = list(old_dyct.values())
        for v in value_list:
            if v != '*':
                use_possible_matches = True

        if use_possible_matches:
            possible_matches = self.show_possible_matches(code_word, old_dyct)
        else:
            possible_matches = self.lists_of_valid_words[len(code_word) - 1] 
        new_value_list = self.build_dicts_from_valid_words(word_len, unique_letters_len, possible_matches)
        for new_values in new_value_list:
            new_dict = old_dyct.copy()
            key_index = 0
            for key_letter in letters_list:
                new_dict[key_letter] = new_values[key_index]
                key_index += 1
            if self.is_word_valid(code_word, new_dict):
                dict_list.append(new_dict)
        print('returning Dict with ', len(dict_list), ' combinations')
        return dict_list

    def build_dicts_from_valid_words(self, word_length, unique_letters_len, possible_matches):
        """takes length of code word, and # of all unique letters in code word.
        Returns a list of lists, each containing possible values for the code letters,
        so that each set of values could be used to create a particular valid word"""
        lists_of_values = []
        for valid_word in possible_matches:
            unique_letters = collections.Counter(valid_word).most_common()
            unique_letters_list = []
            for i in unique_letters:
                unique_letters_list.append(i[0])
            if word_length == len(valid_word) and unique_letters_len == len(unique_letters_list):
                new_values = []
                for c in unique_letters_list:
                    new_values.append(c)
                lists_of_values.append(new_values)
        return lists_of_values
    
    def sort_words_by_length(self):
        """sorts all the words in the code message in order of smallest to largest"""
        test_num = 0
        list_of_words_by_length = []
        word_length_dict = {}
        for word in self.list_of_words:
            if len(word) <= 10:
                word_length_dict[word] = len(word)
        sorted_words = sorted(word_length_dict.items(), key=lambda x: x[1])
        for i in sorted_words:
            list_of_words_by_length.append(i[0])
        return list_of_words_by_length
    
    def is_word_valid(self, word, test_dict):
        """takes a code word and a dict of values, replaces all letters with values in the dict,
        compares against a dict of all valid words, returns True if the translated word is found valid."""
        test_word = []
        for letter in word:
            test_word.append(test_dict.get(letter))
        test_word= "".join(test_word)
        return is_word(self.valid_words_dict, test_word)
    
    def decrypt_final_message(self, dyct):
        """use a current dict of values to translate the entire message."""
        new_message_list = []
        for j in self.message_text:
            new_message_list.append(dyct.get(j))
        new_message = "".join(new_message_list)
        return new_message
    
    def get_list_of_final_message(self, decrypted_message):
        """take a STR of decrypted message, separate into list of words with no
        punctuation. returns list."""
        split_words = decrypted_message.split()
        list_of_words = []
        for i in split_words:
            no_punct = i.strip(" ,.")
            list_of_words.append(no_punct)
        return split_words

    def get_dict_score(self, dyct, number = -1):
        """takes a dict and an index number, scores it based on how many 
        encrypted words (starting at index 0 through index [number]) 
        can produce a possible match with a valid word.
        returns the score, and a list of words with only one possible match. """
        score = 0
        one_match_words = {}
        test_words = []
        words_added = 0
        for word in self.list_of_words_by_length[:number]:
            match_words = self.show_possible_matches(word, dyct)
            if len(match_words) > 0:
                score += 1
            if len(match_words) == 1:
                one_match_words[word] = match_words[0]
        return score, one_match_words
    
    def get_dict_score_end_compare(self, dyct, number = 0):
        """takes a dict and an index number (the starting index of the search, using a list
        of code words ordered from smallest to largest), scores the dict based on how many 
        encrypted words can produce a possible match with a valid word.
        returns the score, and a list of words with only one possible match. """
        score = 0
        one_match_words = {}
        test_words = []
        words_added = 0
        for word in self.list_of_words_by_length[number:]:
            match_words = self.show_possible_matches(word, dyct)
            if len(match_words) > 0:
                score += 1
            if len(match_words) == 1:
                one_match_words[word] = match_words[0]
        return score, one_match_words
    
    def find_next_word(self, number, guess_dict):
        """takes a number (INT), and a guess_dict and looks for a word in the message
        of that size that isn't 'solved' by the current dict yet. If
        all words of that size are solved, moves to the next largest word.
        Returns that word."""
        size = number
        send = False
        choices = []
        for word in self.list_of_words:
            if len(word) == size:
                for c in word:
                    if guess_dict.dyct[c] == '*':
                        return word
        if len(choices) > 0:
            high_score = 0
            best_choice = None
            for choice in choices:
                known_letters = 0
                for c in choice:
                    if guess_dict.dyct[c] != '*':
                        known_letters += 1
                if known_letters > high_score:
                    high_score = known_letters
                    best_choice = choice
            return best_choice
        return self.find_next_word(size+1, guess_dict)

    def remove_lower_scores(self, lyst):
        """takes list of dicts, returns a list of only the highest score
        dicts"""
        new_dict_list = []
        if len(lyst) > 0:
            current_high_score = lyst[0].score
            self.score = current_high_score
            for d in lyst:
                if d.score == current_high_score:
                    new_dict_list.append(d)
        return new_dict_list

    def decrypt_longest_words(self, lyst, end_index):
        """takes lyst of GuessDicts, uses them to decrypt a number of longer words (starting at end_index number),
        returns list of highest scoring dicts."""
        next_dict_list = []
        for dyct in lyst:
            dyct_score, dyct_one_words = test_message.get_dict_score_end_compare(dyct.dyct, end_index)
            guess_dict = GuessDict(dyct.dyct)
            guess_dict.score = dyct_score
            guess_dict.one_words = dyct_one_words
            if guess_dict.score > 0:
                next_dict_list.append(guess_dict)
        next_dict_list = sort_by_highest_score(next_dict_list)
        highest_dict_list = self.remove_lower_scores(next_dict_list)
        return highest_dict_list
    
    def build_dicts_from_one_words(self, lyst):
        for new_dict in lyst:
            keys = list(new_dict.one_words.keys())
            values = list(new_dict.one_words.values())
            key_index = 0
            for one_word in keys:
                value = values[key_index]
                c_index = 0
                for c in one_word:
                    new_dict.replace(c, value[c_index])
                    c_index += 1
                key_index += 1
        return lyst

    def find_next_best_dict(self, word, dyct):
        """takes an unsolved word, and the current best dict, builds new dicts with possible values for
        the word. Scores each dict based on the number of code words with possible matches. Sorts dicts by
        highest score. Takes highest scoring dicts, and adds any words with only one possible solution, 
        then scores them again, sorts them, removes all but highest scores, and returns remaining list of dicts."""
        dict_list = []
        dicts_for_longest_word = self.build_next_word_dicts(word, dyct)
        for dyct in dicts_for_longest_word:
            dyct_score, dyct_one_words = self.get_dict_score(dyct, 6)
            guess_dict = GuessDict(dyct)
            guess_dict.score = dyct_score
            guess_dict.one_words = dyct_one_words
            if guess_dict.score > 0:
                dict_list.append(guess_dict)
        dict_list = sort_by_highest_score(dict_list)
        
        for dyct in dict_list:
            print('score: ', dyct.score)
            print('one word matches: ', dyct.one_words)
            print('message so far: ', test_message.decrypt_final_message(dyct.dyct)) 
        
        new_dict_list = self.remove_lower_scores(dict_list)

        for new_dict in new_dict_list:
            keys = list(new_dict.one_words.keys())
            values = list(new_dict.one_words.values())
            key_index = 0
            for one_word in keys:
                value = values[key_index]
                c_index = 0
                for c in one_word:
                    new_dict.replace(c, value[c_index])
                    c_index += 1
                key_index += 1
            new_dict.score, new_dict.one_words = self.get_dict_score(new_dict.dyct)
        sorted_dict_list = sort_by_highest_score(new_dict_list)
        new_dict_list = self.remove_lower_scores(sorted_dict_list)
        return new_dict_list

if __name__ == '__main__':
    # main()
    ALL_POSSIBLE_WORDS = []
    TWO_LETTER_WORDS = []
    FIRST_LETTERS = []
    LAST_LETTERS = []
    FIRST_AND_LAST_LETTERS = []
    NOT_IN_TWO_LETTER_WORDS = []
    MOST_COMMON_TWO_LETTER_WORDS = []
    MOST_COMMON_THREE_LETTER_WORDS = []
    start = time.perf_counter()
    key = "abcdefghijklmnopqrstuvwxyz0123456789 !@#$%^&*()-_+={}[]|:;'<>?,./\""
    value = "**************************0123456789 !@#$%^&*()-_+={}[]|:;'<>?,./\""
    test_dict = dict(zip(key, value))

    dict_list = []
    print("Choose an option: ")
    print("   1. Decrypt a pre-written test message")
    print("   2. Type your own message to decrypt")
    answer_1 = str(input("Type 1 or 2: "))
    if answer_1 == '1':
        answer_2 = int(input("Choose a number 1-5: "))
        if answer_2 > 5:
            answer_2 = 5
        list_of_messages = ["aeuc dg bhlui gh ukgdcq, whn bkc ihlugdlui euvt whnziuvo lhzu fw euvtdcq whnziuvo vuii.", 
        "MVKCY MFV OCQRCUC RY CEJF VZFCN JNCEZC ENKRCP ZFEZ MRQQ MRY BRYHIVKP EYI MENP", 
        "Qb abg ghea gur fhcrevbe rlr bs pevgvpny cnffvivgl hcba gurfr rssbegf. Jr zhfg abg or nzovgvbhf. Jr pnaabg nfcver gb znfgrecvrprf. Jr znl pbagrag bhefryirf jvgu n wbl evqr va n cnvag obk.", 
        "Robo oxnc wi pybofob wowybklvo psbcd rsqr csobbk ohmebcsyx. S rkfo mbyccon dro bkxqo yp vsqrd, cebovi dro lbsqrdocd kxn locd yp kvv dro vybn rkc lesvd. Kxn, botysmsxq sx sdc qvybi, s qvknvi, qbkdopevvi, ryzopevvi zbki S wki coo sd kqksx.",
        "HU XSJREUHVHUE GKS KDNOUHGQ RZ RDX ZSBBRF ISHUEY, FS WOQ RDXYSBASY GKS KHEKSYG GXHIDGS."]
        encrypted_message = list_of_messages[answer_2 - 1]
    else:
        encrypted_message = str(input("Enter your encrypted message: "))

    test_message = CiphertextMessage(encrypted_message)


    next_word_index = -2
    try: 
        dicts_for_longest_word = test_message.build_next_word_dicts(test_message.longest_word, test_dict)
    except:
        test_message.list_of_words_by_length.pop(-1)
        dicts_for_longest_word = test_message.build_next_word_dicts(test_message.list_of_words_by_length[-1], test_dict)
    if len(dicts_for_longest_word) > 225:
        dicts_for_longest_word = test_message.build_next_word_dicts(test_message.list_of_words_by_length[next_word_index], test_dict)
        next_word_index = -1
    else:
        next_word_index = -3

    # instantiate GuessDict objects for each dict, score them, sort by highest score.
    for dyct in dicts_for_longest_word:
        dyct_score, dyct_one_words = test_message.get_dict_score(dyct, 6)
        guess_dict = GuessDict(dyct)
        guess_dict.score = dyct_score
        guess_dict.one_words = dyct_one_words
        if guess_dict.score > 0:
            dict_list.append(guess_dict)
    dict_list = sort_by_highest_score(dict_list)
    
    new_dict_list = test_message.remove_lower_scores(dict_list)
    for dyct in new_dict_list:
        print('score: ', dyct.score)
        print('one words: ', dyct.one_words)
    best_dict_list = test_message.build_dicts_from_one_words(new_dict_list)
    best_dict_list = test_message.decrypt_longest_words(best_dict_list, -3)
    best_dict_list = test_message.remove_lower_scores(best_dict_list)
    
    CURRENT_TEST_WORD = ''
    CURRENT_TEST_WORD_INDEX = len(test_message.list_of_words_by_length) + next_word_index
    loop_count = 0
    all_true = False
    while all_true == False:
        print('Times through loop = ', loop_count)
        loop_count += 1
        next_dict_list = []
        for dyct in best_dict_list:
            CURRENT_TEST_WORD = test_message.list_of_words_by_length[CURRENT_TEST_WORD_INDEX]
            print('Current Test Word: ', CURRENT_TEST_WORD)
            try:
                temp_list = test_message.find_next_best_dict(CURRENT_TEST_WORD, dyct.dyct)
                print('finished temp list')
            except:
                CURRENT_TEST_WORD = test_message.find_next_word(2, dyct)
                temp_list = test_message.find_next_best_dict(CURRENT_TEST_WORD, dyct.dyct)
            for j in temp_list:
                next_dict_list.append(j)
                final_message = test_message.decrypt_final_message(j.dyct)
                print('final message: ', final_message)
                final_message_list = test_message.get_list_of_final_message(final_message)
                all_true = True
                for word in final_message_list:
                    if len(word) <= 10:
                        if is_word(test_message.valid_words_dict, word) == False:
                            all_true = False
                            print(word, 'is not a valid word')
                if all_true:
                    print()
                    print('*** FINAL TRANSLATION: *** ')
                    print(test_message.message_text, ' == ')
                    print(final_message)
                    print()
                    break
        CURRENT_TEST_WORD_INDEX -= 1
        best_dict_list = next_dict_list.copy()
    
    elapsed = time.perf_counter() - start
    print('time elapsed: ', elapsed)

"""
aeuc dg bhlui gh ukgdcq, whn bkc ihlugdlui euvt whnziuvo lhzu fw euvtdcq whnziuvo vuii.

"""
