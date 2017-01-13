import operator
import random
import math

pathForBaseFile='E:\Semester 2\Data Mining\Assignments\Assignment 2\Data Iris\iris.data.txt'
#pathForBaseFile='E:\Semester 2\Data Mining\Assignments\Assignment 2\Data Iris\\trainData.txt'
#pathForTestFile='E:\Semester 2\Data Mining\Assignments\Assignment 2\Data Iris\\testData2.txt'
interval=10
dataList=[]
testData=[]
minList=[]
maxList=[]
classVariable=[]
attributeAlreadyDone=[]
doneAttribute=[]
nFold=10
#classVariableTest=['Iris-setosa', 'Iris-versicolor', 'Iris-virginica']
attributeList=["sepal length","sepal width","petal length","petal width"]
threshholdStop=8
threshholdClassStop=8
class Node:
    def __init__(self,name,splitAttribute,splitValue,leftChildren,rightChildren,symbol,entropy):
        self.name=name
        self.splitAttribute=splitAttribute
        self.splitValue=splitValue
        self.leftChild=leftChildren
        self.rightChild=rightChildren
        self.symbol=symbol
        self.entropy=entropy


def readFile(path,dataList):
    f = open(path, 'r')

    #wineList=[]
    once=1

    for data in f:
        #attributesList=[]
        count=0
        row=data.split(',')
        if not row:
            continue
        if once==1:
            length=len(row)
            for i in range(0,length-1):
                maxList.append(-999999)
                minList.append(999999)
                once=2
        classVar=""
        tempList=[]
        for att in row:

            try:
                float(att)
            except ValueError:
                classVar=att.rstrip()
                if att.rstrip() not in classVariable:
                    classVariable.append(att.rstrip())
                continue
            value=float(att)
            if maxList[count] < value:
                maxList[count]=value
            if minList[count]>value:
                minList[count]=value
            count+=1
            tempList.append(value)
        tempList.append(classVar)
        dataList.append(tempList)

def stopping_cond(sourceList):
    length=len(sourceList[0])
    checkingClassvar=0
    for inner in sourceList:
        if inner[length-1] not in classVariable:
            checkingClassvar+=1
        else: break

    if checkingClassvar==len(sourceList):
        str="not", classVariable[0]
        return [True,str]

    if len(sourceList)<threshholdStop:
        temp={}
        for value in sourceList:
            classType=value[length-1]
            if temp.has_key(classType):
                temp[classType]=temp.get(classType)+1
            else:
                temp.update({classType:int(1)})
        #max class variable in left entries
        maxClassLeft=-9999
        key=""
        for data in temp:
            count=temp.get(data)
            if maxClassLeft<count:
                maxClassLeft=count
                key=data

        return [True,key]

    classVar=[]
    once=0
    tempList=[]
    classVarCount={}

    for valuesList in sourceList:
        temp=valuesList[length-1]
        if once==0:
            classVar.append(temp)
            once=1
            continue
        if temp not in classVar:
            # if multiple class variable present then return false as program should not stop here
            break
        once+=1

    #if all belongs to same class then stop
    if once == len(sourceList):
        #classVar[0] contains that node should be clasified as this class variable
        return [True,0]

    # if sourcelist contains simillar entries and just class variable are different then it should stop
    for valuesList in sourceList:
        # creating a sub list leaving class variable to check if left data is same
        sublist=valuesList[0:length-1]
        classType=valuesList[length-1]
        if classVarCount.has_key(classType):
            classVarCount[classType]=classVarCount.get(classType)+1
        else:
            classVarCount.update({classType:int(1)})
        if sublist not in tempList:
            tempList.append(sublist)
            if(len(tempList)>1):
                return [False,0]

    #max class variable in left entries
    maxClassLeft=-9999
    key=""
    for data in classVarCount:
        count=classVarCount.get(data)
        if maxClassLeft<count:
            maxClassLeft=count
            key=data
    # if sourcelist contains simillar entries and just class variable are different then it should stop
    #key is the maximum left class variable
    return [True,key]








