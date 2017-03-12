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
queryText = "European explorers"
# docQuery = queryObj.betterQueryIndex(stemText(queryText))
stemmedQuery = stemText(queryText)

nearestDocs = queryObj.getKNearestDocs(stemmedQuery,docTermMatrix,5)

print("the nearest docs are: ")
print(nearestDocs)

# print("------------------")
# queryDict = {}
# for term in stemText(queryText):
#     queryDict[str(term)] = 1
# print(queryDict)

#queryDF = pd.DataFrame([queryDict])

# newMatrix = docTermMatrix.append(queryDict, ignore_index=True).fillna(0)
#
#
# qVec = newMatrix.iloc[-1]
# docVec = newMatrix.iloc[1]
# print(cosineSim(qVec, docVec))
#
# print(newMatrix.shape)
#
# i = 1
# documentSimilarities = {}
# while i < newMatrix.shape[0]-1:
#
#     documentSimilarities[i] = cosineSim(qVec, newMatrix.iloc[i])
#     i += 1
#
# print(documentSimilarities)
# print(sorted(documentSimilarities.items(), key=lambda x: x[1], reverse=True))
#for num in termDocMatrix.ix[2]:
    #print(num)
#print(termDocMatrix[1])
# print ("now we are printing the generated query document")
# print(docQuery)
#
# print(queryObj.documentScores(docQuery))
#
# for doc in docQuery:
#     docId = doc[0]
#     for position in doc[1]:
#
#         print(docId)
#         if position - 4 > 0:
#             positionA = position - 4
#         else:
#             positionA = 0
#         print(docArray[docId-1].split(' ')[positionA:position+4])