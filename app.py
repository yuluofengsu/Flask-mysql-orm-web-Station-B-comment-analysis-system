import json
from flask import Flask,request,render_template,session,redirect
import re
import random

from forms import userModelView, upinfoModelView, videolistModelView, videocommentsModelView
from models import user, upinfo, videolist, videocomments
from settings import db,Config
from utils.query import querys
from utils import getHomePageData
from utils import getPublicData
from utils import getUpInfoEcharts
from utils import getVideoCommentEcharts
from utils import getVideoListData
from utils import getSentimentData
from utils import themeModel
from snownlp import SnowNLP

from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin


app = Flask(__name__)
# 配置MySQL数据库
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/bstation'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'This is a app.secret_Key , You Know ?'
app.config.from_object(Config)
db.init_app(app)

# 初始化Flask Admin
admin = Admin(app, name='后台管理')

# 将模型添加到后台管理
admin.add_view(userModelView(user, db.session))
admin.add_view(upinfoModelView(upinfo, db.session))
admin.add_view(videolistModelView(videolist, db.session))
admin.add_view(videocommentsModelView(videocomments, db.session))



@app.route('/')
def every():
    return render_template('login.html')

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'POST':
        request.form = dict(request.form)

        def filter_fns(item):
            return request.form['email'] in item and request.form['password'] in item

        users = querys('select * from user', [], 'select')
        login_success = list(filter(filter_fns, users))
        if not len(login_success):
            return '账号或密码错误'

        session['email'] = request.form['email']
        session['userRole'] = login_success[0][-1]

        return redirect('/home', 301)

    else:
        return render_template('./login.html')

@app.route("/registry",methods=['GET','POST'])
def registry():
    if request.method == 'POST':
        request.form = dict(request.form)
        if request.form['password'] != request.form['passwordCheked']:
            return '两次密码不符'
        else:
            def filter_fn(item):
                return request.form['email'] in item

            users = querys('select * from user', [], 'select')
            filter_list = list(filter(filter_fn, users))
            if len(filter_list):
                return '该用户名已被注册'
            else:
                querys('insert into user(email,password) values(%s,%s)',
                       [request.form['email'], request.form['password']])

        session['email'] = request.form['email']
        return redirect('/login', 301)

    else:
        return render_template('./registry.html')


@app.route("/home")
def home():
    email = session['email']
    userRole = session['userRole']
    xData,yData,y1Data= getHomePageData.getHomeBarData()
    maxVideoLenName,maxVideoLen, userLen, maxLevelName, maxLevel,maxLikesName,maxLikes = getHomePageData.getPageData()
    upInfoList,videoListCommentTop,videoListTop = getHomePageData.getHomeList()
    upInfoAllList = getPublicData.getAllUpInfo()
    return render_template('home.html',
                           email=email,xData=xData,
                           userRole=userRole,
                           yData=yData,
                           y1Data=y1Data,
                           maxVideoLenName=maxVideoLenName,
                           maxVideoLen=maxVideoLen,
                           userLen=userLen,
                           maxLevelName=maxLevelName,
                           maxLevel=maxLevel,
                           maxLikesName=maxLikesName,
                           maxLikes=maxLikes,
                           upInfoList=upInfoList[:5],
                           videoListCommentTop=videoListCommentTop,
                           videoListTop=videoListTop[:5],
                           upInfoAllList=upInfoAllList
                           )

@app.route("/tableData")
def tableData():
    email = session['email']
    commentList = getPublicData.getAllVideoCommentsList()[:50]
    upInfoAllList = getPublicData.getAllUpInfo()
    userRole = session['userRole']

    return render_template('tableData.html',userRole=userRole,email=email,commentList=commentList,upInfoAllList=upInfoAllList)


@app.route("/editRoleManager/<int:userId>",methods=['GET','POST'])
def editRoleManager(userId):
    userInfo = querys('''
        select * from user where id = %s
    ''',[userId],'select')
    if userInfo[0][-1] == 'user':
        querys('''
                    UPDATE user
                    SET role=%s
                    where id = %s
                ''', ['admin', userId])
    else:
        querys('''
                            UPDATE user
                            SET role=%s
                            where id = %s
                        ''', ['user', userId])
    return redirect('/roleManager')

@app.route('/sentimentComment',methods=['GET','POST'])
def sentimentComment():
    email = session['email']
    userRole = session['userRole']
    upInfoAllList = getPublicData.getAllUpInfo()
    timeList = getSentimentData.getTimeList()
    defaultTime = request.args.get('time') if request.args.get('time') else timeList[0]
    x,y = getSentimentData.getSentimentCommentData(defaultTime)
    dataList,content = themeModel.main(defaultTime)
    sentimentRes = '积极' if SnowNLP(content).sentiments >= 0.5 else '消极'
    resData  =[]
    for index,i in enumerate(x):
        resData.append({
            'name':i,
            'value':y[index]
        })
    return render_template('sentimentComment.html',dataList=dataList,sentimentRes=sentimentRes,userRole=userRole,email=email,upInfoAllList=upInfoAllList,timeList=timeList,defaultTime=defaultTime,x=x,y=y,resData=resData)


@app.route("/addUserManager",methods=['GET','POST'])
def addUserManager():
    email = session['email']
    userRole = session['userRole']
    upInfoAllList = getPublicData.getAllUpInfo()
    if request.method == 'GET':
        return render_template('addUserManager.html',userRole=userRole, email=email, upInfoAllList=upInfoAllList)
    else:
        newEmail = request.form.get('email')
        newPassword = request.form.get('password')
        querys('''
            insert into user(email,password,role) values(%s,%s,%s)
        ''',[newEmail,newPassword,'admin'])
        return redirect('/userManager')

