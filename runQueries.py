from Query import Query
import InvertedIndex
from Parser import stemText
import pickle

invertedIndex = InvertedIndex.InvertedIndex()

invertedIndex.load("mediumCorpus.pkl")

fileName = "mediumCorpus.pkl"

# with open(fileName, 'rb') as inputFile:
#     tempIndex = pickle.load(inputFile)
#
# print(tempIndex.listOfFiles)
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