def calculateGINIinfo(countList):
    # countList contains mainCOunt,othersCount for the number of split

    leftMain=countList[0]
    leftOthers=countList[1]
    totalLeft=leftMain+leftOthers
    rightMain=countList[2]
    rightOthers=countList[3]
    totalRight=rightMain+rightOthers

    MainList=[]
    OthersList=[]

    if totalLeft!=0:
        leftNode= 1-((float(leftMain)/totalLeft)**2)-((float(leftOthers)/totalLeft)**2)
    else:
        leftNode=0
    if totalRight!=0:
        rightNode= 1-((float(rightMain)/totalRight)**2)-((float(rightOthers)/totalRight)**2)
    else:
        rightNode=0
    """
    for i in range(0,len(countList)):
        if i%2==0:
            MainList.append(countList[i])
        else:
            OthersList.append(countList[i])
    """
    #segregating main and other. And then finding gini for all created nodes
    #MainList contains mainvalues
    #OthersList contains other values
    nodeGINI=[]
    allTotal=0
    totalIndividualNode=[]
    """
    for val in range(0,len(countList),2):
        Main=MainList[val]
        Others=OthersList[val+1]
        allTotal+=Main+Others
        total=Main+Others
        totalIndividualNode.append(total)
        nodeGINI.append(1-((Main/total)**2)-((Others/total)**2))
    """
    for val in range(0,len(countList),2):
        Main=countList[val]
        Others=countList[val+1]
        allTotal+=Main+Others
        total=Main+Others
        totalIndividualNode.append(total)
        if total!=0:
            nodeGINI.append(1-((float(Main)/total)**2)-((float(Others)/total)**2))
        else:
            nodeGINI.append(0)

    totalGINI=0

    for node in range(0,len(nodeGINI)):
        totalGINI+=(float(totalIndividualNode[node])/allTotal)*nodeGINI[node]
    return totalGINI

def calculateMinMax(Data):
    classPresent=[]
    lengthData=len(Data[0])
    for i in range(0,len(maxList)-1):
        minList[i]=9999
        maxList[i]=-9999

    for values in Data:
        count=0
        if values[lengthData-1] not in classPresent:
            classPresent.append(values[lengthData-1])
        for inner in values[0:len(values)-1]:
            if minList[count] > inner:
                minList[count] = inner
            if maxList[count] < inner:
                maxList[count] = inner
            count+= 1



def findBestSplit(Data):
    count=0
    # make correction
    length=len(Data[0])-1
    calculateMinMax(Data)

    toReturnList=[]
    for features in range(0,length):
        minValue=minList[features]          # min and max (next line) for this feature
        maxValue=maxList[features]
        intervalLength=(maxValue-minValue)/interval
        splitAt=minValue
        tempListForGINI=[]
        finalLeftList=[]
        finalRightList=[]
        GINIlist=[]
        for i in range(0,interval):

            splitAt+=intervalLength         # increasing intervals value
            for classValue in classVariable:
                leftCountMain=0
                leftCountOthers=0
                rightCountMain=0
                rightCountOthers=0
                leftList=[]
                rightList=[]
                leftDict={}
                rightDict={}
                for att in Data:
                    if att[features]<=splitAt:          #if value is smaller than split value
                        leftList.append(att)
                        if att[length]==classValue:      # if class variable is main or others for binary split
                            leftCountMain+=1
                        else:
                            leftCountOthers+=1
                    else:
                        rightList.append(att)
                        if att[length]==classValue:      # if class variable is main or others for binary split
                            rightCountMain+=1
                        else:
                            rightCountOthers+=1

                finalLeftList.append(leftList)
                finalRightList.append(rightList)
                # create a list of gini for different interval values
                tempGINI=calculateGINIinfo([leftCountMain,leftCountOthers,rightCountMain,rightCountOthers])
                tempListForGINI.append(tempGINI)
        GINIlist.append(tempListForGINI)

        minGINI=99999
        giniOfWhichAttribute=-100
        numberInterval=-99
        for gini in GINIlist:
            for inner in gini:
                if minGINI>inner:
                    minGINI=inner
                    giniOfWhichAttribute=features
                    index=gini.index(inner)
                    numberInterval=(index/len(classVariable))+(index%len(classVariable))      #to find internal index
        resultValueforSplit=minList[giniOfWhichAttribute]+(intervalLength*(numberInterval+1))
        #listNumber=numberInterval*len(classVariable)+giniOfWhichAttribute

        #toReturnList.append([minGINI,giniOfWhichAttribute,resultValueforSplit,finalLeftList[],finalRightList[listNumber]])
        toReturnList.append([minGINI,giniOfWhichAttribute,resultValueforSplit,finalLeftList[index],finalRightList[index]])




    lastIndex=9999
    lastGINI=99
    for last in toReturnList:
        if last[0]<lastGINI:
            lastGINI=last[0]
            lastIndex=toReturnList.index(last)


    indexCount=[]
    for check in toReturnList:
        if check[0]==lastGINI:
            indexCount.append(toReturnList.index(check))
    leastIndexCount=len(indexCount)
    if leastIndexCount>1:
        lastIndex=random.choice(indexCount)

    return toReturnList[lastIndex][1:len(toReturnList)+1]


