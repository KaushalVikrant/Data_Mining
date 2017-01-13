import itertools

pathForAttributes="E:\Semester 2\Data Mining\Assignments\Assignment 3\Data Sets\Mushroom\\attributes.txt"
pathForData="E:\Semester 2\Data Mining\Assignments\Assignment 3\Data Sets\Mushroom\\agaricus-lepiota.data.txt"
pathForTest="E:\Semester 2\Data Mining\Assignments\Assignment 3\Data Sets\Nursery\\testing file.txt"

pathForIndividualAttributesList="E:\Semester 2\Data Mining\Assignments\Assignment 3\Data Sets\Mushroom\\individualAttList.txt"



individualAttributeList=[]
attributeList=[]                #All attributes of dataset
dataList=[]                     #Whole data
minSupportThreshold=30          #Minimum Support Threshold
minConfidenceThreshold=70       #minimum Confidence Threshold
minLiftThreshold=0.99             #minimum lift
frequentItemSetListF1=[]
finalFrequenItemSets=[]
totalSupportDict={}             #Support of frequent itensets
finalAssociationRules={}
totalGeneratedCandidates=[]     #All candidates itemsets
finalRules=[]                   #Final Rules
maximalFrequentItemSets={}      #Maximal Frequent Item Sets 1=Yes and 0=No
closedFrequentItemSets={}       #Closed Frequent Item Sets 1=Yes and 0=No
top10Rules=[]
oneFromFIS=[]
method=-1
prunedBecauseOfLessConfidence=0
bruteForceCount=0


def readIndividualAttributeList(path):
    f = open(path, 'r')

    for data in f:
        #if not data.strip():
        #    continue
        row=data.split(',')
        tempList=[]
        for values in row:
        #   if not values.strip():
        #       continue
            values=values.rstrip().lstrip()
            tempList.append(values)
        individualAttributeList.append(tempList)

def readFile(path,source):
    f = open(path, 'r')
    for data in f:
        if not data.strip():
            continue
        row=data.split(',')
        if row[0] == '\n':
            continue
        count=0
        tempList=[]
        for values in row:
            if count==11:
                count+=1
                continue
            values=values.strip()
            values=values.rstrip().lstrip()
            for inside in individualAttributeList[count]:

                if values == inside:
                    tempList.append(1)
                else:
                    tempList.append(0)
            count+=1
        source.append(tempList)



#############################################





def readAttributesFile(path):
    f=open(path,'r')

    for data in f:
        if not data.strip():
            continue
        row=data.split(',')
        if not row:
            continue
        for val in row:
            if not val.strip():
                continue
            val=val.rstrip().lstrip()
            attributeList.append(val)



def enumerateSupportHashFirst(totalIndexList,source,k):
    itemSetDict={}
    for sets in totalIndexList:
        itemSetDict.update({(sets):0})
    for transaction in source:
        count=0
        oneList=[]
        for enumerateOne in transaction:
            if enumerateOne==1:
                oneList.append(count)
            count+=1
        for subset in oneList:
            itemSetDict[subset]=itemSetDict.get(subset)+1
    return itemSetDict

def enumerateSupportHash(totalIndexList,source,k):
    itemSetDict={}
    for sets in totalIndexList:
        itemSetDict.update({(sets):0})
    for transaction in source:
        if not itemSetDict:
            break
        count=0
        oneList=[]
        for enumerateOne in transaction:
            if enumerateOne==1:
                oneList.append(count)
            count+=1
        for subset in itertools.combinations(oneList, k):
            if itemSetDict.has_key(subset):
                itemSetDict[subset]=itemSetDict.get(subset)+1
    return itemSetDict



def enumerateSupport(indexesList,source):
    support=0
    for row in source:
        count=0
        for index in indexesList:
            if int(row[index])==0:
                break
            count+=1
        if count == len(indexesList):
            support+=1
    return support


