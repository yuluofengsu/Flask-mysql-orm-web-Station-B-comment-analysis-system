from .getPublicData import *

upInfoList = getAllUpInfo()
def getFensiData():
    fensiDic = {}
    for i in upInfoList:
            fensiDic[i[2]] = i[3]
    resData = []
    for index,i in enumerate(list(fensiDic.keys())):
        resData.append([
            i,
            list(fensiDic.values())[index]
        ])
    return resData

def getLevenData():
    levelDic = {}
    for i in upInfoList:
        levelDic[i[2]] = i[-3]
    resData = []
    for key,value in levelDic.items():
        resData.append({
            'name':key,
            'value':value
        })
    return resData

def getVideLenData():
    videoLenDic = {}
    for i in upInfoList:
        videoLenDic[i[2]] = i[-2]

    return list(videoLenDic.keys()),list(videoLenDic.values())

