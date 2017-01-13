import operator
import thread
import math




#pathExtraInfo="E:\Semester 2\Data Mining\Assignments\Assignment 1\ml-100k_old\ml-100k\u.user"
pathExtraInfo='/l/b565/ml-100k/u.user'
readExtraInfoDict={}
ageList=[]
genderList=[]
movieGenreDict={}
sourceMovieNotSeenList=[]
targetMovieNotSeenList=[]

pathForBaseFile='/l/b565/ml-10M100k/r1.train'
pathForTestFile='/l/b565/ml-10M100k/r1.test'



#pathForBaseFile='E:\Semester 2\Data Mining\Assignments\Assignment 1\ml-100k\ml-100k\u1.base'
#pathForTestFile='E:\Semester 2\Data Mining\Assignments\Assignment 1\ml-100k\ml-100k\u1.test'
#pathForBaseFile='/l/b565/ml-100k/u1.base'
#pathForTestFile='/l/b565/ml-100k/u1.test'
#pathForBaseFile='E:\Semester 2\Data Mining\Assignments\Assignment 1\ml-100k_old\ml-100k\u1Base.txt'
#pathForTestFile='E:\Semester 2\Data Mining\Assignments\Assignment 1\ml-100k_old\ml-100k\u1Test.txt'

TestRatingsDict={}
BaseRatingsDict={}
allMovieIdList=[]
movieNotSeenbyAnybody=[]
movieUserDict={}


def readFile(path,source):
    f = open(path, 'r')
    for data in f:
        currentRatingDict={}
        row=data.split('\t')
        newUserId=row[0]
        currentRatingDict.update({row[1]:row[2]})
        if source.has_key(newUserId):
            tempDict=source[newUserId]
            tempDict.update(currentRatingDict)
            source[newUserId]=tempDict
        else:
            source.update({newUserId:currentRatingDict})
def readExtraInfo(path,source):
    f = open(path, 'r')
    for data in f:
        currentRatingDict=[]
        row=data.split('|')
        newUserId=row[0]
        currentRatingDict.append(row[1])
        if row[1]==99 or row[1]==1:
            print row[0]
        currentRatingDict.append(row[2])
        currentRatingDict.append(row[3])
        ageList.append(float(row[1]))
        if row[0]=="29":
            print "check"
        if row[2]!= 'M' and row[2]!='F':
            print "gender check"
        if source.has_key(newUserId):
            tempList=source[newUserId]
            tempList.update(currentRatingDict)
            source[newUserId]=tempList
        else:
            source.update({newUserId:currentRatingDict})


def allMovieId():
    f = open('/l/b565/ml-100k/u.item', 'r')
    #f = open('E:\Semester 2\Data Mining\Assignments\Assignment 1\ml-100k\ml-100k\u.item', 'r')
    allMovieIdList=[]

    for data in f:
        tempList=[]
        row=data.split('|')
        allMovieIdList.append(row[0])
        for i in range(5,24):
            if row[i] !="0" and  row[i] !="0\n":
                tempList.append(i-5)
        movieGenreDict.update({row[0]:tempList})
    return allMovieIdList
def moviesNotSeen(userId,source):
    notSeen=[]
    reviews={}
    reviews=source.get(str(userId))
    for movieId in allMovieIdList:
        if movieId not in reviews:
            notSeen.append(movieId)
    return notSeen


def findAverage(baseDict):
    sumMR={}
    countMovie={}
    averageMR={}
    for key in baseDict:
        innerDict=baseDict[key]
        for innerKey in baseDict.get(key):
            if sumMR.get(innerKey):
                sumMR.update({innerKey:int(sumMR.get(innerKey))+int(innerDict[innerKey])})
            else:
                sumMR.update({innerKey:int(innerDict[innerKey])})
            if countMovie.get(innerKey):
                countMovie.update({innerKey:int(countMovie[innerKey])+1})
            else:
                countMovie.update({innerKey:1})

    for key,value in sumMR.iteritems():
        averageMR.update({key:round(float(value)/float(countMovie.get(key)),2)})
    return averageMR


