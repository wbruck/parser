import nltk
import string
import re

import addDocPostings


def stemText(textToStem):
    """Return Stemmed text as list of words passed to function"""
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    stemmer = nltk.stem.PorterStemmer()


    cleanText = regex.sub('', textToStem)

    stemmed = [stemmer.stem(word).lower() for word in cleanText.split(' ')]

    return stemmed
