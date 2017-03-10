def mergeDocPostingList(docId1, docId2, wordProximity):
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

    print('result')
    print(result)
    print('positionOverlap: ')
    print( positionOverlaps)

    return result


def retrieveBestDocs(queryDocs, wordProximity):
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


def getTextPositionOfDoc(docId, queryDocs, termDistance):
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