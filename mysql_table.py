# -*- coding:utf-8 -*-
from hardcore_tv import db
from config import *
from flask_login import UserMixin

# 创建实体模板类
class UserMain(UserMixin,db.Model):
    __tablename__ = 'userinfo_main'
    user_id = db.Column(db.INTEGER,primary_key=True)
    user_name = db.Column(db.String(20),nullable=False,unique=True)
    u_passwd = db.Column(db.String(20),nullable=False)
    age = db.Column(db.INTEGER,nullable=False)
    email = db.Column(db.String(50),nullable=False)
    img = db.Column(db.String(128))

    other = db.relationship('UserOther',backref='userinfo_main',lazy='dynamic')
    fav = db.relationship('UserFav',backref='useinfo_main',lazy='dynamic')
    gift = db.relationship('UserGift',backref='userinfo_main',lazy='dynamic')
    score = db.relationship('UserScore',backref='userinfo_main',lazy='dynamic')

    def __init__(self,uname,pwd,age,email,img='img/user.jpg'):
        self.user_name = uname
        self.u_passwd = pwd
        self.age = age
        self.email = email
        self.img = img

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
    host_name = db.Column(db.String(50))
    img = db.Column(db.String(128))
    is_oline = db.Column(db.INTEGER)
    live_url = db.Column(db.String(128))

    count = db.relationship('RoomCount',backref='roominfo_main',lazy='dynamic')
    gift = db.relationship('RoomGift',backref='roominfo_main',lazy='dynamic')
    type = db.relationship('RoomType',backref='roominfo_main',lazy='dynamic')
    comment = db.relationship('RoomComment',backref='roominfo_main',lazy='dynamic')
    videolist = db.relationship('VideoList',backref='roominfo_main',lazy='dynamic')


    def __init__(self,rname,hname,img,ol,url):
        self.room_name = rname
        self.host_name = hname
        self.img = img
        self.is_oline = ol
        self.live_url = url

class RoomCount(db.Model):
    __tablename__ =  'roominfo_count'
    id = db.Column(db.INTEGER,primary_key=True)
    r_id = db.Column(db.INTEGER,db.ForeignKey('roominfo_main.room_id'))
    host_lv = db.Column(db.INTEGER)
    fans_num = db.Column(db.INTEGER)
    exp = db.Column(db.INTEGER)
    p_count = db.Column(db.INTEGER)

    def __init__(self,r_id,lv,fans,exp,pco):
        self.r_id = r_id
        self.lv = lv
        self.fans = fans
        self.exp = exp
        self.p_count = pco

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
    type = db.Column(db.Enum('PC游戏','主机游戏','手机游戏','户外美食','娱乐','其它'))

    def __init__(self,rid,type):
        self.r_id = rid
        self.type = type

class RoomComment(db.Model):
    # __tablename__ == 'room_comment'
    id = db.Column(db.INTEGER,primary_key=True)
    rid = db.Column(db.INTEGER,db.ForeignKey('roominfo_main.room_id'))
    uid = db.Column(db.INTEGER)
    comment = db.Column(db.Text)
    uname = db.Column(db.String(30))

    def __init__(self,rid,comment,uid,uname):
        self.rid = rid
        self.comment = comment
        self.uid = uid
        self.uname = uname

class VideoList(db.Model):
    # __table__ == 'videolist'
    id = db.Column(db.INTEGER,primary_key=True)
    rid = db.Column(db.INTEGER,db.ForeignKey('roominfo_main.room_id'))
    video_url = db.Column(db.String(128))
    poster_url = db.Column(db.String(128))
    video_name = db.Column(db.String(64))

    def __init__(self,rid,v_url,p_url,v_name):
        self.rid = rid
        self.video_url = v_url
        self.poster_url = p_url
        self.video_name = v_name

# 创建离线房间信息 空置房间封面
def gen_offline():
    rm = RoomMain('classic music for jay',
             '无与伦比',
             'img/jay.jpeg',
             0,
             '')
    db.session.add(rm)
    db.session.commit()
    rr = RoomMain.query.filter().all()[-1]
    rid = rr.room_id
    rc = RoomCount(rid,100,888888,0,0)
    rt = RoomType(rid,'娱乐')
    rcm = RoomComment(rid,'无与伦比 为杰沉沦',0,'小jayjay')
    db.session.add_all([rc,rt,rcm])
    db.session.commit()

    rm = RoomMain('经典nba赛事',
        'hardcore体育',
         'img/nba.jpeg',
          0,
         ''
    )
    db.session.add(rm)
    db.session.commit()
    rr = RoomMain.query.filter().all()[-1]
    rid = rr.room_id
    rc = RoomCount(rid,100,99999,0,0)
    rt = RoomType(rid,'娱乐')
    rcm = RoomComment(rid,'尽享经典nba赛事',0,'5皇james')
    db.session.add_all([rc,rt,rcm])
    db.session.commit()


# 插入爬取数据
def gen_data():
    with open('./spider/zhanqi.txt') as f:
        for line in f:
            data = line.split('##')
            if data[0][-1]=='万':
                p_count = int(float(data[0][:-1])*10000)
            else:
                p_count = int(data[0])
            host_name = data[1]
            r_name = data[2]
            img = data[3]
            type = data[4].strip()
            live_id = data[-1].strip()
            rm = RoomMain(r_name,host_name,img,1,zq_api+live_id)
            db.session.add(rm)
            db.session.commit()
            robj = RoomMain.query.filter().all()[-1]
            rc = RoomCount(robj.room_id,0,0,0,p_count)
            db.session.add(rc)
            db.session.commit()
            rg = RoomGift(robj.room_id,0,0,0,0)
            db.session.add(rg)
            db.session.commit()
            # 'PC游戏', '主机游戏', '手机游戏', '娱乐', '其它'
            if type in pcgame:
                type = 'PC游戏'
            elif type in videoGame:
                type = '主机游戏'
            elif type in mobileGame:
                type = '手机游戏'
            elif type in entertainment:
                type = '娱乐'
            else:
                type = '其它'
            rt = RoomType(robj.room_id,type)
            db.session.add(rt)
            db.session.commit()

# 删除房间相关数据
def del_room_table():
    del1 = RoomMain.query.filter().all()
    del2 = RoomGift.query.filter().all()
    del3 = RoomType.query.filter().all()
    del4 = RoomCount.query.filter().all()
    del5 = RoomComment.query.filter().all()
    del6 = VideoList.query.filter().all()
    for d in del1:
        db.session.delete(d)
    for d in del2:
        db.session.delete(d)
    for d in del3:
        db.session.delete(d)
    for d in del4:
        db.session.delete(d)
    for d in del5:
        db.session.delete(d)
    for d in del6:
        db.session.delete(d)
    db.session.commit()

# 创建初始表
def createTables():
    db.create_all()
    # 创建管理员
    adm = UserMain.query.filter(UserMain.user_name=='admin').first()
    if not adm:
        admobj = UserMain('admin','admin',0,'admin@admin.com')
        db.session.add(admobj)
        db.session.commit()
    del_room_table()
    gen_data()
    gen_offline()

def deleteAllTables():
    db.drop_all()
