from path import path
from Parser import stemText
from Query import Query
import pandas as pd

import InvertedIndex
from cosineSim import cosineSim

fulldoc = path('C:\Users/admin/Documents/575/parser/Question_Answer_Dataset_v1.2/Question_Answer_Dataset_v1.2/S08/data/set1/a1.txt.clean').bytes()
docArray = [para for para in fulldoc.split('\n') if para.strip() != '']


print(len(docArray))

#print(docArray[4].split(' '))

print(stemText(docArray[4]))


tester = InvertedIndex.InvertedIndex()

for step in docArray:

    stemmed = stemText(step)

    tester.indexDocument(stemmed)

docTermMatrix = tester.createTermDocMatrix()

pd.set_option('display.max_columns', 150)
#print(termDocMatrix.head())

print('running query')
queryObj = Query(tester)
queryText = "james cook"

stemmedQuery = stemText(queryText)

nearestDocs = queryObj.getKNearestDocs(stemmedQuery,docTermMatrix,5)

print("the nearest docs are: ")
print(nearestDocs)