def createItemSetsF1(indexLists):
    resultList=[]
    for indexes in indexLists:
        for j in frequentItemSetListF1:
            if j not in indexes:
                if indexes[len(indexes)-1] < j:


                    for number in range(0,len(indexes)):
                        tempList=[]
                        skip=0
                        for subset in indexes:
                            if number == skip:
                                skip+=1
                                continue
                            else:
                                tempList.append(subset)
                            skip+=1
                        tempList.append(j)
                        if tempList not in indexLists:
                            break
                        temp=list(indexes)
                        temp.append(j)
                        if temp not in resultList:
                            resultList.extend([tuple(temp)])
                            totalGeneratedCandidates.append(temp)
                        #if temp not in finalFrequenItemSets:
                            #finalFrequenItemSets.append(temp)
    return resultList

def createItemSetsF1AP(indexLists):
    resultList=[]
    for indexes in indexLists:
        for j in frequentItemSetListF1:
            if j not in indexes:
                if indexes[len(indexes)-1] < j:


                    for number in range(0,len(indexes)):
                        tempList=[]
                        skip=0
                        for subset in indexes:
                            if number == skip:
                                skip+=1
                                continue
                            else:
                                tempList.append(subset)
                            skip+=1
                        tempList.append(j)
                        tempList=tuple(tempList)
                        if tempList not in indexLists:
                            break
                        temp=list(indexes)
                        temp.append(j)
                        temp=tuple(temp)
                        if temp not in resultList:
                            resultList.extend([tuple(temp)])
                            totalGeneratedCandidates.append(temp)
                        #if temp not in finalFrequenItemSets:
                            #finalFrequenItemSets.append(temp)
    return resultList
"""
def createItemSetsF1Again(indexLists):
    resultList=[]
    for indexes in indexLists:
        for j in frequentItemSetListF1:
            if j not in indexes:
                if indexes[len(indexes)-1] < j:


                    for number in range(0,len(indexes)):
                        tempList=[]
                        skip=0
                        for subset in indexes:
                            if number == skip:
                                skip+=1
                                continue
                            else:
                                tempList.append(subset)
                            skip+=1
                        tempList.append(j)
                        tempList=tuple(tempList)
                        if tempList not in indexLists:
                            break
                        temp=list(indexes)
                        temp.append(j)
                        temp=tuple(temp)
                        if temp not in resultList:
                            resultList.append(temp)
                            totalGeneratedCandidates.append(temp)
                        #if temp not in finalFrequenItemSets:
                            #finalFrequenItemSets.append(temp)
    return resultList
"""

def createItemSetsF1Again(indexLists):
    resultList=[]
    for indexes in indexLists:
        for j in frequentItemSetListF1:
            if j not in indexes:
                if indexes[len(indexes)-1] < j:


                    for number in range(0,len(indexes)):
                        tempList=[]
                        skip=0
                        for subset in indexes:
                            if number == skip:
                                skip+=1
                                continue
                            else:
                                tempList.append(subset)
                            skip+=1
                        tempList.append(j)
                        tempList=tuple(tempList)

                        temp=list(indexes)
                        temp.append(j)
                        temp=tuple(temp)


                        if temp not in resultList:
                            totalGeneratedCandidates.append(temp)
                            if tempList not in indexLists:
                                break
                            resultList.append(temp)

                        #if temp not in finalFrequenItemSets:
                            #finalFrequenItemSets.append(temp)
    return resultList

##########################################################
def ruleGeneration(frequentItemSet):
    total=len(dataList)
    for frequentIS in frequentItemSet:
        tempList=[]
        for value in frequentItemSet:

            tempList.append(value)


        print "done"

def findConfidence(frequentIS):
    once=0
    tempFinalAssociationRules={}
    lowConfidenceConsequentList=[]
    for fs in range(0,len(frequentIS)):
        antecedent=[]
        for elements in frequentIS:
            if once==fs:
                once+=1
                consequent=elements
            else:
                antecedent.append(elements)
        antecedent=tuple(antecedent)
        confidence = totalSupportDict(antecedent)/totalSupportDict(consequent)
        if confidence > minConfidenceThreshold:
            tempFinalAssociationRules.update({antecedent:consequent})
        else:
            lowConfidenceConsequentList.append(consequent)


    print "test"

