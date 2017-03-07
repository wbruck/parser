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


#        #sort term dict before merge
#        #does sorting the dict really make a difference???
#        #print(newTermDict)

        self.mergeTermDictionaries(newTermDict)

        print("master:")
        print(sorted(self.termDict.items()))

        #print(newDocPosting)
#       Postings lists are already sorted becuase they are created sequentially
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

    def betterQueryIndex(self, query):
        """query Index based on list of stemmed words"""

        i = 0

        while i+1 < len(query):
            postingList1 = self.termPosting[query[i]]
            postingList2 = self.termPosting[query[i+1]]
            print(query[i], postingList1)
            print(query[i+1], postingList2)

            x = 0
            y = 0
            while x + y < len(postingList1) + len(postingList2):
                if postingList1[x][0] == postingList2[y][0]:
                    nearByQueryTerms = self.mergePostingPositions(postingList1[x][1],
                                                                  postingList2[y][1],
                                                                  4)
                    x += 1
                    y += 1
                elif postingList1[x][0] > postingList2[y][0]:
                    y += 1
                elif postingList1[x][0] < postingList2[y][0]:
                    x += 1

            print(nearByQueryTerms)
            i += 1


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

    def mergePostingPositions(self, docId1, docId2, wordProximity):
        """merge sort postings lists, only return if items are within wordProximity of each other"""

        i = 0
        j = 0

        result = []
        positionOverlaps = []

        while len(result) != len(docId1) + len(docId2):
            if i == len(docId1):
                result += docId2[j:]

            elif j == len(docId2):
                result += docId1[i:]

            elif docId1[i] >= docId2[j]:
                if docId1[i] - docId2[j] <= wordProximity:
                    positionOverlaps.append(docId2[j])
                result.append(docId2[j])
                j += 1

            elif docId1[i] < docId2[j]:
                if docId2[j] - docId1[i] <= wordProximity:
                    positionOverlaps.append(docId1[i])
                result.append(docId1[i])
                i += 1

        print(result)
        print(positionOverlaps)
        return positionOverlaps

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

    one = [1, 6, 12, 19, 20, 989]
    two = [7, 14, 15, 20, 987]
    print(one)
    print(two)
    tester.mergePostingPositions(one, two, 2)