###############################################################################
###############################################################################




def stopping_condInfoGain(sourceList):
    length=len(sourceList[0])

    noOfClassVariable=0
    #if data contains a lot of data but very less number of class variables
    for check in sourceList:
        if check[len(check)-1] in classVariable:
            noOfClassVariable+=1
    if noOfClassVariable<threshholdClassStop:
        str="not", classVariable[0]
        return [True,str]

    checkingClassvar=0
    for inner in sourceList:
        if inner[length-1] not in classVariable:
            checkingClassvar+=1
        else: break

    if checkingClassvar==len(sourceList):
        str="not", classVariable[0]
        return [True,str]


    if len(sourceList)<threshholdStop:
        temp={}
        for value in sourceList:
            classType=value[length-1]
            if temp.has_key(classType):
                temp[classType]=temp.get(classType)+1
            else:
                temp.update({classType:int(1)})
        #max class variable in left entries
        maxClassLeft=-9999
        key=""
        for data in temp:
            count=temp.get(data)
            if maxClassLeft<count:
                maxClassLeft=count
                key=data

        return [True,key]

    classVar=[]
    once=0
    tempList=[]
    classVarCount={}

    for valuesList in sourceList:
        temp=valuesList[length-1]
        if once==0:
            classVar.append(temp)
            once=1
            continue
        if temp not in classVar:
            # if multiple class variable present then return false as program should not stop here
            break
        once+=1

    #if all belongs to same class then stop
    if once == len(sourceList):
        #classVar[0] contains that node should be clasified as this class variable
        return [True,0]

    # if sourcelist contains simillar entries and just class variable are different then it should stop
    for valuesList in sourceList:
        # creating a sub list leaving class variable to check if left data is same
        sublist=valuesList[0:length-1]
        classType=valuesList[length-1]
        if classVarCount.has_key(classType):
            classVarCount[classType]=classVarCount.get(classType)+1
        else:
            classVarCount.update({classType:int(1)})
        if sublist not in tempList:
            tempList.append(sublist)
            if(len(tempList)>1):
                return [False,0]

    #max class variable in left entries
    maxClassLeft=-9999
    key=""
    for data in classVarCount:
        count=classVarCount.get(data)
        if maxClassLeft<count:
            maxClassLeft=count
            key=data
    # if sourcelist contains simillar entries and just class variable are different then it should stop
    #key is the maximum left class variable
    return [True,key]





def calculateEntropyNode(countList):
    # countList contains mainCOunt,othersCount for the number of split
    #segregating main and other. And then finding entropy for all created nodes
    nodeEntropy=[]
    allTotal=0
    totalIndividualNode=[]

    for val in range(0,len(countList),2):
        Main=countList[val]
        Others=countList[val+1]
        allTotal+=Main+Others
        total=Main+Others
        if total!=0:
            mainProbability=float(Main)/total
            othersProbability=float(Others)/total
            probList=[mainProbability,othersProbability]
            totalIndividualNode.append(total)
            result=0
            for iterate in range(0,2):
                if probList[iterate]!=0:
                    result+=(-(probList[iterate]*math.log(probList[iterate],2)))
            nodeEntropy.append(result)
        else:
            totalIndividualNode.append(0)
            nodeEntropy.append(0)

    totalEntropy=0
    #indiEntropy=[]

    if allTotal!=0:
        for node in range(0,len(nodeEntropy)):
            #indiEntropy.append(-(float(totalIndividualNode[node])/allTotal)*nodeEntropy[node])
            totalEntropy+=(float(totalIndividualNode[node])/allTotal)*nodeEntropy[node]
        nodeEntropy.append(totalEntropy)
    else:
        nodeEntropy.append("All total to calculate total entropy is zero")
    return nodeEntropy