def findsubsets(S,m):
    return set(itertools.combinations(S, m))

def updateClosedFrequentItemSets(frequentItemSet,k,source):
    doneList=[]
    for frequentIS in frequentItemSet:
        for sub in findsubsets(frequentIS,k):
            if sub in doneList:
                continue
            temp=sub
            if len(sub) == 1:
                sub=sub[0]
            support=totalSupportDict.get(sub)
            if totalSupportDict.get(frequentIS) == support:
                if support > minSupportThreshold*len(source)/100:       #Though not requied here as incoming itemSets are already frequent
                    if closedFrequentItemSets.has_key(sub):
                        doneList.append(temp)
                        closedFrequentItemSets.update({sub:0})
                    else:
                        print "closedFrequentItemSets dictionary doesn't has item/key: "+ str(sub)

def updateMaximalFrequentItemSets(frequentItemSet,k):
    doneList=[]
    for frequentIS in frequentItemSet:
        for sub in findsubsets(frequentIS,k):
            if sub in doneList:
                continue
            temp=sub
            if len(sub) == 1:
                sub=sub[0]
            if maximalFrequentItemSets.has_key(sub):
                doneList.append(temp)
                maximalFrequentItemSets.update({sub:0})
            else:
                print "maximalFrequentItemSets dictionary doesn't has item/key: "+ str(sub)



def ruleGenerationConfidence(frequentItemSet):
    total=len(dataList)
    lessConfidence=[]

    for frequentIS in frequentItemSet:
        global bruteForceCount
        bruteForceCount+=2**len(frequentIS)-2
        if len(frequentIS) == 1:
            continue
        returnedList=[]

        tempList=[]
        for m in range(1,len(frequentIS)):
            for sub in findsubsets(frequentIS,m):
                returnedList.append(sub)
        for subsets in returnedList:
            boo=True
            temp=subsets
            if len(subsets) == 1:
                subsets=subsets[0]
            confidence=(float(totalSupportDict.get(frequentIS))/totalSupportDict.get(subsets))*100
            if confidence > minConfidenceThreshold:
                string=""

                for values in frequentIS:
                    if values not in temp:
                        string=string+str(attributeList[int(values)])+" , "
                        #string=string+str(values)+" , "
                antecedentStr=""
                for toFetchAttNames in temp:         #should be temp here
                    antecedentStr=antecedentStr+" , "+attributeList[int(toFetchAttNames)]
                #rule=str(antecedentStr[3:])+"  ---->  "+str(string[0:-2])+ "    confidence: "+str(confidence)
                rule=str(antecedentStr[3:])+"  ---->  "+str(string[0:-2])
                top10Rules.append([totalSupportDict.get(frequentIS),confidence,rule])
                tempList.append([totalSupportDict.get(frequentIS),confidence,rule])
                #rule=str(subsets)+"  ---->  "+str(string[0:-2])+ "    confidence: "+str(confidence)
                finalRules.append(rule)
            else:
                global prunedBecauseOfLessConfidence
                prunedBecauseOfLessConfidence+=1



        if tempList:
            supportSorted= sorted(tempList,key=lambda x: -x[0])
            oneFromFIS.append(supportSorted[0])
    global noOfAssociationRulesGenerated
    noOfAssociationRulesGenerated=len(finalRules)
    #return finalRules
    return oneFromFIS

