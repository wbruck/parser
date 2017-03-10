import nltk
import string
import re
from path import path
from Parser import stemText

import addDocPostings

def readFile(fileName):
    with open(fileName) as f:
        s = f.read()
    print s
    return s

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

tester = addDocPostings.invertedIndex()

for step in steps:

    stemmed = stemText(step)

    tester.indexDocument(stemmed)

print('running query')
query = "red kangaroo largest"
docQuery = tester.betterQueryIndex(stemText(query))


print ("now we are printing the generated query document")
print(docQuery)


#tester.retrieveBestDocs(docQuery, 8)

#tester.getTextPositionOfDoc(1, docQuery, 8)