"""
Chaocipher Decrypter
author: Glenn Gorgoth
date: July 4, 2021

Takes a message and decrypts it using the Chaocipher algorithm. 

Has to option to decrypt a message using a known CypherAlphet.
In this case, it will be decrypted as a string with no spaces, 
then will compare the string with a list of English words to try and
determine where the spaces should go in the message. It has a harder time 
with proper names, slang, or longer words that can be split into several 
valid words.

Alternatively, can try to decrypt a message without knowing the CypherAlphabet.
In this case it will iterate through all possible alphabet cominations until
it finds one that creates a message with English words in it. This could potentially
take 10**12 years to finish, so be patient.

Returns the best guess of the decrypted message.

"""

import random
import add_spaces
import time
from itertools import permutations

def CreateAlphabetList (alphabet):
    """
    takes an alphabet(string) and returns the alphabet in list form.
    """
    lyst = []
    for letter in alphabet:
        lyst.append(letter)
    return lyst

def EncryptLetter(ptLetter, ptLyst, cyLyst):
    """
    Substitutes letter from ptLyst for corresponding letter in cyLyst
    """
    letterIndex = ptLyst.index(ptLetter)
    cyLetter = cyLyst[letterIndex]
    return cyLetter

def DecryptLetter(letter, ptLyst, cyLyst):
    """
    Substitutes letter from ptLyst for corresponding letter in cyLyst
    """
    letterIndex = cyLyst.index(letter)
    ptLetter = ptLyst[letterIndex]
    return ptLetter

def PermutePtLyst (ptLyst, ptIndex):
    """
    Permutes the Plaintext Alphabet (ptLyst) according to the last used letter (ptIndex)
    """
    ptIndex += 1
    newLystFront = ptLyst[ptIndex:]
    newLystBack = ptLyst[:ptIndex]
    newLyst = newLystFront + newLystBack
    letterShift = newLyst.pop(2)
    newLyst.insert(13, letterShift)
    # print("PT Lyst = ", "".join(newLyst))
    return newLyst

def PermuteCyLyst (cyLyst, cyIndex):
    """
    Permutes the Cypher Alphabet (cyLyst) according to the last used letter (cyIndex).
    """
    newLystFront = cyLyst[cyIndex:]
    newLystBack = cyLyst[:cyIndex]
    newLyst = newLystFront + newLystBack
    letterShift = newLyst.pop(1)
    newLyst.insert(13, letterShift)
    # print("CY Lyst = ", "".join(newLyst))
    return newLyst

def EncryptPT (ptLyst, cyLyst, ptWord):
    """
    Takes ptLyst, cyLyst (each a list of alphabets), and ptWord (a plaintext message).
    Encrypts each letter of the message, performs the next permutation, then
    returns encrypted message
    """
    count = 1
    cyWord = ""
    for letter in ptWord:
        if letter == " ":
            continue
        newLetter = EncryptLetter(letter, ptLyst, cyLyst)
        cyWord += newLetter
        count += 1
        if count > 5:
            cyWord += " "
            count = 1
        if letter != " ":
            letterIndex = ptLyst.index(letter)
            ptLyst = PermutePtLyst(ptLyst, letterIndex)
            cyLyst = PermuteCyLyst(cyLyst, letterIndex)
    return cyWord

def DecryptCY (ptLyst, cyLyst, cyWord):
    """
    Take ptLyst (list of PT alphabet), cyLyst (list of cypher alphabet),
    and cyWord (encrypted message). Substitutes each letter, then performes next
    permutation. Returns decrypted message.
    """
    count = 1
    ptWord = ""
    for letter in cyWord:
        if letter == " ":
            continue
        newLetter = DecryptLetter(letter, ptLyst, cyLyst)
        ptWord += newLetter
        count += 1
        if letter != " ":
            letterIndex = ptLyst.index(newLetter)
            ptLyst = PermutePtLyst(ptLyst, letterIndex)
            cyLyst = PermuteCyLyst(cyLyst, letterIndex)
    return ptWord

def randomAlphabet (alphabet):
    """
    Generates a random alphabet to use in encrypting the message.
    """
    newAlpha = ""
    maxNum = len(alphabet)
    alphaLyst = list(alphabet)
    for i in range(maxNum):
        nextLetter = alphaLyst.pop(random.randint(0, len(alphaLyst)-1))
        print(nextLetter)
        newAlpha += nextLetter
    return newAlpha

def crackTheCode(message, alphabet):
    # alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    ptAlpha = alphabet
    cyAlpha = alphabet
    lyst = []
    for p in permutations(ptAlpha):
        newPT = list(p)
        print("ptAlpha: ", newPT)
        for c in permutations(cyAlpha):
            newCY = list(c)
            # newCyAlpha = ''.join(c)
            print("new cyAlpha: ", "".join(newCY))
            decryptedNoSpaces = DecryptCY(newPT, newCY, message)
            print("noSpaces = ", decryptedNoSpaces)
            testSpaces = add_spaces.Message(decryptedNoSpaces)
            testMessage = testSpaces.divide_message(testSpaces.message_list)
            # print(testMessage)
            # print("Score: ", testSpaces.score)
            if testSpaces.score > 5:
                lyst.append((testMessage, testSpaces.score))
                return lyst
    return lyst
    pass