def ruleGenerationLift(frequentItemSet):
    total=len(dataList)
    lessConfidence=[]
    doneList={}
    for frequentIS in frequentItemSet:
        returnedList=[]
        tempList=[]
        for m in range(1,len(frequentIS)):
            for sub in findsubsets(frequentIS,m):
                returnedList.append(sub)
        for subsets in returnedList:
            boo=True
            temp=subsets
            if len(subsets) == 1:
                subsets=subsets[0]
            #confidence=(float(totalSupportDict.get(frequentIS))/totalSupportDict.get(subsets))*100
            confidence=(float(totalSupportDict.get(frequentIS))/totalSupportDict.get(subsets))
            listToTuple=[]
            for values in frequentIS:
                if values not in temp:
                    listToTuple.append(values)
            if len(listToTuple) == 1:
                listToTuple=listToTuple[0]
            else:
                listToTuple=tuple(listToTuple)
            #lift=float(confidence)/totalSupportDict.get(listToTuple)*100
            lift=(float(confidence)/totalSupportDict.get(listToTuple))*len(dataList)
            if lift > minLiftThreshold:
                string=""

                for values in frequentIS:
                    if values not in temp:
                        string=string+str(attributeList[int(values)])+" , "
                        #string=string+str(values)+" , "
                antecedentStr=""
                for toFetchAttNames in temp:
                    antecedentStr=antecedentStr+" , "+attributeList[int(toFetchAttNames)]
                #rule=str(antecedentStr[3:])+"  ---->  "+str(string[0:-2])+ "    Lift: "+str(lift)
                rule=str(antecedentStr[3:])+"  ---->  "+str(string[0:-2])
                top10Rules.append([lift,confidence,rule])
                """
                print doneList.get(antecedentStr[3:])
                print type(doneList.get(antecedentStr[3:]))

                print doneList.has_key(antecedentStr[3:])
                """
                if doneList.get(antecedentStr[3:]):
                    f=str(doneList.get(antecedentStr[3:]))
                if doneList.has_key(antecedentStr[3:]) and len(doneList.get(antecedentStr[3:])) >= len(string[0:-2]):
                    continue
                tempList.append([lift,confidence*100,rule,str(antecedentStr[3:]),str(string[0:-2])])
                #rule=str(subsets)+"  ---->  "+str(string[0:-2])+ "    confidence: "+str(confidence)
                finalRules.append(rule)
        if tempList:
            supportSorted= sorted(tempList,key=lambda x: -x[0])
            oneFromFIS.append(supportSorted[0][0:3])
            doneList.update({supportSorted[0][3]:supportSorted[0][4]})
    global noOfAssociationRulesGenerated
    noOfAssociationRulesGenerated=len(finalRules)
    return oneFromFIS

##########################################################################################



def Apriori(source):
    k=1
    createFISindexList=[]
    totalAttributes=len(attributeList)
    totalDataPoints=len(source)
    for i in range(0,totalAttributes):
        result=enumerateSupport([i],source)
        if result > minSupportThreshold*totalDataPoints/100:
            frequentItemSetListF1.append(i)
            createFISindexList.append([i])
    once=1
    while True:
        if once==1:
            once=2
            createFISindexList=createItemSetsF1(createFISindexList)
        else:
            createFISindexList=createItemSetsF1AP(createFISindexList)

        tempList=[]
        for i in createFISindexList:
            result=enumerateSupport(i,dataList)
            if result > minSupportThreshold*totalDataPoints/100:
                tempList.append(i)
                finalFrequenItemSets.append(i)
        if not tempList:
            break
        createFISindexList=tempList

