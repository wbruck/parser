import nltk
import string
import re

import addDocPostings


one = '1. Spray 5-quart slow cooker with cooking spray. In large bowl, mix melted butter, Worcestershire sauce, seasoned salt and garlic. Add chicken; toss to coat. Pour mixture into slow cooker.'
two = '2 In same bowl, mix tomatoes, soup and chiles; pour over chicken.'
three = '3 Cover; cook on High heat setting 2 to 3 hours or on Low heat setting 3 to 4 hours or until instant-read thermometer inserted in thickest part of chicken reads at least 165°F.'
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


