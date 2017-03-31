from path import path
import glob
import os

from Parser import stemText
import InvertedIndex

def loadFiles(fileName):
    invertedIndex = InvertedIndex.InvertedIndex()

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
                stemmedFile = stemText(path(file).text(encoding="utf8"))
                print("File stemmed")
                invertedIndex.indexDocument(stemmedFile, fullFileName)
                print("File added to index")

    os.chdir(currentDir)

    invertedIndex.save(fileName)


if __name__ == "__main__":
    loadFiles("largeCorpus.pkl")