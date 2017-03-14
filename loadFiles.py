from path import path
import glob
import os

from Parser import stemText
from Query import Query
import InvertedIndex

fulldoc = path('C:\Users/admin/Documents/575/parser/Question_Answer_Dataset_v1.2/Question_Answer_Dataset_v1.2/S08/data/set1/a1.txt.clean').bytes()
#docArray = [para for para in fulldoc.split('\n') if para.strip() != '']


invertedIndex = InvertedIndex.InvertedIndex()

currentDir = os.getcwd()

dataDir = "C:\Users/admin/Documents/575/parser/Question_Answer_Dataset_v1.2/Question_Answer_Dataset_v1.2/S08/data/"

os.chdir(dataDir)
for set in glob.glob("set*"):
    os.chdir(dataDir+set)
    print(set)
    for file in glob.glob("*.clean"):
        fullFileName = dataDir+set+"/"+file
        print(fullFileName)
        stemmedFile = stemText(path(file).text(encoding="utf8"))
        print("File stemmed")
        invertedIndex.indexDocument(stemmedFile, fullFileName)
        print("File added to index")

os.chdir(currentDir)

invertedIndex.save("mediumCorpus.pkl")
