"""
message_encrypter.py
author: Glenn Gorgoth

description: encrypt or decrypt a message using a caesar shift cipher.
for example: Original message = "home sweet home"
Then shift all letters by a number 1-25, say 2.
Encrypted word = "jqog uyggv jqog"
"""

import string
import textwrap

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    # print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    # print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

def get_story_file(file_name):
    f = open(file_name, "r")
    story = str(f.read())
    f.close()
    return story


def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        # pass #delete this line and replace with your code here

        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)


    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        # pass #delete this line and replace with your code here
        
        return self.message_text

    def split_message_text(self):
        """
        Used to split a string of multiple words into a list

        """
        self.split_text = self.message_text.split()

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        # pass #delete this line and replace with your code here

        self.valid_words_copy = self.valid_words.copy()
        return self.valid_words_copy

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        # pass #delete this line and replace with your code here

        shift = int(shift)
        if shift >= 0 and shift <26:
            self.shift = shift
        else:
            print("Not a Valid Shift number")
            pass
        punctuation_list = list("0123456789 !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
        lowercase_list = list(string.ascii_lowercase)
        uppercase_list = list(string.ascii_uppercase)
        lowercase_nums = []
        uppercase_nums = []
        lowercase_code = []
        uppercase_code = []

        for i in lowercase_list:
            if (ord(i)+self.shift) <= 122:
                lowercase_nums.append(ord(i)+self.shift)
            else:
                lowercase_nums.append(ord(i)+(self.shift-26))
        for i in lowercase_nums:
            lowercase_code.append(chr(i))

        for i in uppercase_list:
            if (ord(i) + self.shift) <= 90:
                uppercase_nums.append(ord(i) + self.shift)
            else:
                uppercase_nums.append(ord(i) + (self.shift - 26))
        for i in uppercase_nums:
            uppercase_code.append(chr(i))

        letter_list = uppercase_list+lowercase_list
        code_leters = uppercase_code+lowercase_code
        self.shift_dict = dict(zip(letter_list, code_leters))
        for i in punctuation_list:
            self.shift_dict.update({i: i})
        return self.shift_dict


    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        # pass #delete this line and replace with your code here
        self.org_message = list(self.message_text)
        self.new_message = []
        for i in self.org_message:
            self.new_message.append(self.shift_dict.get(i))
        # print(self.new_message)
        self.new_string = "".join(self.new_message)
        return self.new_string



class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object        
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
        # pass #delete this line and replace with your code here
        Message.__init__(self, text)
        self.message_text = text
        self.valid_words = self.get_valid_words()
        self.shift = shift
        self.shift_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(self.shift)



    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        # pass #delete this line and replace with your code here

        return self.shift

    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class
        
        Returns: a COPY of self.encryption_dict
        '''
        # pass #delete this line and replace with your code here

        return self.encryption_dict.copy()

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        # pass #delete this line and replace with your code here

        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift.        
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        # pass #delete this line and replace with your code here
        self.shift = shift


class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        # pass #delete this line and replace with your code here
        Message.__init__(self, text)
        self.message_text = text
        self.valid_words = self.get_valid_words()

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create 
        the maximum number of valid words, you may choose any of those shifts 
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        # pass #delete this line and replace with your code here
        self.s = 0
        self.s_word_dict = {}
        high_value = 0
        best_s = None
        lowercase_list = list(string.ascii_lowercase)
        uppercase_list = list(string.ascii_uppercase)


        # iterate through all possible letter shifts
        for i in range(25):
            #restart a counter of how many real words the message contains,
            #a dictionary for each shift,
            #empty test translation
            self.word_count = 0
            self.test_dict = self.build_shift_dict(self.s)
            self.test_message = []

            # Shifts all letters according to the current dict
            for j in self.message_text:
                self.test_message.append(self.test_dict.get(j))
            self.test_words = "".join(self.test_message)

            # separates string into list of words
            self.split_text = self.test_words.split()

            # if self.test_word in self.valid_words:
            for k in self.split_text:
                if is_word(self.valid_words, k):
                    self.word_count += 1

            # Keep track of valid words counts and translations for each shift
            add_value = [self.word_count, self.test_words]
            self.s_word_dict.update({self.s: add_value})
            self.s += 1

        # Finds shift number with most valid word counts
        for i in self.s_word_dict:
            j = self.s_word_dict[i][0]
            if j > high_value:
                high_value = j
                best_s = i
        self.answer = (best_s, self.s_word_dict[best_s] [1])
        return self.answer

            # for j in self.message_text:
                # if j in lowercase_list:
                #     if ord(j)-self.s >= 97:
                #         self.test_message.append(chr(ord(j) - self.s))
                #     else:
                #         self.test_message.append(chr(ord(j) - (26-self.s)))
                # elif j in uppercase_list:
                #     if ord(j)-self.s >= 65:
                #         self.test_message.append(chr(ord(j) - self.s))
                #     else:
                #         self.test_message.append(chr(ord(j) - (26-self.s)))
                # if ord(j)
                # self.test_message.append(chr(ord(j)))


if __name__ == '__main__':

    print("--Menu--")
    print("   1. Encrypt a Message")
    print("   2. Decrypt a Message")
    e_or_d = int(input("Choose an option: "))
    message_file = ''


    if e_or_d != 1 and e_or_d != 2:
        print("Not a valid option. Sorry")
    else:
        print("Would you like to: ")
        print("   1. encrypt/decrypt a .txt file")
        print("   2. type a message")
        file_or_type = int(input("Choose an option: "))

        if file_or_type == 1:
            file_name = str(input("Enter name of file to encrypt/decrypt: "))
            message_file = get_story_file(file_name)
            print("Original Message: ")
            print(textwrap.fill(message_file, 50))
            print("----------------")



        elif file_or_type == 2:
            message_file = str(input("Enter your message: "))

        if e_or_d == 1:
            s = int(input("What shift level will you use (enter a number 1-26)? "))
            encrypted_message = PlaintextMessage(message_file, s)
            print("Encrypted message: ")
            # print(textwrap.fill((encrypted_message.get_message_text_encrypted()), 50))
            print(encrypted_message.get_message_text_encrypted())

        elif e_or_d == 2:
            ciphertext = CiphertextMessage(message_file)


            decrypted_cipher = ciphertext.decrypt_message()
            print("Shift Value: ", decrypted_cipher[0])
            print("Decrypted Message: ")
            print(textwrap.fill(decrypted_cipher[1], 50))

"""
Here ends my forever memorable first High Sierra excursion. 
I have crossed the Range of Light, surely the brightest and 
best of all the Lord has built. And, rejoicing in its glory, 
I gladly, gratefully, hopefully pray I may see it again.

Robo oxnc wi pybofob wowybklvo psbcd rsqr csobbk
ohmebcsyx. S rkfo mbyccon dro bkxqo yp vsqrd,
cebovi dro lbsqrdocd kxn locd yp kvv dro vybn rkc
lesvd. Kxn, botysmsxq sx sdc qvybi, s qvknvi,
qbkdopevvi, ryzopevvi zbki S wki coo sd kqksx.

It is arguable whether the human race have been gainers by the march of science beyond the steam engine. Electricity opens a field of infinite conveniences to ever greater numbers, but they may well have to pay dearly for them. But anyhow in my thought I stop short of the internal combustion engine which has made the world so much smaller. Still more must we fear the consequences of entrusting to a human race so little different from their predecessors of the so-called barbarous ages such awful agencies as the atomic bomb. Give me the horse.
Ny nx fwlzfgqj bmjymjw ymj mzrfs wfhj mfaj gjjs lfnsjwx gd ymj rfwhm tk xhnjshj gjdtsi ymj xyjfr jslnsj. Jqjhywnhnyd tujsx f knjqi tk nsknsnyj htsajsnjshjx yt jajw lwjfyjw szrgjwx, gzy ymjd rfd bjqq mfaj yt ufd ijfwqd ktw ymjr. Gzy fsdmtb ns rd ymtzlmy N xytu xmtwy tk ymj nsyjwsfq htrgzxynts jslnsj bmnhm mfx rfij ymj btwqi xt rzhm xrfqqjw. Xynqq rtwj rzxy bj kjfw ymj htsxjvzjshjx tk jsywzxynsl yt f mzrfs wfhj xt qnyyqj inkkjwjsy kwtr ymjnw uwjijhjxxtwx tk ymj xt hfqqji gfwgfwtzx fljx xzhm fbkzq fljshnjx fx ymj fytrnh gtrg. Lnaj rj ymj mtwxj.

Pa pz hynbhisl dolaoly aol obthu yhjl ohcl illu
nhpulyz if aol thyjo vm zjplujl ilfvuk aol zalht
lunpul. Lsljaypjpaf vwluz h mplsk vm pumpupal
jvucluplujlz av lcly nylhaly ubtilyz, iba aolf thf
dlss ohcl av whf klhysf mvy aolt. Iba hufovd pu tf
aovbnoa P zavw zovya vm aol pualyuhs jvtibzapvu
lunpul dopjo ohz thkl aol dvysk zv tbjo zthssly.
Zapss tvyl tbza dl mlhy aol jvuzlxblujlz vm
luaybzapun av h obthu yhjl zv spaasl kpmmlylua
myvt aolpy wylkljlzzvyz vm aol zv-jhsslk ihyihyvbz
hnlz zbjo hdmbs hnlujplz hz aol havtpj ivti. Npcl
tl aol ovyzl.

Do not turn the superior eye of critical passivity upon these efforts. We must not be ambitious. We cannot aspire to masterpieces. We may content ourselves with a joy ride in a paint-box.

Qb abg ghea gur fhcrevbe rlr bs pevgvpny cnffvivgl
hcba gurfr rssbegf. Jr zhfg abg or nzovgvbhf. Jr
pnaabg nfcver gb znfgrecvrprf. Jr znl pbagrag
bhefryirf jvgu n wbl evqr va n cnvag obk.

I firmly believe that any man's finest hour, the greatest fulfillment of all that he holds dear, is that moment when he has worked his heart out in a good cause and lies exhausted on the field of battle

i like to play soccer with my friends
s vsuo dy zvki cymmob gsdr wi pbsoxnc

ice car bee fun dog sad bus cat me you dug fox eel tea the man boy red fir ton ten
rln lja knn odw mxp bjm kdb ljc vn hxd mdp oxg nnu cnj cqn vjw kxh anm ora cxw cnw

ice car bee fun dog sad bus cat me you dug fox eel tea the man boy red fir ton ten six seven eight nine ten eleven twelve thirteen fourteen sixteen 
wqs qof pss tib rcu gor pig qoh as mci riu tcl ssz hso hvs aob pcm fsr twf hcb hsb gwl gsjsb swuvh bwbs hsb szsjsb hkszjs hvwfhssb tcifhssb gwlhssb 

iron jams jerk jive kegs kilo labs laid leaf lice load make dons dare duel eats turn trim team weed wife vote zoom
wfcb xoag xsfy xwjs ysug ywzc zopg zowr zsot zwqs zcor aoys rcbg rofs risz sohg hifb hfwa hsoa kssr kwts jchs ncca

my wife is so sweet and kind and pretty and the best mom of all the moms and i love her all day and all night long
se colk oy yu yckkz gtj qotj gtj vxkzze gtj znk hkyz sus ul grr znk susy gtj o rubk nkx grr jge gtj grr tomnz rutm

the puppies love to run and play with their mom. they jump on the couch and bring joy to the whole family.
dro zezzsoc vyfo dy bex kxn zvki gsdr drosb wyw. droi tewz yx dro myemr kxn lbsxq tyi dy dro gryvo pkwsvi.

If life were predictable it would cease to be life, and be without flavor.
Nk qnkj bjwj uwjinhyfgqj ny btzqi hjfxj yt gj qnkj, fsi gj bnymtzy kqfatw.

The heights by great men reached and kept were not attained by sudden flight, but they, while their companions slept, were toiling upward in the night.
Cqn qnrpqcb kh panjc vnw anjlqnm jwm tnyc fnan wxc jccjrwnm kh bdmmnw ourpqc, kdc cqnh, fqrun cqnra lxvyjwrxwb bunyc, fnan cxrurwp dyfjam rw cqn wrpqc.

Greatness lies, not in being strong, but in the right using of strength; and strength is not used rightly when it serves only to carry a man above his fellows for his own solitary glory. He is the greatest whose strength carries up the most hearts by the attraction of his own.
Ufsohbsgg zwsg, bch wb pswbu ghfcbu, pih wb hvs fwuvh igwbu ct ghfsbuhv; obr ghfsbuhv wg bch igsr fwuvhzm kvsb wh gsfjsg cbzm hc qoffm o aob opcjs vwg tszzckg tcf vwg ckb gczwhofm uzcfm. Vs wg hvs ufsohsgh kvcgs ghfsbuhv qoffwsg id hvs acgh vsofhg pm hvs ohhfoqhwcb ct vwg ckb.

The greater the obstacle, the more glory in overcoming it.
Hvs ufsohsf hvs cpghoqzs, hvs acfs uzcfm wb cjsfqcawbu wh.

The greatest weapon against stress is our ability to choose one thought over another.


"""

    

