from .getPublicData import *
import datetime
import pytz
videoCommentList = getAllVideoCommentsList()
videList = getAllVideoList()
def timestamp_to_datetime(t):
    if t >= 86400:
        return datetime.datetime.fromtimestamp(t)
    else:
        return datetime.datetime.fromtimestamp(t, pytz.timezone('UTC')).replace(tzinfo=None)  # 世界标准时间

def getCommentLen(time):
    commentLenDic = {}
    for i in videoCommentList:
        if time == str(timestamp_to_datetime(int(i[-2])))[:7]:
            if commentLenDic.get(i[1],-1) == -1:
                commentLenDic[i[1]] = 1
            else:
                commentLenDic[i[1]] += 1
    totalNum = 0
    xData = list(commentLenDic.keys())
    yData = list(commentLenDic.values())
    for x in yData:
        totalNum += int(x)
    y1Data = [0 for x in range(len(xData))]
    for index,item in enumerate(yData):
        y1Data[index] = round(item/totalNum,3)
    return xData,yData,y1Data

def getUserCommentLikeTopData(time):
    videoCommentListes = []
    for i in videoCommentList:
        if time == str(timestamp_to_datetime(int(i[-2])))[:7]:
            videoCommentListes.append(i)
    videoCommentLists = list(sorted(videoCommentListes, key=lambda x: int(x[-3]), reverse=True))[:15]
    xData = []
    yData = []
    for i in videoCommentLists:
        xData.append(i[2])
        yData.append(i[-3])
    return xData,yData

def getUserSexData(time):
    sexDic = {}
    for i in videoCommentList:
        if time == str(timestamp_to_datetime(int(i[-2])))[:7]:
            if sexDic.get(i[-5],-1) == -1:
                sexDic[i[-5]] = 1
            else:
                sexDic[i[-5]] += 1
    resData = []
    for key,value in sexDic.items():
        resData.append({
            'name':key,
            'value':value
        })
    return resData

def getUserLevelData(time):
    sexDic = {}
    for i in videoCommentList:
        if time == str(timestamp_to_datetime(int(i[-2])))[:7]:
            if sexDic.get(i[-1], -1) == -1:
                sexDic[i[-1]] = 1
            else:
                sexDic[i[-1]] += 1
    resData = []
    for key,value in sexDic.items():
        resData.append({
            'name':key,
            'value':value
        })
    return resData
