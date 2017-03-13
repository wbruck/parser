from mergeScorePostingsList import mergeDocPostingList
import InvertedIndex
from cosineSim import cosineSim
from itertools import combinations


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

                documentsSoFar = self.twoTermPostingsMerge(self.invertedIndex.termPosting[query[i]],
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

    def twoTermPostingsMerge(self, postingList1, postingList2, termProximity):
        """query Index based on list of stemmed words"""

        candidateDocs = []

        x = 0
        y = 0
        while x + y < len(postingList1) + len(postingList2):
            if x >= len(postingList1) or y >= len(postingList2):
                break

            if postingList1[x][0] == postingList2[y][0]:
                #print("DocID: " + str(postingList1[x][0]))
                nearByQueryTerms = mergeDocPostingList(postingList1[x][1],
                                                       postingList2[y][1],
                                                       termProximity)

                # print('near by:')
                # print(nearByQueryTerms)
                candidateDocs.append((postingList1[x][0], nearByQueryTerms))

                x += 1
                y += 1

            elif postingList1[x][0] > postingList2[y][0]:
                y += 1
            elif postingList1[x][0] < postingList2[y][0]:
                x += 1

        #print(candidateDocs)
        return candidateDocs


    def mergeEachPostingPair(self,query, termProximity):
        """create all unique pairs of query terms, merge positing lists for each pair"""

        termPairMergedPostings = []
        for terms in combinations(query, 2):

            print(terms)
            postingsMerged = self.twoTermPostingsMerge(self.invertedIndex.termPosting[terms[0]],
                                                       self.invertedIndex.termPosting[terms[1]],
                                                       termProximity)

            print(postingsMerged)
            termPairMergedPostings.append(postingsMerged)

        return termPairMergedPostings

    def showDocumentText(self, documentsByTermProximity, documentArray, distanceFromTerm):
        """Show text that may answer the query from the relevent documents"""
        for termPairProximity in documentsByTermProximity:
            for doc in termPairProximity:
                print(doc)
                docId = doc[0]

                i = 0

                while i < len(doc[1]) - 1:
                    positionA = doc[1][i]
                    positionB = doc[1][i+1]
                    print(docId)
                    if positionA - distanceFromTerm > 0:
                        positionA = positionA - distanceFromTerm
                    else:
                        positionA = 0
                    print(documentArray[docId - 1].split(' ')[positionA:(positionB + distanceFromTerm)])

                    i += 2

    def consolidateDocProximityList(self, firstDocList, docProximityList):
        """consolidate the list of documents X term pair proximity"""

        # turn all document proximities into a dict, reference by key, join the lists consolidate lists





    def getKNearestDocs(self, query, docTermMatrix, k):
        """Return the K most similar documents to the query"""

        queryDict = {}

        for term in query:
            queryDict[str(term)] = 1

        newMatrix = docTermMatrix.append(queryDict, ignore_index=True).fillna(0)

        qVec = newMatrix.iloc[-1]

        #print(newMatrix.shape)

        i = 1
        documentSimilarities = {}
        while i < newMatrix.shape[0] - 1:
            documentSimilarities[i] = cosineSim(qVec, newMatrix.iloc[i])
            i += 1

        print(documentSimilarities)
        rankedDocSim = sorted(documentSimilarities.items(), key=lambda x: x[1], reverse=True)

        nearestKDocs = []
        j=0
        while j <= k:
            print(rankedDocSim[j])
            if rankedDocSim[j][1] ==0:
                break
            nearestKDocs.append(rankedDocSim[j][0])
            j += 1

        return nearestKDocs