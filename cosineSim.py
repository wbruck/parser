import math


def cosineSim(vec1, vec2):
    """Calculate the cosine similarity of 2 vectors"""
    aTot = 0
    bTot = 0

    numerator = 0

    for a,b in zip(vec1,vec2):

        #print(str(a) + ", "+ str(b))
        numerator += (a*b)
        aTot += a*a
        bTot += b*b

    return numerator/math.sqrt(aTot*bTot)

def getKNearest(matrix):
    print("what")