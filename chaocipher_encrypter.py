"""
Chaocipher Encrypter
author: Glenn Gorgoth
date: July 4, 2021

Takes a message and encrypts it using the Chaocipher algorithm. 
Returns the encrypted message, and the cypher Alphabet used to encrypt 
(and needed to decrypt).

"""

import random
import add_spaces

def CreateAlphabetList (alphabet):
    lyst = []
    for letter in alphabet:
        lyst.append(letter)
    return lyst

def EncryptLetter(ptLetter, ptLyst, cyLyst):
    letterIndex = ptLyst.index(ptLetter)
    cyLetter = cyLyst[letterIndex]
    return cyLetter

def DecryptLetter(letter, ptLyst, cyLyst):
    letterIndex = cyLyst.index(letter)
    ptLetter = ptLyst[letterIndex]
    return ptLetter

def PermutePtLyst (ptLyst, ptIndex):
    ptIndex += 1
    newLystFront = ptLyst[ptIndex:]
    newLystBack = ptLyst[:ptIndex]
    newLyst = newLystFront + newLystBack
    letterShift = newLyst.pop(2)
    newLyst.insert(13, letterShift)
    # print("PT Lyst = ", "".join(newLyst))
    return newLyst

def PermuteCyLyst (cyLyst, cyIndex):
    newLystFront = cyLyst[cyIndex:]
    newLystBack = cyLyst[:cyIndex]
    newLyst = newLystFront + newLystBack
    letterShift = newLyst.pop(1)
    newLyst.insert(13, letterShift)
    # print("CY Lyst = ", "".join(newLyst))
    return newLyst

def EncryptPT (ptLyst, cyLyst, ptWord):
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
    print("Decrypting")
    print("ptLyst = ", ptLyst)
    print("cyLyst = ", cyLyst)
    print("message = ", cyWord)
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
    newAlpha = ""
    maxNum = len(alphabet)
    alphaLyst = list(alphabet)
    for i in range(maxNum):
        nextLetter = alphaLyst.pop(random.randint(0, len(alphaLyst)-1))
        newAlpha += nextLetter
    return newAlpha


if __name__ == '__main__':
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    plaintextAlpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    plaintextLyst = CreateAlphabetList(plaintextAlpha)
    cyphertextAlpha = randomAlphabet(alphabet)
    cyphertextLyst = list(cyphertextAlpha)

    plaintext = input("Enter a message you would like to encrypt: ")
    if plaintext == '' or plaintext == None:
        ptMessage = "women who believe in each other create armies that will win kingdoms and wars"
    else:
        ptMessage = plaintext
    ptMessage = ptMessage.upper()
    cyMessage = EncryptPT(plaintextLyst, cyphertextLyst, ptMessage)
    print("Encrypted Message = ", cyMessage)
    print("cyphertextAlpha = ", cyphertextAlpha)
    