def findBestSplitInfoGain(Data):
    count=0
    # make correction
    length=len(Data[0])-1
    calculateMinMax(Data)

    toReturnList=[]
    for features in range(0,length):
        if features in doneAttribute:
            continue
        minValue=minList[features]          # min and max (next line) for this feature
        maxValue=maxList[features]
        intervalLength=(maxValue-minValue)/interval
        splitAt=minValue
        tempListForGINI=[]
        finalLeftList=[]
        finalRightList=[]
        EntropyList=[]
        childEntropy=[]
        for i in range(0,interval):

            splitAt+=intervalLength         # increasing intervals value
            for classValue in classVariable:

                leftList=[]
                rightList=[]
                leftCountMain=0
                leftCountOthers=0
                rightCountMain=0
                rightCountOthers=0
                for att in Data:
                    if att[features]<=splitAt:          #if value is smaller than split value
                        leftList.append(att)
                        if att[length]==classValue:      # if class variable is main or others for binary split
                            leftCountMain+=1
                        else:
                            leftCountOthers+=1
                    else:
                        rightList.append(att)
                        if att[length]==classValue:      # if class variable is main or others for binary split
                            rightCountMain+=1
                        else:
                            rightCountOthers+=1
                finalLeftList.append(leftList)
                finalRightList.append(rightList)

                # create a list of gini for different interval values
                tempEntropy=calculateEntropyNode([leftCountMain,leftCountOthers,rightCountMain,rightCountOthers])
                tempListForGINI.append(tempEntropy[len(tempEntropy)-1])
                childEntropy.append([tempEntropy[0],tempEntropy[1]])

        EntropyList.append(tempListForGINI)


        minGINI=99999
        entropyOfWhichAttribute=-100
        numberInterval=-99
        for entropy in EntropyList:
            for inner in entropy:
                if minGINI>inner:
                    minGINI=inner
                    entropyOfWhichAttribute=features
                    index=entropy.index(inner)
                    indexOfChildEntropy=EntropyList.index(entropy)
                    numberInterval=(index/len(classVariable))+(index%len(classVariable))      #to find internal index
        resultValueforSplit=minList[entropyOfWhichAttribute]+(intervalLength*(index+1))
        listNumber=numberInterval*len(classVariable)+entropyOfWhichAttribute
        #toReturnList.append([minGINI,entropyOfWhichAttribute,resultValueforSplit,finalLeftList[listNumber],
         #                    finalRightList[listNumber],childEntropy[indexOfChildEntropy][0],childEntropy[indexOfChildEntropy][1]])
        toReturnList.append([minGINI,entropyOfWhichAttribute,resultValueforSplit,finalLeftList[index],
                             finalRightList[index],childEntropy[indexOfChildEntropy][0],childEntropy[indexOfChildEntropy][1]])

        """
        minGINI=99999
        entropyOfWhichAttribute=[]
        numberInterval=-99
        for entropy in EntropyList:
            for inner in entropy:
                if minGINI>inner:
                    minGINI=inner


        minGINIList=[]
        index=[]
        indexOfChildEntropy=[]
        numberInterval=[]
        indexPlus=0
        for entropy in EntropyList:
            for inner in entropy:
                if minGINI==inner:
                    minGINIList.append(inner)
                    entropyOfWhichAttribute.append(features)
                    index.append(entropy.index(inner,indexPlus))
                    indexOfChildEntropy.append(EntropyList.index(entropy))
                    indexPlus=index[len(index)-1]+1
                    numberInterval.append((index[len(index)-1]/len(classVariable))+(index[len(index)-1]%len(classVariable)))      #to find internal index
        differnce=9999
        finalIndex=-99
        for findIndex in index:
            tempDiffernce=abs(len(finalLeftList[findIndex])-len(finalRightList[findIndex]))
            if differnce>tempDiffernce:
                differnce=tempDiffernce
                finalIndex=findIndex
        find=-999
        counter=0
        for chk in index:
            if chk==finalIndex:
                find=counter
            counter+=1

        resultValueforSplit=minList[entropyOfWhichAttribute[0]]+(intervalLength*(index[finalIndex]+1))


        toReturnList.append([minGINI,entropyOfWhichAttribute[0],resultValueforSplit,finalLeftList[finalIndex],
                             finalRightList[finalIndex],childEntropy[finalIndex][0],childEntropy[finalIndex][1]])
        """

    lastIndex=9999
    lastGINI=99
    for last in toReturnList:
        if last[0]<lastGINI:
            lastGINI=last[0]
            lastIndex=toReturnList.index(last)


    indexCount=[]
    for check in toReturnList:
        if check[0]==lastGINI:
            indexCount.append(toReturnList.index(check))
    leastIndexCount=len(indexCount)

    temp=[]

    if leastIndexCount>1:
        for weight in indexCount:
            if weight not in attributeAlreadyDone:
                temp.append(weight)
        for wh in temp:
            indexCount.append(wh)
        lastIndex=random.choice(indexCount)

    return toReturnList[lastIndex]
    #attributeAlreadyDone.append(lastIndex)