def predictUsingAverage(baseDict):
    predictedDict={}
    averageDict=findAverage(baseDict)
    for user in baseDict:
        notSeenMoviesListOfUser=moviesNotSeen(user,baseDict)
        movieRating={}
        for movie in notSeenMoviesListOfUser:
            averageRating=averageDict.get(movie)
            if not averageRating:
                #movieRating.update({movie:-99})
                continue
            movieRating.update({movie:averageRating})
        predictedDict.update({user:movieRating})
        notSeenMoviesListOfUser={}
    return predictedDict

def listOfUsersWhoHaveSeenThisMovie(movieId,sourceDict):
    seenUserList=[]
    for key in sourceDict:
        innerDict=sourceDict[key]
        if innerDict.get(str(movieId)):
            seenUserList.append(key)
            innerDict={}
    return seenUserList

def listOfMoviesSeen(userId,sourceDict):
    moviesList=[]
    innerDict=sourceDict.get(str(userId))
    for innerKey in innerDict:
            moviesList.append(innerKey)
    return moviesList

def noAndIdOfSimilarWatchedMovies(sourceUser,targetUser,sourceDict):
    noOfMoviesSeen=[]
    noOfMoviesSeen.append(0)
    sourceUserSeenMoviesList=listOfMoviesSeen(sourceUser,sourceDict)
    targetUserSeenMoviesList=listOfMoviesSeen(targetUser,sourceDict)
    for movie in sourceUserSeenMoviesList:
        if movie in targetUserSeenMoviesList:
            noOfMoviesSeen[0]+=1
            noOfMoviesSeen.append(movie)
        else:
            targetMovieNotSeenList.append(movie)
    for movie in targetUserSeenMoviesList:
        if movie not in sourceUserSeenMoviesList:
            sourceMovieNotSeenList.append(movie)
    return noOfMoviesSeen

def square(list):
    sq=0
    for i in list:
        sq=i*i+sq
    return round(sq,2)


def euclideanDistance(sourceUser,targetUser,sourceDict):
    result=[]
    sourceUserDict=sourceDict.get(str(sourceUser))
    targetUserDict=sourceDict.get(str(targetUser))
    alreadyCovered=[]

    for mov in sourceUserDict:
        alreadyCovered.append(mov)
        if targetUserDict.get(mov):
            result.append(abs(int(sourceUserDict.get(mov))-int(targetUserDict.get(mov))))
        else:
            result.append(abs(int(sourceUserDict.get(mov))-int(0)))
    for mov in targetUserDict:
        if mov in alreadyCovered:
            continue
        if sourceUserDict.get(mov):
            result.append(abs(int(sourceUserDict.get(mov))-int(targetUserDict.get(mov))))
        else:
            result.append(abs(int(targetUserDict.get(mov))-int(0)))
    return round(math.sqrt(float(square(result))),4)


def euclideanDistancewithSimilarMoviesList(sourceUser,targetUser,similarMovieList,sourceDict):
    result=[]
    sourceUserDict=sourceDict.get(str(sourceUser))
    targetUserDict=sourceDict.get(str(targetUser))

    for key in similarMovieList:
        if targetUserDict.get(key):
            result.append(abs(int(sourceUserDict.get(key))-int(targetUserDict.get(key))))
    return round(math.sqrt(float(square(result))),4)

def manhattanDistancewithSimilarMoviesList(sourceUser,targetUser,similarMovieList,sourceDict):
    result=[]
    sourceUserDict=sourceDict.get(str(sourceUser))
    targetUserDict=sourceDict.get(str(targetUser))

    for key in similarMovieList:
        if targetUserDict.get(key):
            result.append(abs(int(sourceUserDict.get(key))-int(targetUserDict.get(key))))
    return sum(result)


def LmaxDistancewithSimilarMoviesList(sourceUser,targetUser,similarMovieList,sourceDict):
    result=[]
    sourceUserDict=sourceDict.get(str(sourceUser))
    targetUserDict=sourceDict.get(str(targetUser))

    for key in similarMovieList:
        if targetUserDict.get(key):
            result.append(abs(int(sourceUserDict.get(key))-int(targetUserDict.get(key))))
    return max(result)




