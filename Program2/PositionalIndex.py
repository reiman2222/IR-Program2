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
    

def doPhraseQuery(posIndex, phraseQ):
    phraseL = phraseQ.split()
    
    
    
    
#################    MAIN    ####################

'''
posIndex is a hash table that maps terms to list of tuples where the left part
of each tuple holds a document ID and the right part holds a list of positions
where the term appears in the document contained in the left part.
'''
posIndex = {}

inputFiles = giveFilePath('input-files.txt')
#indexFile(posIndex, inputFiles[0], 0)
buildPosIndex(posIndex, inputFiles)

hold = posIndex['cow']
print(hold)

'''
flag = True
while(flag):
    print("What do you want to do?")
    print("(1) proximitiy query")
    print("(2) phrase query")
    print("(3) exit")
    
    uinput = input()
    
    if (uinput == '1'):
        print("You chose proximity query.")
        
    elif (uinput == '2'):
        print("You chose phrase query.")
        
    elif (uinput == '3'):
        flag = False
        
    else:
        print("You made a mistake.")

'''

'''
outfile = "bitch.txt"
bitchfile = open(outfile, 'w')
for x in dict_list:
  bitchfile.write(str(x))
bitchfile.close()
'''