"""
    if lastIndex!=9999:
        doneAttribute.append(toReturnList[lastIndex][1])
        #return toReturnList[lastIndex][1:len(toReturnList)+1]

    else:
        return None
"""


def calculateParentEntropy(sourceList):
    noOfClassVariables=[]
    for i in range(0,len(classVariable)):
        noOfClassVariables.append(i)
    choice=random.choice(noOfClassVariables)
    mainCount=0
    othersCount=0
    for tuple in sourceList:
        if classVariable[choice]==tuple[len(tuple)-1]:
            mainCount+=1
        else:
            othersCount+=1
    totalCount=mainCount+othersCount
    if totalCount!=0:
        mainProbability=float(mainCount)/totalCount
        othersProbability=float(othersCount)/totalCount
    else:
        return 0
    result=0
    probList=[mainProbability,othersProbability]
    for iterate in range(0,2):
        if probList[iterate]!=0:
            result+=(-(probList[iterate]*math.log(probList[iterate],2)))
    return result



##############################################################################

def TreeGrowth(sourceList):
    resultList=stopping_cond(sourceList)
    if  resultList[0]:
        if resultList[1]==0:
            leaf=Node(sourceList[0][len(sourceList[0])-1],"null","null","null","null","null","null")
        else:
            leaf=Node(resultList[1],"null","null","null","null","null","null")
        return leaf
    else:
        returnedValue=findBestSplit(sourceList)
        featureNumber=returnedValue[0]
        root=Node("null",attributeList[featureNumber],returnedValue[1],"null","null","<=","null")
        if returnedValue[2]:
            root.leftChild=TreeGrowth(returnedValue[2])
        if returnedValue[3]:
            root.rightChild=TreeGrowth(returnedValue[3])
    return root



def calculateName(sourceList):
    length=len(sourceList[0])
    temp={}
    for value in sourceList:
        classType=value[length-1]
        if temp.has_key(classType):
            temp[classType]=temp.get(classType)+1
        else:
            temp.update({classType:int(1)})
    #max class variable in left entries
    maxClassLeft=-9999
    key=""
    for data in temp:
        count=temp.get(data)
        if maxClassLeft<count:
            maxClassLeft=count
            key=data

    return key



def TreeGrowthInfoGain(sourceList,node,parentEntropy):
    resultList=stopping_condInfoGain(sourceList)
    if  resultList[0]:
        if resultList[1]==0:
            leaf=Node(sourceList[0][len(sourceList[0])-1],"null","null","null","null","null","null")
        else:
            leaf=Node(resultList[1],"null","null","null","null","null","null")
        return leaf
    else:
        returnedValue=findBestSplitInfoGain(sourceList)
        if returnedValue==None:
            node.name=calculateName(sourceList)
            return None
        featureNumber=returnedValue[1]
        if node==None:
            node=Node("null",attributeList[featureNumber],returnedValue[2],"null","null","null",calculateParentEntropy(sourceList))
            if float(node.entropy)-float(returnedValue[0])>=0:
                if returnedValue[3]:
                    node.leftChild=TreeGrowthInfoGain(returnedValue[3],node,returnedValue[5])
                    if node.leftChild==None:
                        node.name=calculateName(sourceList)
                if returnedValue[4]:
                    node.rightChild=TreeGrowthInfoGain(returnedValue[4],node,returnedValue[6])
                    if node.rightChild==None:
                        node.name=calculateName(sourceList)
                if node.leftChild==None and node.rightChild==None:
                    node.splitAttribute=None
                    node.splitValue=None
            return node
        elif float(parentEntropy)-float(returnedValue[0])>=0:
            newNode=Node("null",attributeList[featureNumber],returnedValue[2],"null","null","<=",parentEntropy)
            if returnedValue[3]:
                newNode.leftChild=TreeGrowthInfoGain(returnedValue[3],newNode,returnedValue[5])
                if newNode.leftChild==None:
                    newNode.name=calculateName(sourceList)

            if returnedValue[4]:
                newNode.rightChild=TreeGrowthInfoGain(returnedValue[4],newNode,returnedValue[6])
                if newNode.rightChild==None:
                        node.name=calculateName(sourceList)
            if newNode.leftChild==None and newNode.rightChild==None:
                    newNode.splitAttribute=None
                    newNode.splitValue=None

            return newNode
        else:
            return None
    #return root



