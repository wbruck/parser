import pandas as pd
import os
import glob
import pickle
from path import Path

from Parser import stemText

class InvertedIndex(object):
    """A Single-pass im-memory index"""
    termDict = {}
    termPosting = {}
    listOfFiles = []
    numDocs = 0

    def __init__(self):
        self.termDict = {}
        self.termPosting = {}
        self.numDocs = 0
        self.listOfFiles = []

    def save(self,fileName):
        """Pickle the InvertedIndex object to load later"""

        with open(fileName, 'wb') as outputFile:
            pickle.dump(self, outputFile, pickle.HIGHEST_PROTOCOL)

    def load(self, fileName):
        """Load a pickled Inverted Index Object for queries or to add more documents"""

        with open(fileName, 'rb') as inputFile:
            tempIndex = pickle.load(inputFile)

        self.termDict = tempIndex.termDict
        self.termPosting = tempIndex.termPosting
        self.listOfFiles = tempIndex.listOfFiles
        self.numDocs = tempIndex.numDocs

    def indexDocument(self, stemmedWordList, fileName):
        """Index terms in new document, add it to the existing in memory InvertedIndex"""
        self.listOfFiles.append(fileName)

        newTermDict = {}
        newDocPosting = {}

        for index, term in enumerate(stemmedWordList):
            try:
                newTermDict[term] += 1
                newDocPosting[term].append(index)
            except:
                newTermDict[term] = 1
                newDocPosting[term] = [index]


#        #sort term dict before merge
#        #does sorting the dict really make a difference???
#        #print(newTermDict)

        self.mergeTermDictionaries(newTermDict)

        #print("master:")
        #print(sorted(self.termDict.items()))

        #print(newDocPosting)
#       Postings lists are already sorted becuase they are created sequentially
        self.addDocPosting(newDocPosting, self.numDocs+1)

        #print("------------------------")
        #print(sorted(self.termPosting.items()))

        self.numDocs += 1

    def mergeTermDictionaries(self, termDictionaryToMerge):
        """Merge the new term dictinary for document into existing master term dictionary"""

        for k in termDictionaryToMerge:
            try:
                self.termDict[k] += termDictionaryToMerge[k]
            except:
                self.termDict[k] = termDictionaryToMerge[k]

            #sort term Dict here

    def addDocPosting(self, docPosting, docNum):
        """Append (docNum, termPos) to the termPostings dict"""
        for k in docPosting:
            postTuple = (docNum, docPosting[k])
            try:
                self.termPosting[k].append(postTuple)
            except:
                self.termPosting[k] = [postTuple]


    def createTermDocMatrix(self):
        """create a term document matrix from the inverted index"""
        docsList = []

        i = 0
        while i <= self.numDocs:
            docsList.append({})
            i += 1

        for term, postingList in self.termPosting.items():
            #print(term)
            for posting in postingList:
                #print(posting)
                # EXAMPLE posting: (16, [53])
                docsList[posting[0]][term] = len(posting[1])

        matrix = pd.DataFrame(docsList)
        matrix = matrix.fillna(0)

        return matrix

    def loadIncludedCorpusFiles(self, fileName):
        """Load the included corpus files into the current Inverted Index"""

        currentDir = os.getcwd()

        workingDir = os.getcwd()

        questionsDir = workingDir + "/Question_Answer_Dataset_v1.2/Question_Answer_Dataset_v1.2/"

        os.chdir(questionsDir)
        for sDir in glob.glob("S*"):
            dataDir = questionsDir+sDir+"/data/"
            os.chdir(dataDir)
            print(sDir)
            for set in glob.glob("set*"):
                os.chdir(dataDir+set)
                print(set)
                for file in glob.glob("*.clean"):
                    fullFileName = dataDir+set+"/"+file
                    print(fullFileName)
                    stemmedFile = stemText(Path(file).text(encoding="utf8"))
                    print("File stemmed")
                    self.indexDocument(stemmedFile, fullFileName)
                    print("File added to index")

        os.chdir(currentDir)

        self.save(fileName)




if __name__ == "__main__":
    print("main")
