import nltk
import string
import re
from path import path

import addDocPostings

def readFile(fileName):
    with open(fileName) as f:
        s = f.read()
    print s
    return s

one = path('C:\Users/admin/Documents/575/parser/Question_Answer_Dataset_v1.2/Question_Answer_Dataset_v1.2/S08/data/set1/a1.txt.clean').bytes()
print(one[:1000])
#one = '1. Spray 5-quart slow cooker with cooking spray. In large bowl, mix melted butter, Worcestershire sauce, seasoned salt and garlic. Add chicken; toss to coat. Pour mixture into slow cooker.'
two = '2 In same bowl, mix tomatoes, soup and chiles; pour over chicken.'
three = '3 Cover; cook on High heat setting 2 to 3 hours or on Low heat setting 3 to 4 hours or until instant-read thermometer inserted in thickest part of chicken reads at least 165F.'
four = '4 Remove chicken from slow cooker, and transfer to cutting board; let stand 5 minutes or until cool enough to handle. Meanwhile, stir cream cheese and Cheddar cheese into slow cooker. Cover; cook on High heat setting 5 to 10 minutes or until cheese melts. Stir.'
five = '5 Meanwhile, shred chicken with 2 forks; return to slow cooker, and stir in cooked spaghetti. Top with parsley.'

steps = [one, two, three, four, five]

regex = re.compile('[%s]' % re.escape(string.punctuation))
stemmer = nltk.stem.PorterStemmer()
tester = addDocPostings.invertedIndex()

for step in steps:

    step = regex.sub('', step)

    stemmed = [stemmer.stem(word).lower() for word in step.split(' ')]

    tester.indexDocument(stemmed)

print('running query')
docQuery = tester.betterQueryIndex(['european', 'settlement'])

print ("now we are printing the generated query document")
print(docQuery )

#tester.retrieveBestDocs(docQuery, 8)

#tester.getTextPositionOfDoc(1, docQuery, 8)