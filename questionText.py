from path import path
from Parser import stemText
from Query import Query

import InvertedIndex

fulldoc = path('C:\Users/admin/Documents/575/parser/Question_Answer_Dataset_v1.2/Question_Answer_Dataset_v1.2/S08/data/set1/a1.txt.clean').bytes()
docArray = [para for para in fulldoc.split('\n') if para.strip() != '']


print(len(docArray))
one = docArray[15]
print(one)
two = docArray[9]
print(two)
three = docArray[34]
four = docArray[29]
five = docArray[15]

steps = [one, two, three, four, five]

tester = InvertedIndex.InvertedIndex()

for step in docArray:

    stemmed = stemText(step)

    tester.indexDocument(stemmed)

print('running query')
queryObj = Query(tester)
queryText = "red kangaroo"
docQuery = queryObj.betterQueryIndex(stemText(queryText))


print ("now we are printing the generated query document")
print(docQuery)

print(queryObj.documentScores(docQuery))

for doc in docQuery:
    docId = doc[0]
    for position in doc[1]:

        print(docId)
        if position - 4 > 0:
            positionA = position - 4
        else:
            positionA = 0
        print(docArray[docId-1].split(' ')[positionA:position+4])