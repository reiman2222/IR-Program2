import re
import porter

#tokenizes a word
def tokenize(word):
    regex = re.compile('[^a-zA-Z]+')
    w = regex.sub('', word)
    w = w.lower()
    w = porter.stem(w)
    return w

#toeknizeWordList(line) tokenizes a string of words. 
#line is the string to tokenize.
#returns list of tokenized words.
def tokenizeWordList(line):
    wordlist = []
    
    for token in line.split():
        wordlist.extend(token.replace('--', '-').split('-'))
    
    i = 0
    while(i < len(wordlist)):
        
        wordlist[i] = tokenize(wordlist[i])
        i = i + 1
    
    return wordlist


def giveWordList(filename):
    f = open(filename, 'r')
    words = []
    for line in f:
        for token in line.split():
            words.extend(token.replace('--', '-').split('-'))
    return words

def indexFile(posIndex, filename, fileNumber):
    with open(filename, mode='r') as f:
        #go through file line by line
        currPos = 0
        for line in f:
            tokenized = tokenizeWordList(line)
            
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
#query phraseQ is satisfied. phraseQ is a space delineated string of two terms.
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
        
    while((currPos[0] < len(posL[0])) & (currPos[1] < len(posL[1]))):
        if (posL[0][currPos[0]][0] == posL[1][currPos[1]][0]):
            phraseQueryFile(posL, currPos, docIDs)
            currPos[0] += 1
            currPos[1] += 1
        else:
            if posL[0][currPos[0]] < posL[1][currPos[1]]:
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
            if (len(docIDs) > 0):
                if (docIDs[len(docIDs) - 1][0] == Ltuple[0]):
                    docIDs[len(docIDs) - 1][1].append(Ltuple[1][LPos])
                else:
                    docIDs.append( (Ltuple[0], [Ltuple[1][LPos]]) )
            else:
                docIDs.append( (Ltuple[0], [Ltuple[1][LPos]]) )
            LPos += 1
            RPos += 1
        elif (Ltuple[1][LPos] < Rtuple[1][RPos]):
            LPos += 1
        else:
            RPos += 1


#doProxQuery(posIndex, posQ, dist) returns a list of documents where the proximity 
#query proxQ is satisfied. proxQ is a space deliniated string of two terms
#dist is the maximum distance that the two terms can be seperated
def doProxQuery(posIndex, proxQ, dist):
    termL = tokenizeWordList(proxQ)
    
    currPos = [0] * len(termL) #index of current document
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
        if (posL[0][currPos[0]][0] == posL[1][currPos[1]][0]):
            proxQueryFile(posL, currPos, docIDs, dist)
            currPos[0] += 1
            currPos[1] += 1
        else:
            if((posL[0][currPos[0]] < posL[1][currPos[1]])):
                currPos[0] += 1
            else:
                currPos[1] += 1
    return docIDs


def proxQueryFile(tuples, currPos, docIDs, dist):
    Ltuple = tuples[0][currPos[0]]
    Rtuple = tuples[1][currPos[1]]

    LPos = 0
    RPos = 0
    while (LPos < len(Ltuple[1]) and
            RPos < len(Rtuple[1])):
        if (abs(Ltuple[1][LPos] - Rtuple[1][RPos]) - 1 <= dist):
            if (len(docIDs) > 0):
                if (docIDs[len(docIDs) - 1][0] == Ltuple[0]):
                    docIDs[len(docIDs) - 1][1].append((Ltuple[1][LPos],Rtuple[1][RPos]))
                else:
                    docIDs.append( (Ltuple[0], [(Ltuple[1][LPos],Rtuple[1][RPos])]))
            else:
                docIDs.append( (Ltuple[0], [(Ltuple[1][LPos],Rtuple[1][RPos])]))
            LPos += 1
            RPos += 1
        elif (Ltuple[1][LPos] < Rtuple[1][RPos]):
            LPos += 1
        else:
            RPos += 1    

def getPhrase():
    print('Enter a query')
    return input()



def printQueryResultsPhr(docs, queryS, inputFiles):
    preview = 10
    
    print('"' + queryS +  '" found in ' + str(len(docs)) + ' documents')
    print(" ")
    
    for tup in docs:
        filename = inputFiles[tup[0]]
        docRaw = giveWordList(filename)
        
        print("There are " + str(len(tup[1])) + " matches in:")
        print(filename)
        print(' ')

        for pos in tup[1]:
            if(pos - preview < 0):
                start = 0
                preview = preview + preview/2
            else:
                start = pos - preview
            
            if(pos + preview < len(tup[1])):
                end = len(tup[1]) - 1
            else:
                end = pos + preview
            
            docL = docRaw[start:end]
            docS = " ".join(docL)
            print(docS)
            print(" ")


def printQueryResultsPrx(docs, queryS, inputFiles, dist):
    preview = 7
    
    print('"' + queryS +  '" within ' + str(dist)+ ' words, found in ' + str(len(docs)) + ' documents')
    print(" ")
    
    for tup in docs:
        filename = inputFiles[tup[0]]
        docRaw = giveWordList(filename)
        
        print("There are " + str(len(tup[1])) + " matches in:")
        print(filename)
        print(' ')

        for posTup in tup[1]:
            
            if(posTup[0] < posTup[1]):
                begin = posTup[0]
                stop = posTup[1]
            else:
                begin = posTup[1]
                stop = posTup[0]
                            
            if(begin - preview < 0):
                start = 0
                preview = preview + preview/2
            else:
                start = begin - preview
            
            if(stop + preview < len(tup[1])):
                end = len(tup[1]) - 1
            else:
                end = stop + preview
                
            
            
            docL = docRaw[start:end]
            docS = " ".join(docL)
            print(docS)
            print(" ")

        

#################    MAIN    ####################

'''
posIndex is a hash table that maps terms to list of tuples where the left part
of each tuple holds a document ID and the right part holds a list of positions
where the term appears in the document contained in the left part.
'''
posIndex = {}

inputFiles = giveFilePath('input-files.txt')

buildPosIndex(posIndex, inputFiles)

docs = []

flag = True
while(flag):
    print("What do you want to do?")
    print("(1) proximity query")
    print("(2) phrase query")
    print("(3) exit")
    
    uinput = int(input())
    
    if (uinput == 1):
        print("You chose proximity query.")
        uphrase = getPhrase()
        
        print("What is the distance that you want for the Proximity Query?")
        dist = int(input())
        
        docs = doProxQuery(posIndex, uphrase, dist)
        printQueryResultsPrx(docs, uphrase, inputFiles, dist)
        
        
    elif (uinput == 2):
        print("You chose phrase query.")
        uphrase = getPhrase()
        docs = doPhraseQuery(posIndex, uphrase)
        printQueryResultsPhr(docs, uphrase, inputFiles)
        
    elif (uinput == 3):
        flag = False
        
    else:
        print("You made a mistake.")

