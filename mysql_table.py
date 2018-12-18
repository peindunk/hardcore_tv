# -*- coding:utf-8 -*-
from hardcore_tv import *

# 创建实体模板类
class UserMain(db.Model):
    __tablename__ = 'userinfo_main'
    user_id = db.Column(db.INTEGER,primary_key=True)
    user_name = db.Column(db.String(20),nullable=False,unique=True)
    u_passwd = db.Column(db.String(20),nullable=False)
    age = db.Column(db.INTEGER,nullable=False)
    email = db.Column(db.String(50),nullable=False)

    other = db.relationship('UserOther',backref='userinfo_main',lazy='dynamic')
    fav = db.relationship('UserFav',backref='useinfo_main',lazy='dynamic')
    gift = db.relationship('UserGift',backref='userinfo_main',lazy='dynamic')
    score = db.relationship('UserScore',backref='userinfo_main',lazy='dynamic')

    def __init__(self,uname,pwd,age,email):
        self.user_name = unamespan
        self.u_passwd = pwd
        self.age = age
        self.email = email

    def __repr__(self):
        return 'userinfo %s %s'%(self.user_name,self.u_passwd)



class UserOther(db.Model):
    __tablename__ = 'user_other_info'
    id = db.Column(db.INTEGER,primary_key=True)
    uid = db.Column(db.INTEGER,db.ForeignKey('userinfo_main.user_id'))
    sex = db.Column(db.Enum('男','女','保密'),nullable=True)
    phone = db.Column(db.String(11),nullable=True)
    city = db.Column(db.String(15),nullable=True)
    ps = db.Column(db.Text,nullable=True)

    def __init__(self,uid,sex,phone,city,ps):
        self.uid = uid
        self.sex = sex
        self.phone = phone
        self.city = city
        self.ps = ps


class UserFav(db.Model):
    __tablename__ = 'user_fav'
    id = db.Column(db.INTEGER,primary_key=True)
    uid = db.Column(db.INTEGER,db.ForeignKey('userinfo_main.user_id'))
    fav = db.Column(db.INTEGER,unique=True)

    def __init__(self,uid,fav):
        self.uid = uid
        self.fav = fav

class RoomMain(db.Model):
    __tablename__ = 'roominfo_main'
    room_id = db.Column(db.INTEGER,primary_key=True)
    room_name = db.Column(db.String(100))
    room_comment = db.Column(db.Text)
    host_name = db.Column(db.String(20))

    count = db.relationship('RoomCount',backref='roominfo_main',lazy='dynamic')
    gift = db.relationship('RoomGift',backref='roominfo_main',lazy='dynamic')
    video = db.relationship('VideoLoad',backref='roominfo_main',lazy='dynamic')
    type = db.relationship('RoomType',backref='roominfo_main',lazy='dynamic')

    def __init__(self,rname,rcomment,hname):
        self.room_name = rname
        self.room_comment = rcomment
        self.host_name = hname

class RoomCount(db.Model):
    __tablename__ =  'roominfo_count'
    id = db.Column(db.INTEGER,primary_key=True)
    r_id = db.Column(db.INTEGER,db.ForeignKey('roominfo_main.room_id'))
    host_lv = db.Column(db.INTEGER)
    fans_num = db.Column(db.INTEGER)
    exp = db.Column(db.INTEGER)

    def __init__(self,r_id,lv,fans,exp):
        self.r_id = r_id
        self.lv = lv
        self.fans = fans
        self.exp = exp

class RoomGift(db.Model):
    __tablename__ = 'roominfo_gift'
    id = db.Column(db.INTEGER,primary_key=True)
    r_id = db.Column(db.INTEGER,db.ForeignKey('roominfo_main.room_id'))
    free = db.Column(db.INTEGER)
    low = db.Column(db.INTEGER)
    middle = db.Column(db.INTEGER)
    highclass = db.Column(db.INTEGER)

    def __init__(self,r_id,free,low,middle,high):
        self.r_id = r_id
        self.free = free
        self.low = low
        self.middle = middle
        self.high = high


class UserGift(db.Model):
    __tablename__ = 'userinfo_gift'
    id = db.Column(db.INTEGER,primary_key=True)
    u_id = db.Column(db.INTEGER, db.ForeignKey('userinfo_main.user_id'))
    free = db.Column(db.INTEGER)
    low = db.Column(db.INTEGER)
    middle = db.Column(db.INTEGER)
    highclass = db.Column(db.INTEGER)

    def __init__(self,u_id,free,low,middle,high):
        self.u_id = u_id
        self.free = free
        self.low = low
        self.middle = middle
        self.high = high

class VideoLoad(db.Model):
    __tablename__ = 'video_load'
    id = db.Column(db.INTEGER,primary_key=True)
    r_id = db.Column(db.INTEGER,db.ForeignKey('roominfo_main.room_id'))
    path = db.Column(db.String(100))

    def __init__(self,rid,path):
        self.r_id = rid
        self.path = path

class UserScore(db.Model):
    __tablename__ = 'user_score'
    id = db.Column(db.INTEGER,primary_key=True)
    u_id = db.Column(db.INTEGER, db.ForeignKey('userinfo_main.user_id'))
    score = db.Column(db.INTEGER)

    def __init__(self,uid,score):
        self.u_id = uid
        self.score = score

class RoomType(db.Model):
    __tablename__ = 'room_type'
    id = db.Column(db.INTEGER,primary_key=True)
    r_id = db.Column(db.INTEGER,db.ForeignKey('roominfo_main.room_id'))
    type = db.Column(db.Enum('体育','游戏','娱乐','户外','星秀'))

    def __init__(self,rid,type):
        self.r_id = rid
        self.type = type


def createTables():
    db.create_all()

def deleteTables():
    db.drop_all()

