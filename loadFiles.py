from path import path
import glob
import os
from Parser import stemText
from Query import Query

import InvertedIndex

fulldoc = path('C:\Users/admin/Documents/575/parser/Question_Answer_Dataset_v1.2/Question_Answer_Dataset_v1.2/S08/data/set1/a1.txt.clean').bytes()
#docArray = [para for para in fulldoc.split('\n') if para.strip() != '']


invertedIndex = InvertedIndex.InvertedIndex()

dataDir = "C:\Users/admin/Documents/575/parser/Question_Answer_Dataset_v1.2/Question_Answer_Dataset_v1.2/S08/data/"

os.chdir(dataDir)
for set in glob.glob("set*"):
    os.chdir(dataDir+set)
    print(set)
    for file in glob.glob("a1.*.clean"):
        fullFileName = dataDir+set+"/"+file
        print(fullFileName)
        stemmedFile = stemText(path(file).text(encoding="utf8"))
        print("File stemmed")
        invertedIndex.indexDocument(stemmedFile, fullFileName)
        print("File added to index")

easyQuestions = ['beetles antennae function',
                 'beetles considered pests',
                 'ducks forage underwater',
                 'adult ducks fast fliers',
                 'elephant kill rhinoceros',
                 'elephants good swimmers',
                 'wolf pup fur darker',
                 'gray wolf mammal',
                 'giant otter inhabit',
                 'otters live pacific coast'
                 ]

mediumQuestions = ['largest living species penguin',
                   'tallest prehistoric penguins',
                   'male polar bear weight',
                   'polar bear guard hair',
                   'suborder turtles extinct'
                   ]

oneQuestion = ['red kangaroo']

queryObj = Query(invertedIndex)

queryNum = 1
for query in oneQuestion:
    print('RUNNING QUERY NUMBER: ' + str(queryNum) + ',' + query)


    stemmedQuery = stemText(query)

    docsWithTermProximity = queryObj.mergeEachPostingPair(stemmedQuery, 5)

    #print(docsWithTermProximity)

    shortList = queryObj.consolidateDocProximityList(docsWithTermProximity, 5)
    queryObj.showDocumentText(shortList, 10)
    print('---\n')
    queryNum += 1