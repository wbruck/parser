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

    def queryIndex(self, query):
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
        return queryDocs

    def retrieveBestDocs(self, queryDocs, wordProximity):
        """ranke the top X docs from query return based on wordProximity (number of words in spaces for wordProx)"""
        docProximityScores = {}
        for docKey, wordOccurrences in queryDocs.items():
            lastWordPos = 0
            docScore = 0

            for i, position in enumerate(sorted(wordOccurrences)):
                # improve this later with map
                if i == 0:
                    lastWordPos = position
                    continue

                if position - lastWordPos <= wordProximity:
                    docScore += wordProximity - (position - lastWordPos)

                lastWordPos = position

            docProximityScores[docKey] = docScore

        print (docProximityScores)
        return docProximityScores

    def checkPostingPositions(self, docId1, docId2, wordProximity):

        one = [1, 4, 6, 9, 19, 20]
        two = [3, 7, 10, 16]
        if len(docId1) < len(docId2):
            tempList = docId1
            docId1 = docId2
            docId2 = tempList

        i = 0

        list = []
        for post1 in docId1:
            for post2 in docId2[i:]:
                if post1 > post2:
                    list.append(post2)
                    i += 1

                elif post1 < post2:
                    list.append(post1)

                    break

        list += docId2[i:]

        print(list)

    def getTextPositionOfDoc(self, docId, queryDocs, termDistance):
        """get the main text segmets of the document that may contain the answer"""
        positionsList = []
        for i, position in enumerate(queryDocs[docId]):
            if i == 0:
                lastPosition = position
                continue

            if lastPosition - position < termDistance:
                positionsList.append(position)

            lastPosition = position

        print(positionsList)



if __name__ == "__main__":
    #one = ['1', 'spray', '5quart', 'slow', 'cooker', 'with', 'cook', 'spray']

    tester = invertedIndex()

    #tester.indexDocument(one)

    one = [1, 4, 6, 9, 19, 20]
    two = [3, 7, 10, 15]
    tester.checkPostingPositions(one, two, 3)