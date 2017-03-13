from path import path
from Parser import stemText
from Query import Query
import itertools

import InvertedIndex

fulldoc = path('C:\Users/admin/Documents/575/parser/Question_Answer_Dataset_v1.2/Question_Answer_Dataset_v1.2/S08/data/set1/a1.txt.clean').bytes()
docArray = [para for para in fulldoc.split('\n') if para.strip() != '']


tester = InvertedIndex.InvertedIndex()

for step in docArray:

    stemmed = stemText(step)

    tester.indexDocument(stemmed)

print('running query')
queryObj = Query(tester)
queryText = "kangaroo marsupial"
stemmedQuery = stemText(queryText)

docsWithTermProximity = queryObj.mergeEachPostingPair(stemmedQuery, 5)

print(docsWithTermProximity)

shortList = queryObj.consolidateDocProximityList(docsWithTermProximity, 5)
queryObj.showDocumentText(shortList,
                          docArray, 10)
