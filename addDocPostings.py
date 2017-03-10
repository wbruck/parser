from mergeScorePostingsList import mergeDocPostingList

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

    def betterQueryIndex(self, query):
        """query Index based on list of stemmed words"""
        terms = len(query)
        totalDocuments = []
        documentsSoFar = []
        i = 0

        while i <= terms:
            if i == 0:
                print ("term1 " + query[i] )
                print(self.termPosting[query[i]])
                print("term2" + query[i+1])
                print(self.termPosting[query[i+1]])

                documentsSoFar = self.twoTermQueryByPostings(self.termPosting[query[i]],
                                                             self.termPosting[query[i+1]])
                if len(documentsSoFar) > len(totalDocuments):
                    print("second run")
                    documentsSoFar = self.twoTermQueryByPostings(documentsSoFar,
                                                                 self.termPosting[query[i+2]])
            i += 1
            print("These are the docs")
        print(documentsSoFar)

    def twoTermQueryByPostings(self, postingList1, postingList2):
        """query Index based on list of stemmed words"""

        candidateDocs = []

        x = 0
        y = 0
        while x + y < len(postingList1) + len(postingList2):
            if x >= len(postingList1) or y >= len(postingList2):
                break

            if postingList1[x][0] == postingList2[y][0]:
                nearByQueryTerms = mergeDocPostingList(postingList1[x][1],
                                                       postingList2[y][1],
                                                       4)
                print('near by:')
                print(nearByQueryTerms)
                candidateDocs.append((postingList1[x][0], nearByQueryTerms))

                x += 1
                y += 1

            elif postingList1[x][0] > postingList2[y][0]:
                y += 1
            elif postingList1[x][0] < postingList2[y][0]:
                x += 1

        #print(candidateDocs)
        return candidateDocs


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





if __name__ == "__main__":
    #one = ['1', 'spray', '5quart', 'slow', 'cooker', 'with', 'cook', 'spray']

    tester = invertedIndex()

    #tester.indexDocument(one)

    one = [1, 6, 12, 19, 20, 989]
    two = [7, 14, 15, 20, 987]
    print(one)
    print(two)
    tester.mergePostingPositions(one, two, 2)