@app.route("/deleteUserManager/<int:userId>",methods=['GET','POST'])
def deleteUserManager(userId):
    querys('delete from user where id = %s',[userId])
    return redirect('/userManager')

@app.route("/editUserManager/<int:userId>",methods=['GET','POST'])
def editUserManager(userId):
    email = session['email']
    userRole = session['userRole']
    upInfoAllList = getPublicData.getAllUpInfo()
    if request.method == 'GET':
        userInfo = querys('''
            select * from user where id = %s
        ''',[userId],'select')
        return render_template('editUserManager.html',userRole=userRole, email=email, upInfoAllList=upInfoAllList,userInfo=userInfo[0],userId=userId)
    else:
        newEmail = request.form.get('email')
        newPassword = request.form.get('password')
        querys('''
            UPDATE user
            SET email=%s,
                password=%s
            where id = %s
        ''',[newEmail,newPassword,userId])
        return redirect('/userManager')

@app.route('/upDetail')
def upDetail():
    email = session['email']
    userRole = session['userRole']
    upInfoAllList = getPublicData.getAllUpInfo()
    videoAllList = getPublicData.getAllVideoList()
    videAllCommentVideo = getPublicData.getAllVideoCommentsList()
    upId = upInfoAllList[0][0]
    if request.args.get('upId'):upId = request.args.get('upId')
    upInfo = []
    for i in upInfoAllList:
        if int(i[0]) == int(upId):
            upInfo = i


    videoAllList = list(filter(lambda x:int(x[-4]) == int(upInfo[1]),videoAllList))
    videoId = videoAllList[0][0]
    if request.args.get('videoId'):videoId = request.args.get('videoId')
    videoInfo = []
    for i in videoAllList:
        if int(i[0]) == int(videoId):
            videoInfo = i

    videAllCommentVideo = list(filter(lambda x:int(x[1]) == int(videoInfo[2]),videAllCommentVideo))
    commentInfo = videAllCommentVideo
    return render_template('upDetail.html',
                           email=email,
                           upInfoAllList=upInfoAllList,
                           upInfo=upInfo,
                           videoAllList=videoAllList[:8],
                           videoInfo=videoInfo,
                           commentInfo=commentInfo[:5],
                           upId=upId,
                           userRole=userRole
                           )

@app.route('/upInfoEcharts')
def upInfoEcharts():
    email = session['email']
    userRole = session['userRole']
    upInfoAllList = getPublicData.getAllUpInfo()
    fensiData = getUpInfoEcharts.getFensiData()
    levenData = getUpInfoEcharts.getLevenData()
    xData,yData = getUpInfoEcharts.getVideLenData()
    return render_template('upInfoEcharts.html',
                           email=email,
                           userRole=userRole,
                           upInfoAllList=upInfoAllList,
                           fensiData=fensiData,
                           levenData=levenData,
                           xData=xData,
                           yData=yData
                           )

@app.route('/videoCommentEcharts')
def videoCommentEcharts():
    email = session['email']
    timeList = getSentimentData.getTimeList()
    defaultTime = request.args.get('time') if request.args.get('time') else timeList[0]
    upInfoAllList = getPublicData.getAllUpInfo()
    xData, yData, y1Data=getVideoCommentEcharts.getCommentLen(defaultTime)
    x1Data,y2Data = getVideoCommentEcharts.getUserCommentLikeTopData(defaultTime)
    sexData = getVideoCommentEcharts.getUserSexData(defaultTime)
    levelData = getVideoCommentEcharts.getUserLevelData(defaultTime)
    userRole = session['userRole']
    return render_template('videoCommentEcharts.html',
                           email=email,
                           upInfoAllList=upInfoAllList,
                           xData=xData,
                           yData=yData,
                           y1Data=y1Data,
                           x1Data=x1Data,
                           userRole=userRole,
                           y2Data=y2Data,
                           sexData=sexData,
                           levelData=levelData,
                           defaultTime=defaultTime,
                           timeList=timeList
                           )

@app.route('/videoListEcharts')
def videoListEcharts():
    email = session['email']
    timeList = getSentimentData.getTimesList()
    defaultTime = request.args.get('time') if request.args.get('time') else timeList[0]
    upInfoAllList = getPublicData.getAllUpInfo()
    xData,yData = getVideoListData.getVideoLenData(defaultTime)
    x1Data,y1Data = getVideoListData.getSeeNumData(defaultTime)
    userRole = session['userRole']
    return render_template('videoListEcharts.html',
                           email=email,
                           upInfoAllList=upInfoAllList,
                            xData=xData,
                           userRole=userRole,
                            yData=yData,
                           x1Data=x1Data,
                           y1Data=y1Data,
                           timeList=timeList,
                           defaultTime=defaultTime
                           )

@app.route('/title_cloud')
def title_cloud():
    email = session['email']
    userRole = session['userRole']

    upInfoAllList = getPublicData.getAllUpInfo()
    return render_template('title_cloud.html',
                           email=email,
                           upInfoAllList=upInfoAllList,
                           userRole=userRole
                           )

@app.route('/comment_content_cloud')
def comment_content_cloud():
    email = session['email']
    userRole = session['userRole']

    upInfoAllList = getPublicData.getAllUpInfo()
    return render_template('comment_content_cloud.html',
                           email=email,userRole=userRole,
                           upInfoAllList=upInfoAllList
                           )

@app.route('/logOut')
def logOut():
    session.clear()
    return redirect('/login')

@app.before_request
def before_requre():
    pat = re.compile(r'^/static')
    if re.search(pat,request.path):
        return
    if request.path == "/login" :
        return
    if request.path == '/registry':
        return
    uname = session.get('email')
    if uname:
        return None

    return redirect("/login")

if __name__ == '__main__':
    app.run(port=5000)