def decryptAndAddSpaces(ptalpha, cyalpha, message):
    """
    takes ptalpha (plain text alphabet), cyalpha (cypher alphabet), and encrypted message.
    Decripts message as one long string with no spaces, then attempts to split it into English words.
    """
    ptLyst, cyLyst = list(ptalpha), list(cyalpha)
    decryptedNoSpaces = DecryptCY(ptLyst, cyLyst, message)
    message = add_spaces.Message(decryptedNoSpaces)
    messageWithSpaces = message.divide_message(message.message_list)
    return messageWithSpaces

def generateCode(message, ptalpha, cyalphabet):
    """ takes message: string, and encrypts it using phtalpha: a plaintext alphabet 
    and cyalphabet: a cyphertext alphabet. Returns list of encrypted message and
    respective cypher alphabet.
    """
    cyphertextLyst = list(cyalphabet)
    plaintextLyst = list(ptalpha)
    cyMessage = EncryptPT(plaintextLyst, cyphertextLyst, message)
    print("cyMessage = ", cyMessage)
    print("cyphertextAlpha = ", cyalphabet)
    return [cyMessage, cyalphabet]



## Uncomment below to encrypt the test message with a specific alphabet

# ptMessage = "women who believe in each other create armies that will win kingdoms and wars"
# ptMessage = "if you can solve this message you are a champion among champions"
# ptMessage = ptMessage.upper()
# plaintextAlpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
# cyphertextAlpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
# generateCode(ptMessage, plaintextAlpha, cyphertextAlpha)


# # Uncomment below to decrypt a message using specified alphabets

start = time.time()
# Replace cyMessage with your own chaocipher encrypted message"
cyMessage =  "NXYAE NBPKC UEIKG ZYTTS LKEHE AYIKD XIKDI EMKQX VXIWS XFNLF CWYEV OT"
# Replace cyphertextAlpha with the chaocipher alphebet used to encrypt message
cyphertextAlpha =  "JZYQOEXBACPDSMLHRGWNUIKVTF"
plaintextAlpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
dcMessage = decryptAndAddSpaces(plaintextAlpha, cyphertextAlpha, cyMessage)
print("cyMessage = ", cyMessage)
print("PTAlphabet = ", plaintextAlpha)
print("CYAlphaget = ", cyphertextAlpha)
if dcMessage:
    print(dcMessage)
else:
    print("Unable to decipher message.")
end = time.time()
print("Time Elapsed: ", end-start)



# # Uncomment below to decrypt a message without knowing the alphabets used

# start = time.time()
# plaintextAlpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
# cyMessage =  "IEWLQ WJELD NLSHU EBJKZ OHICH SHFEX OZFWS JTFWE PIEWP XGTPQ QPT"
# bestGuesses = crackTheCode(cyMessage, plaintextAlpha)
# for guess in bestGuesses:
#     print("Message: ", guess[0], "Score: ", guess[1])
# end = time.time() 
# print("Time Elapsed: ", end-start)


# Below are time results for decrypting without knowing the CYalphabet. Since the "permutations" starts
# at the end of the alphabet, each digit from the left edge that is changed adds exponentially more
# time to the process

# try#1
# cyMessage =  "ZNKOY RNIRX DWUGR SPNUV MXGLV FODFJ OOSAE OGUJK RLPHI JJBUY ZCZZN YKWBU QDZP"
# cyphertextAlpha = "ABCDEFGHIJKLMNOPQRSTUVZYXW"
# time elapsed = 0.5711989402770996

# try#2
# cyMessage =  "YNKOX RNIRW DUVGR SPNVZ MWGLZ FODFJ OOSAE OGVJK RLPHI JJBVX YCYYN XKUBV QDYP"
# cyphertextAlpha = "ABCDEFGHIJKLMNOPQRSTVZYXWU"
# time elapsed = 4.619878053665161

# try#3
# cyMessage =  "TNKOX RNIRW DUZGR SPNZY MWGLY FODFJ OOSAE OGZJK RLPHI JJBZX TCTTN XKUBZ QDTP"
# cyphertextAlpha = "ABCDEFGHIJKLMNOPQRSVZYTXWU"
# time elapsed = 41.511240005493164

# try#4
# cyMessage =  "TNKOX RNIRW DUYGR VPNYS MWGLS FODFJ OOVAE OGYJK RLPHI JJBYX TCTTN XKUBY QDTP"
# cyphertextAlpha = "ABCDEFGHIJKLMNOPQRVZYSTXWU"
# time elapsed = 397.6084861755371

# try whole CY alphabet combination =
# estimated time elapsed 10**12 years

















