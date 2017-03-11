from mergeScorePostingsList import mergeDocPostingList

class InvertedIndex(object):
    """A Single-pass im-memory index"""
    termDict = {}
    termPosting = {}
    numDocs = 0

    def __init__(self):
        self.termDict = {}
        self.termPosting = {}
        self.numDocs = 0

    def indexDocument(self, stemmedWordList):
        """Index terms in new document, add it to the existing in memory InvertedIndex"""
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







if __name__ == "__main__":
    #one = ['1', 'spray', '5quart', 'slow', 'cooker', 'with', 'cook', 'spray']

    tester = InvertedIndex()

    #tester.indexDocument(one)

    one = [1, 6, 12, 19, 20, 989]
    two = [7, 14, 15, 20, 987]
    print(one)
    print(two)
    tester.mergePostingPositions(one, two, 2)