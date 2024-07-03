from .query import querys

def getAllUpInfo():
    upInfoList = querys('select * from upinfo',[],'select')
    return upInfoList

def getAllVideoCommentsList():
    videoCommentsList = querys('select * from videocomments',[],'select')
    return videoCommentsList

def getAllVideoList():
    videoList = querys('select * from videoList',[],'select')
    return videoList

def getAllUser():
    userList = querys('select * from user',[],'select')
    return userList