def traverseTree(Tree,assignClass):
    classAssigned=True
    name=Tree
    while classAssigned:
        if name==None:
            print "stop"
        if  name.splitAttribute == 'null' or name.splitValue==None:
            if name.name not in classVariable:
                string=str("not "+classVariable[0])
                return string
            return name.name
        index=attributeList.index(name.splitAttribute)
        if float(assignClass[index]) <= float(name.splitValue):
            if name.leftChild!=None and name.leftChild!='null' and   name.leftChild!='None'  :
                name=name.leftChild
            else:
                if name.name not in classVariable:
                    string=str("not "+classVariable[0])
                    return string
                return name.name
        else:
            if name.rightChild!=None and name.rightChild!='null' and name.rightChild!='None':
                name=name.rightChild
            else:
                if name.name not in classVariable:
                    string=str("not "+classVariable[0])
                    return string
                return name.name





def nFoldValidation(sourceList,value):
    length=len(sourceList)
    sizeOfOneSplit=length/nFold
    doneList=[]
    s=range(0,length)
    accuracyValue=0
    accurateList=[]
    for i in range(0,nFold):
        trainList=list(sourceList)
        testList=[]
        for j in range(0,sizeOfOneSplit):
            var=random.choice(list(s))
            testList.append(sourceList[var])
            s.remove(var)
        for k in range(0,sizeOfOneSplit):
            trainList.remove(testList[k])
        if value==1:
            Tree=TreeGrowth(trainList)
        else:
            Tree=TreeGrowthInfoGain(trainList,None,None)
        accurate=0
        node=calculateBestTree(Tree,trainList,sizeOfOneSplit)

        for data in testList:
            result= traverseTree(node,data)
            classVar=data[len(data)-1]
            if (result==classVar and classVariable[0]==result) or (classVariable[0]!=result and classVariable[0]!=classVar):
                accurate+=1

        accurateList.append(accurate)
        accuracyValue+=float(accurate)/sizeOfOneSplit
    return accuracyValue/nFold




def calculateBestTree(Tree,trainList,sizeOfOneSplit):
    returnedValue=0
    returnedVal2=0
    node=Tree
    bfsList=[]
    limit=5
    pessimistErrorVar=[]
    once=1
    prevNode=0
    for inner in range(0,limit):
        #value=returnTree(Tree,inner)
        value=returnTreeAgain(Tree,inner,trainList)

        node=value[0]
        error=cal(node,trainList,sizeOfOneSplit)
        if once==1:
            pessimistErrorVar.append(error)
            prevNode=node
            once=2
            continue
        if pessimistErrorVar[len(pessimistErrorVar)-1]-error<0 or value[1]==1:
            return prevNode
            break
        pessimistErrorVar.append(error)
        prevNode=node
    return node


def returnTree(Tree,limit):
    node=Node(Tree.name,Tree.splitAttribute,Tree.splitValue,"null","null",Tree.symbol,Tree.entropy)
    value1=0
    value2=0
    if limit==0:
        return [node,0]
    if Tree.leftChild!='null' and Tree.leftChild!=None:
        retunrned=returnTree(Tree.leftChild,limit-1)
        node.leftChild=retunrned[0]
        value1=retunrned[1]
    if Tree.rightChild!='null' and Tree.rightChild!=None:
        retunrned=returnTree(Tree.rightChild,limit-1)

        node.rightChild=retunrned[0]
        value2=retunrned[1]
    if (Tree.leftChild=='null' or  Tree.leftChild!=None) and (Tree.rightChild=='null' or Tree.rightChild!=None):
        return [node,1]
    if value1==1 and value2==1:
        return [node,1]
    return [node,0]

