import re
import porter

#tokenizes a word
def tokenize(word):
    regex = re.compile('[^a-zA-Z]+')
    w = regex.sub('', word)
    w = w.lower()
    w = porter.stem(w)
    return w

#tokenizes a list of words
def tokenizeWordList(line):
    wordlist = line.split()
    i = 0
    while i < len(wordlist):
        wordlist[i] = tokenize(wordlist[i])
        i = i + 1
   
    return wordlist

def indexFile(posIndex, filename, fileNumber):
    with open(filename, 'r') as f:
        #go through file line by line
        currPos = 0
        for line in f:
            tokenized = tokenizeWordList(line)
            
            #print(tokenized)
            
            for word in tokenized:
                if word in posIndex:
                    addToPosIndex(posIndex, word, currPos, fileNumber)
                else:
                    posIndex[word] = [(fileNumber,[currPos])]
                    
                currPos += 1


def addToPosIndex(posIndex, word, currPos, fileNumber):
    L = posIndex[word]
    for tup in L:
        if tup[0] is fileNumber:
            tup[1].append(currPos)
            return
    #if not return early then this file has not been    
    #encountered yet
    posIndex[word].append((fileNumber, [currPos]))

#give_file_path(filename) returns the list of paths
#stored in the file called filename
def giveFilePath(filename):
    f = open(filename, 'r')
    words = [token for line in f for token in line.split()]
    return words


def buildPosIndex(posIndex, inputFiles):
    fileNumber = 0
    
    
    while(fileNumber < len(inputFiles)):
        print("processing %s" %inputFiles[fileNumber])
        indexFile(posIndex, inputFiles[fileNumber], fileNumber)
        fileNumber += 1
    
#doPhraseQuery(posIndex, phraseQ) returns a list of documents where the phrase
#query phraseQ is satisfied. phraseQ is a space deliniated string of two terms.
def doPhraseQuery(posIndex, phraseQ):
    phraseL = tokenizeWordList(phraseQ)
	
    currPos = [0] * len(phraseL)
    docIDs = []
    posL = []
    
    i = 0
    for term in phraseL:
        if term in posIndex:
            posL.append(posIndex[term])
        else:
            return [] #all terms are not present in corpus
        i += 1
    #print(posIndex['other'])
    #print(posL[0])
    #print(posIndex['things'])
    #print(posL[1])
    while((currPos[0] < len(posL[0])) & (currPos[1] < len(posL[1]))):
        #print(posL[0][0][0])
        #print(posL[1][0][0])
        if (posL[0][0][0] == posL[1][0][0]):
            phraseQueryFile(posL, currPos, docIDs)
            currPos[0] += 1
            currPos[1] += 1
        else:
            if posL[0][0] < posL[1][0]:
                currPos[0] += 1
            else:
                currPos[1] += 1
    return docIDs

def phraseQueryFile(tuples, currPos, docIDs):
    Ltuple = tuples[0][currPos[0]]
    Rtuple = tuples[1][currPos[1]]

    LPos = 0
    RPos = 0
    while (LPos < len(Ltuple[1]) and
            RPos < len(Rtuple[1])):
        if ((Ltuple[1][LPos] + 1 == Rtuple[1][RPos])):
            docIDs.append(Ltuple[0])
            return
        elif (Ltuple[1][LPos] < Rtuple[1][RPos]):
            LPos += 1
        else:
            RPos += 1


#doProxQuery(posIndex, posQ, dist) returns a list of documents where the proximity 
#query proxQ is satisfied. proxQ is a space deliniated string of two terms
#dist is the maximum distance that the two terms can be seperated
def doProxQuery(posIndex, proxQ, dist):
    termL = tokenizeWordList(proxQ)
	
    currPos = [0] * len(termL)
    docIDs = []
    posL = []
    
    i = 0
    for term in termL:
        if term in posIndex:
            posL.append(posIndex[term])
        else:
            return [] #all terms are not present in corpus
        i += 1

    while((currPos[0] < len(posL[0])) & (currPos[1] < len(posL[1]))):
        if (posL[0][0][0] == posL[1][0][0]):
            posQueryFile(posL, currPos, docIDs, dist)
            currPos[0] += 1
            currPos[1] += 1
        else:
            if posL[0][0] < posL[1][0]:
                currPos[0] += 1
            else:
                currPos[1] += 1
    return docIDs


def posQueryFile(tuples, currPos, docIDs, dist):
    Ltuple = tuples[0][currPos[0]]
    Rtuple = tuples[1][currPos[1]]

    LPos = 0
    RPos = 0
    while (LPos < len(Ltuple[1]) and
            RPos < len(Rtuple[1])):
        if (abs(Ltuple[1][LPos] - Rtuple[1][RPos]) - 1 <= dist):
            docIDs.append(Ltuple[0])
            return
        elif (Ltuple[1][LPos] < Rtuple[1][RPos]):
            LPos += 1
        else:
            RPos += 1    

def getPhrase():
    print('enter a phrase for the query')
    return input()

#################    MAIN    ####################

'''
posIndex is a hash table that maps terms to list of tuples where the left part
of each tuple holds a document ID and the right part holds a list of positions
where the term appears in the document contained in the left part.
'''
posIndex = {}

inputFiles = giveFilePath('input-files.txt')
buildPosIndex(posIndex, inputFiles)


docs = doProxQuery(posIndex, 'God good', 7)
print(docs)
  
#userInput = get user input 


flag = True
while(flag):
    print("What do you want to do?")
    print("(1) proximitiy query")
    print("(2) phrase query")
    print("(3) exit")
    
    uinput = int(input())
    
    if (uinput == 1):
        print("You chose proximity query.")
        uphrase = getPhrase()
        
        print("What is the distance that you want for the Proximity Query?")
        dist = int(input())
        
        doProxQuery(posIndex, uphrase, dist)
        
        
    elif (uinput == 2):
        print("You chose phrase query.")
        uphrase = getPhrase()
        doPhraseQuery(posIndex, uphrase)
        
    elif (uinput == 3):
        flag = False
        
    else:
        print("You made a mistake.")

