from mergeScorePostingsList import mergeDocPostingList
import InvertedIndex

class Query(object):
    invertedIndex = None

    def __init__(self, invertedIndex):
        self.invertedIndex = invertedIndex

    def betterQueryIndex(self, query):
        """query Index based on list of stemmed words"""
        terms = len(query)
        totalDocuments = []
        documentsSoFar = []
        i = 0

        while i <= terms:
            if i == 0:
                print ("term1 " + query[i] )
                print(self.invertedIndex.termPosting[query[i]])
                print("term2" + query[i+1])
                print(self.invertedIndex.termPosting[query[i+1]])

                documentsSoFar = self.twoTermQueryByPostings(self.invertedIndex.termPosting[query[i]],
                                                             self.invertedIndex.termPosting[query[i+1]])


        i += 1
        print("These are the docs")
        print(documentsSoFar)
        return documentsSoFar

    def documentScores(self, documentPostings):

        scoresList = []

        for posting in documentPostings:
            score = len(posting[1])
            scoresList.append((posting[0],score))

        return scoresList

    def twoTermQueryByPostings(self, postingList1, postingList2):
        """query Index based on list of stemmed words"""

        candidateDocs = []

        x = 0
        y = 0
        while x + y < len(postingList1) + len(postingList2):
            if x >= len(postingList1) or y >= len(postingList2):
                break

            if postingList1[x][0] == postingList2[y][0]:
                print("DocID: " + str(postingList1[x][0]))
                nearByQueryTerms = mergeDocPostingList(postingList1[x][1],
                                                       postingList2[y][1],
                                                       4)
                newPosting = (postingList1[x][0], nearByQueryTerms)
                ### recursivly merge postings for the next query term here with newPosting
                #for posting in list1:
                #   call twoTermPosting([posting],Query)
                #nearByQueryTerms = self.twoTermQueryByPostings(newPosting, otherPosting)
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