def cal(node,trainList,sizeOfOneSplit):
    pessimistErrorVar=0
    accurate=0
    nodesResult=calculateNodes(node)
    trainCount=len(trainList)

    for data in trainList:
            result= traverseTree(node,data)
            classVar=data[len(data)-1]
            if (result==classVar and classVariable[0]==result) or (classVariable[0]!=result and classVariable[0]!=classVar):
                accurate+=1
    pessimistErrorVar=pessimistError(nodesResult[1],trainCount-accurate)
    return pessimistErrorVar

def returnTreeAgain(Tree,limit,trainList):
    node=Node(Tree.name,Tree.splitAttribute,Tree.splitValue,"null","null",Tree.symbol,Tree.entropy)
    node.name=calculateName(trainList)
    value1=0
    value2=0
    if limit==0:
        return [node,0]
    if Tree.leftChild!='null' and Tree.leftChild!=None:
        attributeValue=node.splitValue
        attributeToSplit=node.splitAttribute
        indexOfAttribute=attributeList.index(attributeToSplit)
        leftList=[]
        for data in trainList:
            if data[indexOfAttribute]<=attributeValue:
                leftList.append(data)
        if leftList:
            retunrned=returnTreeAgain(Tree.leftChild,limit-1,leftList)
            node.leftChild=retunrned[0]
            value1=retunrned[1]
    if Tree.rightChild!='null' and Tree.rightChild!=None:
        attributeValue=node.splitValue
        attributeToSplit=node.splitAttribute
        indexOfAttribute=attributeList.index(attributeToSplit)
        rightList=[]
        for data in trainList:
            if data[indexOfAttribute]>attributeValue:
                rightList.append(data)
        if rightList:
            retunrned=returnTreeAgain(Tree.rightChild,limit-1,rightList)
            node.rightChild=retunrned[0]
            value2=retunrned[1]
    if (node.leftChild=='null' or  node.leftChild==None) and (node.rightChild=='null' or node.rightChild==None):
        # 1 means that we have already traveres whole tree, no need to come here again
        return [node,1]

    if value1==1 and value2==1:
        return [node,1]
    return [node,0]

def returnBFS(Tree,limit,trainList):
    Queue=[]
    value=limit
    node=Node(Tree.name,Tree.splitAttribute,Tree.splitValue,"null","null",Tree.symbol,Tree.entropy)
    temp=node
    Queue.append(Tree)
    while Queue:
        node=Queue[0]
        if Queue[0].leftChild:
            node.leftChild=Tree.leftChild
            node.name=calculateName(trainList)
            Queue.append(node.leftChild)
            value-=1
            if value==0:
                return node
        if Queue[0].rightChild:
            node.rightChild=Queue[0].leftChild
            Queue.append(node.rightChild)
            value-=1
            if value==0:
                return node
        Queue.pop(0)
    return temp

def pessimistError(leafNodes,inaccurate):
    return inaccurate+(0.5*leafNodes)

def calculateNodes(Tree):
    internalNodes=0
    leafNodes=0
    bfsList=[]
    bfsList.append(Tree)
    while bfsList :


        if bfsList[0].leftChild!='null' and bfsList[0].leftChild!=None:
            internalNodes+=1
            bfsList.append(bfsList[0].leftChild)
        if bfsList[0].rightChild != 'null' and bfsList[0].rightChild!=None:
            if not bfsList[0].leftChild:
                internalNodes+=1
            bfsList.append(bfsList[0].rightChild)

        if (bfsList[0].leftChild=='null' or bfsList[0].leftChild==None) and (bfsList[0].rightChild=='null' or bfsList[0].rightChild==None):
            leafNodes+=1
        bfsList.pop(0)
    return [internalNodes,leafNodes]







readFile(pathForBaseFile,dataList)

#readFile(pathForTestFile,testData)


#classVariableTest=['Iris-setosa', 'Iris-versicolor', 'Iris-virginica']
print "Presence of which class variable you want to check "
inputVar=1
for var in classVariable:
    print inputVar," ",var
    inputVar+=1
number = input('Enter your number: ')
#classVariable=[]
#classVariable=['Iris-virginica']
variable=classVariable[number-1]
classVariable=[]
classVariable.append(variable)
number = input('GINI or Information Gain \n 1. GINI \n 2. Information Gain')
print "Accuracy:" , nFoldValidation(dataList,number)

"""
Tree=TreeGrowthInfoGain(dataList,None,None)
for test in testData:
    print traverseTree(Tree,test)

Tree=TreeGrowth(dataList)
for test in testData:
    print traverseTree(Tree,test)
"""


print "Test"