class invertedIndex(object):
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

        #sort term dict before merge

        #print(newTermDict)

        self.mergeTermDictionaries(newTermDict)

        print("master:")
        print(sorted(self.termDict.items()))

        #print(newDocPosting)
        self.addDocPosting(newDocPosting, self.numDocs+1)

        print("------------------------")
        print(sorted(self.termPosting.items()))

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

    def queryIndex(self,query):
        """query Index based on list of stemmed words"""
        queryDocs = {}
        for word in query:
            print(word, self.termPosting[word])
            for docPos in self.termPosting[word]:
                print(docPos[0], docPos[1])
                positions = docPos[1]
                try:
                    [queryDocs[docPos[0]].append(position) for position in positions]
                except:
                    queryDocs[docPos[0]] = positions
        print(queryDocs)

if __name__ == "__main__":
    one = ['1', 'spray', '5quart', 'slow', 'cooker', 'with', 'cook', 'spray']

    tester = invertedIndex()

    tester.indexDocument(one)