def findingSimilarityWithMovie(sourceUser,movie,distanceType,sourceDict,extraInfo):
    sourceUser=str(sourceUser)
    moviesSeenList=listOfMoviesSeen(sourceUser,sourceDict)
    DistanceDict={}
    count=0
    noOfSimilarWatchMovieDict={}
    distanceType=int(distanceType)

    listOfUsersWhoSawMovie=movieUserDict.get(movie)
    if  listOfUsersWhoSawMovie== None:
        return None

    for targetUser in listOfUsersWhoSawMovie:
        if targetUser == sourceUser:
            continue
        noAndIdofSimilarMoviesList=noAndIdOfSimilarWatchedMovies(sourceUser,targetUser,sourceDict)
        noOfSimilarWatchMovieDict.update({targetUser:noAndIdofSimilarMoviesList[0]})
        if noAndIdofSimilarMoviesList[0]>12:
                noAndIdofSimilarMoviesList.pop(0)
                if distanceType==1:
                    distance=euclideanDistancewithSimilarMoviesList(sourceUser,targetUser,noAndIdofSimilarMoviesList,sourceDict)
                    #distance=euclideanDistancewithSimilarMoviesListPartB(sourceUser,targetUser,noAndIdofSimilarMoviesList,sourceDict,extraInfo)

                    #distance=euclideanDistance(sourceUser,targetUser,sourceDict)
                elif distanceType==2:
                    distance=manhattanDistancewithSimilarMoviesList(sourceUser,targetUser,noAndIdofSimilarMoviesList,sourceDict)
                else:
                    distance=LmaxDistancewithSimilarMoviesList(sourceUser,targetUser,noAndIdofSimilarMoviesList,sourceDict)
                DistanceDict.update({targetUser:distance})
    """
    sorted_x = sorted(DistanceDict.items(), key=operator.itemgetter(1))
    leastFive=[]
    if len(sorted_x)<3:
        return "Empty"
    for i in range(0, 5):
        if (i==3 and len(sorted_x)==3) or (i==4 and len(sorted_x)==4):
            return leastFive
        leastFive.append(sorted_x[i][0])
    return lestFiveAgain
    """

    if len(DistanceDict)<20:
        return "Empty"

    lestFiveAgain=[]
    for i in range(0,20):
        minDist=9999
        minUser=0
        for dist in DistanceDict:
            d=DistanceDict.get(dist)
            if d==0:
                continue
            if(d<minDist):
                minDist=d
                minUser=dist
        DistanceDict[minUser]=9999
        if(noOfSimilarWatchMovieDict.get(dist)>10):
            lestFiveAgain.append(minUser)
    if len(lestFiveAgain)<20:
        return "Empty"
    return lestFiveAgain



def makePrediction(sourceDict):
    predictions={}
    allUserPredictions={}
    ratingSum=0
    count=0
    distanceType = input('1 for Euclidean Distance \n2 for Manhattan Distance\n3 for L Max (Supremum)\nEnter distance Type: ')
    usercount=0

    for targetUser in sourceDict:
        moviesNotSeenList=moviesNotSeen(targetUser,sourceDict)
        usercount+=1

        for movie in moviesNotSeenList:
            count+=1
            if movie not in movieNotSeenbyAnybody:
                similarUsers=findingSimilarityWithMovie(targetUser,movie,distanceType,sourceDict)
                if similarUsers=="Empty" or  similarUsers == None:
                    listOfUsersWhoSawMovie=movieUserDict.get(movie)
                    if listOfUsersWhoSawMovie==None:
                        continue
                    for innerTargetUser in listOfUsersWhoSawMovie:
                        ratingSum=int(sourceDict.get(innerTargetUser).get(movie))+int(ratingSum)
                    if len(listOfUsersWhoSawMovie)==0:
                        #predictions.update({movie:-99 })
                        movieNotSeenbyAnybody.append(movie)
                        continue
                    averageRating=round(float(float(ratingSum)/len(listOfUsersWhoSawMovie)),2)
                    predictions.update({movie:averageRating })
                else:
                    for similarUser in similarUsers:
                        if similarUser==0:
                            continue
                        ratingSum=int(sourceDict.get(similarUser).get(movie))+ratingSum
                    averageRating=round(float(float(ratingSum)/len(similarUsers)),2)
                    predictions.update({movie:averageRating })
                ratingSum=0
                averageRating=0
            #else:
                #predictions.update({movie:-99 })
            if allUserPredictions.has_key(targetUser):
                    tempDict=allUserPredictions[targetUser]
                    tempDict.update(predictions)
                    allUserPredictions.update({targetUser:tempDict})
            else:
                allUserPredictions.update({targetUser:predictions})

            print "*",usercount," ",count,
            predictions={}
    return allUserPredictions


