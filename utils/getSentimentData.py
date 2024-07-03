from utils.getPublicData import getAllVideoCommentsList,getAllVideoList
import datetime
import pytz
from snownlp import SnowNLP
def timestamp_to_datetime(t):
    if t >= 86400:
        return datetime.datetime.fromtimestamp(t)
    else:
        return datetime.datetime.fromtimestamp(t, pytz.timezone('UTC')).replace(tzinfo=None)  # 世界标准时间

def getTimeList():
    commentList = getAllVideoCommentsList()
    timeList = []
    for comment in commentList:
        strimTime = int(comment[-2])
        project_start_day = timestamp_to_datetime(strimTime)
        timeList.append(str(project_start_day)[:7])
    return list(set(timeList))

def getTimesList():
    commentList = getAllVideoList()
    timeList = []
    for comment in commentList:
        strimTime = int(comment[-3])
        project_start_day = timestamp_to_datetime(strimTime)
        timeList.append(str(project_start_day)[:7])
    return list(set(timeList))

def getSentimentCommentData(time):
    commentList = getAllVideoCommentsList()
    xData = ['消极','中性','积极']
    yData = [0,0,0]
    for i in commentList:
        if time == str(timestamp_to_datetime(int(i[-2])))[:7]:
            if SnowNLP(i[4]).sentiments >= 0.6:
                yData[2] += 1
            elif SnowNLP(i[4]).sentiments > 0.4 and SnowNLP(i[4]).sentiments < 0.6:
                yData[1] += 1
            elif SnowNLP(i[4]).sentiments <= 0.4:
                yData[0] += 1
    return xData,yData