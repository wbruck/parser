from mergeScorePostingsList import mergeDocPostingList
import InvertedIndex
from cosineSim import cosineSim
from itertools import combinations
from path import Path
from Parser import stemText


class Query(object):
    invertedIndex = None
    query = ''

    def __init__(self, invertedIndex):
        self.invertedIndex = invertedIndex

    def setQuery(self, query):
        self.query = query

    def runQuery(self, query):
        stemmedQuery = stemText(query)

        docsWithTermProximity = self.mergeEachPostingPair(stemmedQuery, 5)

        # print(docsWithTermProximity)

        shortList = self.consolidateDocProximityList(docsWithTermProximity, 5)
        self.showDocumentText(shortList, 10)


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
                if len(nearByQueryTerms) != 0:
                    candidateDocs.append((postingList1[x][0], nearByQueryTerms))

                x += 1
                y += 1

            elif postingList1[x][0] > postingList2[y][0]:
                y += 1
            elif postingList1[x][0] < postingList2[y][0]:
                x += 1

        #print(candidateDocs)
        return candidateDocs


    def mergeEachPostingPair(self, query, termProximity):
        """create all unique pairs of query terms, merge positing lists for each pair"""

        self.setQuery(query)

        termPairMergedPostings = []
        for terms in combinations(query, 2):

            #print(terms)
            postingsMerged = self.twoTermPostingsMerge(self.invertedIndex.termPosting[terms[0]],
                                                       self.invertedIndex.termPosting[terms[1]],
                                                       termProximity)

            #print(postingsMerged)
            termPairMergedPostings.append(postingsMerged)

        return termPairMergedPostings

    def showDocumentText(self, documentsByTermProximity, distanceFromTerm):
        """Show text that may answer the query from the top 3 most relevant documents determined with cosine similarity to query"""


        #for termPairProximity in documentsByTermProximity:
        totalSections = 0

        print("Documents Retrived: " + str(len(documentsByTermProximity)))

        blurbInvertedIndex = InvertedIndex.InvertedIndex()
        blurbList = []

        for doc in documentsByTermProximity: #termPairProximity:

            docId = doc[0]

            sectionsFound = (len(doc[1])/2)

            documentFile = self.invertedIndex.listOfFiles[docId - 1]
            rawDocumentText = Path(documentFile).text(encoding='utf8')
            documentText = [word.lower().replace('\n', '') for word in rawDocumentText.split(' ') if word.strip() != '']

            i = 0

            while i < len(doc[1]) - 1:
                positionA = doc[1][i]
                positionB = doc[1][i+1]

                if positionA - distanceFromTerm > 0:
                    positionA = positionA - distanceFromTerm
                else:
                    positionA = 0

                termsInDoc = ' '.join(documentText[positionA:(positionB + distanceFromTerm)])

                blurbList.append(termsInDoc)

                blurbInvertedIndex.indexDocument(stemText(termsInDoc), '')

                i += 2

            totalSections += sectionsFound

        print("Sections Retrieved: " + str(totalSections))

        blurbMatrix = blurbInvertedIndex.createTermDocMatrix()
        bestBlurbs = self.getKNearestDocs(self.query, blurbMatrix, 3)

        print("Showing Best 3 Results:")
        for blurbNum in bestBlurbs:
            print(blurbNum)
            print(blurbList[blurbNum-1])

    def consolidateDocProximityList(self, docTermProximityList, x):
        """consolidate the list of documents X term pair proximity"""
        combinedDocPostingsDict = {}

        # turn all document proximities into a dict, reference by key, join the lists consolidate lists
        for termProximity in docTermProximityList:
            for documentProximity in termProximity:
                try:
                    combinedDocPostingsDict[documentProximity[0]] += documentProximity[1]
                except:
                    combinedDocPostingsDict[documentProximity[0]] = documentProximity[1]

        #print(combinedDocPostingsDict)

        docTermConsolidatedPositions = []

        for document, positions in combinedDocPostingsDict.items():

            sortedPositionsList = sorted(positions)
            lowestPosition = sortedPositionsList[0]
            positionPairs = []
            positionPairs.append(lowestPosition)

            for nextPosition in sortedPositionsList:

                if (nextPosition - lowestPosition) <= x:
                    lowestPosition = nextPosition
                    continue
                else:
                    positionPairs.append(lowestPosition)
                    positionPairs.append(nextPosition)
                    lowestPosition = nextPosition

            positionPairs.append(lowestPosition)

            docTermConsolidatedPositions.append((document, positionPairs))

        return docTermConsolidatedPositions

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

        #print(documentSimilarities)
        rankedDocSim = sorted(documentSimilarities.items(), key=lambda x: x[1], reverse=True)

        nearestKDocs = []

        if len(rankedDocSim)-1 <= k:
            k = len(rankedDocSim)-1
        else:
            k -= 1

        j=0
        while j <= k:
            print(rankedDocSim[j])
            if rankedDocSim[j][1] == 0:
                break
            nearestKDocs.append(rankedDocSim[j][0])
            j += 1

        return nearestKDocs