def calculateMAD(baseDict,testDict):
    sumMAD=0
    count=0;
    for user in testDict:
        baseInnerDict=baseDict.get(user)
        testInnerDict=testDict.get(user)
        for movie in testInnerDict:
            temp=baseInnerDict.get(movie)
            if temp==-99:
                print "garbage value"
            if temp and temp !=99:
                sumMAD= round(abs(float(temp)-float(testInnerDict.get(movie)))+float(sumMAD),2)
                count+=1
    return sumMAD/int(count)


def populateMovieUser(path):
    f = open(path, 'r')
    movieUser={}
    for data in f:
        row=data.split('\t')
        UserId=[]
        UserId.append(row[0])
        movie=row[1]
        #movieUser.update(row[1]:row[0])
        if movieUser.has_key(movie):
            tempMovieList=[]
            tempMovieList=movieUser[movie]
            tempMovieList.append(row[0])
            movieUser[row[1]]=tempMovieList
        else:
            movieUser.update({movie:UserId})
    return movieUser


def noOfMoviesSeenUser(userID,sourceDict):
    for key in sourceDict:
        innerDict=sourceDict[key]
        return len(innerDict)

def findTestEntries(sourceDict):
    prepareDict={}
    for key in sourceDict:
        testMoviesList=[]
        innerDict=sourceDict[key]
        for innerKey in sourceDict.get(key):
            testMoviesList.append(innerKey)
        prepareDict.update({key:testMoviesList})
    return prepareDict

def makePredictionSecond(sourceDict,preparedTestDict,extraInfo):
    predictions={}
    allUserPredictions={}
    ratingSum=0
    count=0
    distanceType = input('1 for Euclidean Distance \n2 for Manhattan Distance\n3 for L Max (Supremum)\nEnter distance Type: ')
    usercount=0

    for targetUser in preparedTestDict:

        usercount+=1
	print usercount
        innerDict=sourceDict[targetUser]
        #for innerKey in sourceDict.get(targetUser):


        for movie in preparedTestDict.get(targetUser):
            count+=1
            if movie not in movieNotSeenbyAnybody:
                similarUsers=findingSimilarityWithMovie(targetUser,movie,distanceType,sourceDict,extraInfo)
                if similarUsers=="Empty" or  similarUsers == None:
                    listOfUsersWhoSawMovie=movieUserDict.get(movie)
                    if listOfUsersWhoSawMovie==None:
                        continue
                    for innerTargetUser in listOfUsersWhoSawMovie:
                        ratingSum=int(sourceDict.get(innerTargetUser).get(movie))+int(ratingSum)
                    if len(listOfUsersWhoSawMovie)==0:
                        #predictions.update({movie:-99 })
                        movieNotSeenbyAnybody.append(movie)
                        continue
                    averageRating=round(float(float(ratingSum)/len(listOfUsersWhoSawMovie)),2)
                    predictions.update({movie:averageRating })
                else:
                    sUserCount=0
                    for similarUser in similarUsers:
                        if similarUser==0:
                            continue
                        sUserCount+=1
                        ratingSum=int(sourceDict.get(similarUser).get(movie))+ratingSum
                    averageRating=round(float(float(ratingSum)/sUserCount),2)
                    predictions.update({movie:averageRating })
                ratingSum=0
                averageRating=0
            #else:
                #predictions.update({movie:-99 })
            if allUserPredictions.has_key(targetUser):
                    tempDict=allUserPredictions[targetUser]
                    tempDict.update(predictions)
                    allUserPredictions.update({targetUser:tempDict})
            else:
                allUserPredictions.update({targetUser:predictions})

            predictions={}
    return allUserPredictions


