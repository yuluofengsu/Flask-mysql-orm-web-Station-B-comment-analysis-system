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

def getVideoLenData(time):
    xData = ['小于10分钟','10-50分钟','50-250分钟','250-800分钟','800-2000分钟','大于2000分钟']
    yData = [0 for x in range(len(xData))]
    for i in videList:
        if time == str(timestamp_to_datetime(int(i[-3])))[:7]:
            if i[1] <= 10:
                yData[0] += 1
            elif i[1] <= 50:
                yData[1] += 1
            elif i[1] <= 250:
                yData[2] += 1
            elif i[1] <= 800:
                yData[3] += 1
            elif i[1] <= 2000:
                yData[4] += 1
            elif i[1] > 2000:
                yData[5] += 1
    return xData,yData

def getSeeNumData(time):
    xData = ['小于500','500-5000','5000-5万','5万-50万','50万-500万','大于500万']
    yData = [0 for x in range(len(xData))]
    for i in videList:
        if time == str(timestamp_to_datetime(int(i[-3])))[:7]:
            if int(i[4]) <= 500:
                yData[0] += 1
            elif int(i[4]) <= 5000:
                yData[1] += 1
            elif int(i[4]) <= 50000:
                yData[2] += 1
            elif int(i[4]) <= 500000:
                yData[3] += 1
            elif int(i[4]) <= 5000000:
                yData[4] += 1
            elif int(i[4]) > 5000000:
                yData[5] += 1
    return xData,yData