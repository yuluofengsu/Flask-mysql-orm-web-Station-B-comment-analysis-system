from .getPublicData import *

def getPageData():
    upInfoList = getAllUpInfo()
    userList = getAllUser()
    videoCommentList = getAllVideoCommentsList()
    maxVideoLen = 0
    maxVideoLenName = ''
    for i in upInfoList:
        if maxVideoLen < int(i[-2]):
            maxVideoLen = int(i[-2])
            maxVideoLenName = i[2]
    userLen = len(userList)
    maxLevel = 0
    maxLevelName = ''
    for i in videoCommentList:
        if maxLevel < int(i[-1]):
            maxLevel = int(i[-1])
            maxLevelName = i[2]
    maxLikes = 0
    maxLikesName = ''
    for i in videoCommentList:
        if maxLikes < int(i[-3]):
            maxLikes = int(i[-3])
            maxLikesName = i[2]
    return maxVideoLenName,maxVideoLen,userLen,maxLevelName,maxLevel,maxLikesName,maxLikes

def getHomeBarData():
    upInfoList = getAllUpInfo()
    videoCommentList = getAllVideoCommentsList()
    videoList = getAllVideoList()
    xData = []
    yData = []
    for i in upInfoList:
        xData.append(i[1])
        yData.append(i[-2])
    y1DataDic = {}
    for i in videoCommentList:
        for j in videoList:
            if i[1] == j[2]:
                if y1DataDic.get(str(j[5]),-1) == -1:
                    y1DataDic[str(j[5])] = 1
                else:
                    y1DataDic[str(j[5])] += 1

    y1Data = [x[1] for x in list(y1DataDic.items())]


    xData = []
    for i in upInfoList:
        xData.append(i[2])
    return xData,yData,y1Data

def getHomeList():
    upInfoList = getAllUpInfo()
    videoCommentList = getAllVideoCommentsList()
    videoCommentList = list(sorted(videoCommentList, key=lambda x: x[-3], reverse=True))
    videoList = getAllVideoList()
    videoList = list(sorted(videoList, key=lambda x: int(x[4]), reverse=True))
    return upInfoList,videoCommentList[:5],videoList