def euclideanDistancewithSimilarMoviesListPartB(sourceUser,targetUser,similarMovieList,sourceDict,InfoDict):
    result=[]
    extraResultInfo=[]
    sourceUserDict=sourceDict.get(str(sourceUser))
    targetUserDict=sourceDict.get(str(targetUser))
    age=abs(int(ageList[int(sourceUser)-1]- ageList[int(targetUser)-1]))
    gender=-99
    occupation=-99
    result.append(1.1*age)
    if(InfoDict.get(str(sourceUser))[1])== InfoDict.get(str(targetUser))[1]:
        gender=1
        result.append(0)
    else:
        result.append(round(1.1*3,2))
        gender=0
    if(InfoDict.get(str(sourceUser))[2]in InfoDict.get(str(targetUser))[2] and InfoDict.get(str(targetUser))[2]!='other'):
        occupation=1
        result.append(0)
    else:
        occupation=0
        result.append(round(1.1*3,2))
    sourceSeenGenreDict={}
    targetSeenGenreDict={}
    for movie in targetMovieNotSeenList:
        InnerListTarget=[]
        InnerListTarget=movieGenreDict.get(movie)
        for genre in InnerListTarget:
            if targetSeenGenreDict.get(genre):
                targetSeenGenreDict.update({genre:int(targetSeenGenreDict.get(genre))+1})
            else:
                targetSeenGenreDict.update({genre:1})

    for movie in sourceMovieNotSeenList:
        InnerListSource=[]
        InnerListSource=movieGenreDict.get(movie)
        for genre in InnerListSource:
            if sourceSeenGenreDict.get(genre):
                sourceSeenGenreDict.update({genre:int(sourceSeenGenreDict.get(genre))+1})
            else:
                sourceSeenGenreDict.update({genre:1})
    targetMovieNotSeenList[:] = []
    sourceMovieNotSeenList[:] = []


    targetTopGenre=[]
    sourceTopGenre=[]

    for i in range(0,5):
        maxGenre=0
        number=0
        for genre in targetSeenGenreDict:
            count=int(targetSeenGenreDict.get(genre))
            if count>maxGenre:
                maxGenre=count
                number=genre
        targetTopGenre.append(number)
        targetSeenGenreDict.update({number:-99})

    for i in range(0,5):
        maxGenre=0
        number=0
        for genre in sourceSeenGenreDict:
            count=int(sourceSeenGenreDict.get(genre))
            if count>maxGenre:
                maxGenre=count
                number=genre
        sourceTopGenre.append(number)
        sourceSeenGenreDict.update({number:-99})
    commonGenre=0
    for genreList in sourceTopGenre:
        if genreList in targetTopGenre:
            commonGenre+=1
    result.append(1.5*(int(5)-int(commonGenre)))

    for key in similarMovieList:
        if targetUserDict.get(key):

            result.append(abs(int(sourceUserDict.get(key))-int(targetUserDict.get(key))))
    return round(math.sqrt(float(square(result))),4)

##########################################################

def scaleDownAge(sourceList):
    minValue=float(min(sourceList))
    maxValue=float(max(sourceList))
    scaledMin=1
    scaledMax=float(5)
    print minValue
    print maxValue
    for i in range(0,len(sourceList)):
        value=int(sourceList[i])
        sourceList[i]= round((float((scaledMax-scaledMin)*(value-minValue))/float((maxValue-minValue)))+scaledMin,2)
        if sourceList[i]=="0":
            print "stop"






allMovieIdList=allMovieId()
movieUserDict=populateMovieUser(pathForBaseFile)
readFile(pathForTestFile,TestRatingsDict)
readFile(pathForBaseFile,BaseRatingsDict)
readExtraInfo(pathExtraInfo,readExtraInfoDict)
scaleDownAge(ageList)



prepareTestDict=findTestEntries(TestRatingsDict)


#makePredictionSecond(BaseRatingsDict,prepareTestDict)



#file = open('myfile', 'w+')
#predictUsingAverageList=predictUsingAverage(BaseRatingsDict)

#makePrediction(TestRatingsDict)


with open("LMaxU1.txt", "w+") as myfile:
    myfile.write(str(calculateMAD(makePredictionSecond(BaseRatingsDict,prepareTestDict,readExtraInfoDict),TestRatingsDict)))
myfile.close()


"""
with open("testq.txt", "w+") as myfile:
    myfile.write(str(calculateMAD(makePrediction(BaseRatingsDict),TestRatingsDict)))
myfile.close()


with open("testAverage.txt", "w+") as myfile:
    myfile.write(str(calculateMAD(predictUsingAverageList,TestRatingsDict)))
myfile.close()
"""

print "Test"
print "Test Again"