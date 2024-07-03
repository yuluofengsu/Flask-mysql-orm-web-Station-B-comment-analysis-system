from settings import db


# 定义模型
class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    role = db.Column(db.String(255))

class upinfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mid = db.Column(db.String(255))
    upName = db.Column(db.String(255))
    fensi = db.Column(db.Integer)
    avatar = db.Column(db.String(255))
    level = db.Column(db.Integer)
    upVideoLen = db.Column(db.Integer)
    sign = db.Column(db.String(255))

class videolist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    videoLen = db.Column(db.Integer)
    videoId = db.Column(db.Integer)
    avatar = db.Column(db.String(255))
    seeNum = db.Column(db.String(255))
    mid = db.Column(db.String(255))
    created = db.Column(db.String(255))
    title = db.Column(db.String(255))
    bvid = db.Column(db.String(255))

class videocomments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    videoId = db.Column(db.Integer)
    uname = db.Column(db.String(255))
    avatar = db.Column(db.String(255))
    content = db.Column(db.String(255))
    sex = db.Column(db.String(255))
    mid = db.Column(db.Integer)
    likes = db.Column(db.Integer)
    created = db.Column(db.String(255))
    vipLen = db.Column(db.Integer)
