one = '1. Spray 5-quart slow cooker with cooking spray. In large bowl, mix melted butter, Worcestershire sauce, seasoned salt and garlic. Add chicken; toss to coat. Pour mixture into slow cooker.'
two = '2 In same bowl, mix tomatoes, soup and chiles; pour over chicken.'
three = '3 Cover; cook on High heat setting 2 to 3 hours or on Low heat setting 3 to 4 hours or until instant-read thermometer inserted in thickest part of chicken reads at least 165F.'
four = '4 Remove chicken from slow cooker, and transfer to cutting board; let stand 5 minutes or until cool enough to handle. Meanwhile, stir cream cheese and Cheddar cheese into slow cooker. Cover; cook on High heat setting 5 to 10 minutes or until cheese melts. Stir.'
five = '5 Meanwhile, shred chicken with 2 forks; return to slow cooker, and stir in cooked spaghetti. Top with parsley.'

steps = [one, two, three, four, five]


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


# this is all wrong... dont merge term 3 with completed 2term dic
if len(documentsSoFar) > len(totalDocuments):
    print("second run")
    print(documentsSoFar)
    print(self.invertedIndex.termPosting[query[i + 2]])
    recursiveDocs = self.twoTermQueryByPostings(documentsSoFar,
                                                self.invertedIndex.termPosting[query[i + 2]])
    if len(recursiveDocs) > len(documentsSoFar):
        documentsSoFar = recursiveDocs
        # this is where is stops being wrong