def AprioriAgain(source):
    k=1
    prevResult=[]
    createFISindexList=[]
    totalAttributes=len(attributeList)
    totalDataPoints=len(source)

    """
    for i in range(0,totalAttributes):
        result=enumerateSupport([i],source)
        if result > minSupportThreshold*totalDataPoints/100:
            frequentItemSetListF1.append(i)
            createFISindexList.append([i])
            totalSupportDict.update({i:result})
    """

    numberAttList=[]
    for i in range(0,totalAttributes):
        numberAttList.append(i)

    result=enumerateSupportHashFirst(numberAttList,dataList,k)
    for supportCount in result:
            support=result.get(supportCount)
            if support > minSupportThreshold*totalDataPoints/100:
                #tempList.append(supportCount)
                #finalFrequenItemSets.append(supportCount)
                frequentItemSetListF1.append(supportCount)
                createFISindexList.append([supportCount])
                totalSupportDict.update({supportCount:support})
                maximalFrequentItemSets.update({supportCount:1})
                closedFrequentItemSets.update({supportCount:1})
            #createFISindexList.append((i))
    once=1
    while True:
        if once==1:
            once=2
            createFISindexList=createItemSetsF1(createFISindexList)
        else:
            createFISindexList=createItemSetsF1Again(createFISindexList)
        tempList=[]
        k+=1
        createFISindexList=tuple(createFISindexList)
        result=enumerateSupportHash(createFISindexList,dataList,k)
        for supportCount in result:
            support=result.get(supportCount)
            if support > minSupportThreshold*totalDataPoints/100:
                tempList.append(supportCount)
                finalFrequenItemSets.append(supportCount)
                totalSupportDict.update({supportCount:support})
                maximalFrequentItemSets.update({supportCount:1})
                closedFrequentItemSets.update({supportCount:1})
        updateMaximalFrequentItemSets(tempList,k-1)
        updateClosedFrequentItemSets(tempList,k-1,source)
        if not tempList:
            break
        prevResult=tempList
        createFISindexList=tempList
    #rules=confidencePruning(finalFrequenItemSets)
    if method==1:
        rules=ruleGenerationConfidence(finalFrequenItemSets)
    else:
        rules=ruleGenerationLift(finalFrequenItemSets)
    global noOfAssociationRulesGeneratedConsidered
    noOfAssociationRulesGeneratedConsidered=len(rules)
    #for rule in rules:
    #    print rule






readAttributesFile(pathForAttributes)
readIndividualAttributeList(pathForIndividualAttributesList)
#readFile(pathForData,dataList)
readFile(pathForData,dataList)

while  method not in [1,2]:
    method = input('1 for Confidence\n2 for Lift\nWhich method for rule generation: ')
    method=int(method)
    if method not in [1,2]:
        print "Please enter either 1 or 2"


AprioriAgain(dataList)
#Apriori(dataList)



countMaximalFIS=0
for mfIS in maximalFrequentItemSets:
    if maximalFrequentItemSets.get(mfIS) == 1:
        countMaximalFIS+=1

countClosedFIS=0
for cfIS in closedFrequentItemSets:
    if closedFrequentItemSets.get(cfIS) == 1:
        countClosedFIS+=1

#############################
supportSorted= sorted(oneFromFIS,key=lambda x: -x[0])
confidenceSorted=sorted(oneFromFIS,key=lambda x: -x[1])

confidenceTop15=confidenceSorted[0:15]
supportTop10=supportSorted[0:10]

import operator
list1 = sorted(confidenceTop15, key=operator.itemgetter(0,1), reverse=True)
list1=list1[0:10]
##############################

if method==1:
    print "Total association rules by brute force: "+ str(bruteForceCount)
    print "Total association rules generated: "+str(bruteForceCount-prunedBecauseOfLessConfidence)
    print "Savings because of confidence pruning: "+str(prunedBecauseOfLessConfidence)
    print "Top 10 Association rules"
    print "Support      Confidence      Association Rule"
else:
    print "Top 10 Association rules"
    print "Lift      Confidence      Association Rule"
for items in list1:
    print items

"""
supportSorted= sorted(top10Rules,key=lambda x: -x[0])
confidenceSorted=sorted(top10Rules,key=lambda x: -x[1])

confidenceTop10=confidenceSorted[0:10]
supportTop10=supportSorted[0:10]

import operator
list1 = sorted(top10Rules, key=operator.itemgetter(0, 1))

##############################
"""


print "\n\nTotal number of candidates generated:  "+ str(len(totalGeneratedCandidates))
print "Total number of Frequent itemsets:  "+ str(len(totalSupportDict))
print "Total Maximal Frequent items sets are: "+ str(countMaximalFIS)
print "Total CLosed Frequent items sets are: "+ str(countClosedFIS)
print "Total number of association rules generated: "+ str(noOfAssociationRulesGenerated)
print "Single itemset can generate many association rules but we have considered just one best association rules in an" \
      " item set."
print "Total number of association rules considered: "+ str(noOfAssociationRulesGeneratedConsidered)

print "done"
