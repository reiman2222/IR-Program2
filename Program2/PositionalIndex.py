import re

#tokenizes a word
def tokenize(word):
    regex = re.compile('[^a-zA-Z]+')
    w = regex.sub('', word)
    w = w.lower()
    return w

#tokenizes a list of words
def tokenizeWordList(line):
    wordlist = line.split()
    i = 0
    while i < len(wordlist):
        wordlist[i] = tokenize(wordlist[i])
        i = i + 1
   
    return wordlist

def indexFile(posIndex, filename):
    with open(filename, 'r') as f:
        #go through file line by line
        currPos = 0
        for line in f:
            tokenized = tokenizeWordList(line)
            
            #print(tokenized)
            
            for word in tokenized:
                if word in posIndex:
                    addToPosIndex(posIndex, word, currPos, filename)
                else:
                    posIndex[word] = [(filename,[currPos])]
            currPos += 1


def addToPosIndex(posIndex, word, currPos, filename):
    L = posIndex[word]
    for tup in L:
        if L[0] is filename:
            L[1].append(currPos)
            return
    #if not return this file has not been    
    #encountered yet
    posIndex[word].insert(0, (filename, [currPos]))



#give_file_path(filename) returns the list of paths
#stored in the file called filename
def giveFilePath(filename):
    f = open(filename, 'r')
    words = [token for line in f for token in line.split()]
    return words

#def buildPosIndex(invertedIndex, inputFiles):
    





#################    MAIN    ####################

'''
posIndex is a hash table that maps terms to list of tuples where the left part
of each tuple holds a document name and the right part holds a list of positions
where the term appears in the document contained in the left part.
'''
posIndex = {}

inputFiles = giveFilePath('input-files.txt')

#BuildPosIndex(posIndex, inputFiles)

indexFile(posIndex, inputFiles[0])
  
#userInput = get user input 
'''
while(userInput.isExit())
    if(userInput.isPhraseQuery())
      #phraseQuery = get phrase query from user
      documents = doPhraseQuery(posIndex, phraseQuery)
      if(documents != null):
          print(documents)
      else:
          print("no match found")

    else: #input is a positional query
        #posQuery = get post query from user
        documents = doPosQuery(posIndex, posQuery)
        if(Documents != null):
          Print(documents)
        else:
          Print("no match found")    
     
'''
