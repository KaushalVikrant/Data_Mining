import random
import math
import json
dataPoints={}
dimensionDataPoints=[]
print ""
result={}
dimensions=100

for k in range(1,dimensions+1):
    print k
    for i in range(1,101):
        points=[]
        for dimensions in range(0,k):
            points.append(random.random())

        dataPoints.update({i:points})
    dimensionDataPoints.append(dataPoints)
    dataPoints={}



def square(list):
    sq=0
    for i in list:
        sq=i*i+sq
    return sq
def findEuclideanDist(firstAttList,secondAttList):
    distance=[]
    for i in range(0,len(firstAttList)):
        distance.append(abs(float(firstAttList[i])-float(secondAttList[i])))
    dist=square(distance)**0.5
    return dist


def findMaxMin(sourceList):
    distance=[]
    for point in sourceList:
        print point
        for secondPoint in sourceList:
            if point == secondPoint or secondPoint<point:
                continue
            distance.append(findEuclideanDist(sourceList.get(point),sourceList.get(secondPoint)))
            #print "chal rha hai",
            #distance.append(abs(float(sourceList.get(point))-float(sourceList.get(secondPoint))))
    distanceMax=max(distance)
    distanceMin=min(distance)
    distance=[]
    distance.append(distanceMax)
    distance.append(distanceMin)
    return  distance

#findMaxMin(dimensionDataPoints[0])


def result():
    saveMaxMinForAllDict={}
    result={}
    for dimen in range(0,dimensions):
        print "Dimensions done",dimen
        saveMaxMinForAllDict.update({dimen+1:findMaxMin(dimensionDataPoints[dimen])})
    f=open("test1000.txt", "a")
    for feature in saveMaxMinForAllDict:
        val=calculateRK(saveMaxMinForAllDict.get(feature))
        result.update({feature:val})
        f.write(str(str(feature)+" , "+str(val))+"\n")
    f.close()
    """
    with open("test.txt", "a") as myfileQuetion4for10000:
        json.dump(result,myfileQuetion4for10000)
    myfileQuetion4for10000.close()
    """

def calculateRK(sourceList):
    value=math.log10((sourceList[0]-sourceList[1])/sourceList[1])
    print value
    return value


result()

print " before this"


print "log10 ",math.log10(50)

print dataPoints
