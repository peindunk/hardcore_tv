# -*- coding:utf-8 -*-
from flask import flash,jsonify,session
import mysql_table as mt
import time
from werkzeug.security import check_password_hash,generate_password_hash

class API_Surface:
    def __init__(self,req,db=None):
        self.request = req
        self.db = db

    def do_login(self,login):
        if self.request.method == 'POST':
            uname = login.uname.data
            upwd = login.upwd.data
            user = mt.UserMain.query.filter_by(user_name=uname).first()
            # 通过验证器验证
            if login.validate_on_submit():
                if not user:
                    flash('用户不存在')
                else:
                    if not check_password_hash( user.u_passwd,upwd):
                    # if user.u_passwd != upwd:
                        flash('密码不正确')
                        return 0
                    else:
                        session.permanent = True
                        session['is_login'] = '%d:1'%user.user_id
                        print('登录成功')
                        return 1

    def do_register(self,register):
        uname = register.uname.data
        upwd = register.upwd1.data
        age = register.age.data
        email = register.email.data

        sex = register.sex.data
        phone = register.phone.data
        city = register.city.data
        ps = register.ps.data

        un = mt.UserMain.query.filter_by(user_name=uname).first()
        if un:
            flash('用户已经存在')
            return
        if register.validate_on_submit():
            print('验证通过')
            upwd = generate_password_hash(upwd)
            user_m = mt.UserMain(uname,upwd,age,email)
            mt.db.session.add(user_m)
            mt.db.session.commit()
            user = mt.UserMain.query.filter().all()[-1]
            uid = user.user_id
            user_o = mt.UserOther(uid,sex,phone,city,ps)
            mt.db.session.add(user_o)
            mt.db.session.commit()
            user_s = mt.UserScore(uid,100)
            mt.db.session.add(user_s)
            mt.db.session.commit()
            user_g = mt.UserGift(uid,0,0,0,0)
            mt.db.session.add(user_g)
            mt.db.session.commit()
            flash('注册成功～～即将跳转')
            session.permanent = True
            session['is_login'] = '%d:1'%uid
            print('是否成功存储session',session.get('is_login'))
            return True
        else:
            flash('有选项为空或者填写不正确')
            return False

    # 录播显示数据接口
    def lubo_visble(self,rid):
        # 数据库查询
        rm = mt.RoomMain.query.filter(mt.RoomMain.room_id==rid).first()
        rc = mt.RoomCount.query.filter(mt.RoomCount.r_id==rid).first()
        rt = mt.RoomType.query.filter(mt.RoomType.r_id==rid).first()
        vl = mt.VideoList.query.filter(mt.VideoList.rid==rid).all()
        info = dict()
        if rt:
            type = rt.type
            info["type"] = type
        if rc:
            lv = rc.host_lv
            fans = rc.fans_num
            exp = rc.exp
            pcount = rc.p_count
            info["lv"] = lv
            info["fans"] = fans
            info["exp"] = exp
            info["pcount"] = pcount
        if rm:
            rname = rm.room_name
            hname = rm.host_name
            himg = rm.host_img
            info["room_name"] = rname
            info["host_name"] = hname
            info["himg"] =himg

        # if vl:
        #     for v in vl:
        #         info["video_url"] = v.video_url
        #         info["poster_url"] = v.poster_url
        #         info["video_name"] = v.video_name
        return  (info,vl)

    # 评论
    def comment_visible(self,rid):
        rcm = mt.db.session.query(mt.RoomComment).all()
        mt.db.session.commit()
        print(rcm)
        user_com = []
        for item in rcm:
            if item.rid == rid:
                user_com.append(item.uname+":"+item.comment)
        return user_com

    def show_index(self):
        pc = mt.RoomType.query.filter(mt.RoomType.type=='PC游戏').all()[:4]
        moblie = mt.RoomType.query.filter(mt.RoomType.type=='手机游戏')[:4]
        rids = []
        for p in pc:
            rids.append(p.r_id)
        for m in moblie:
            rids.append(m.r_id)
        rms = []
        for id in rids:
            rm = mt.RoomMain.query.filter(mt.RoomMain.room_id==id).first()
            rms.append(rm)
        return rms

    def show_live(self,rid):
        rm = mt.RoomMain.query.filter(mt.RoomMain.room_id==rid).first()
        rc = mt.RoomCount.query.filter(mt.RoomCount.r_id==rid).first()
        rt = mt.RoomType.query.filter(mt.RoomType.r_id==rid).first()
        info = dict()
        if rm:
            live_url = rm.live_url
            rname = rm.room_name
            hname = rm.host_name
            himg = rm.host_img
            info["live_url"] = live_url
            info["room_name"] = rname
            info["host_name"] = hname
            info['himg'] = himg
        if rc:
            lv = rc.host_lv
            fans = rc.fans_num
            exp = rc.exp
            pcount = rc.p_count
            info["lv"] = lv
            info["fans"] = fans
            info["exp"] = exp
            info["pcount"] = pcount
        if rt:
            type = rt.type
            info["type"] = type
        # 需要数据　真实流　房间名　主播名　关注数　人数 主播头像 分类 （经验 等级）

        return info

    # 搜索接口
    def search(self,key):
        result = []
        # 获取搜索内容
        rm = mt.RoomMain.query.filter().all()
        rids = []
        for r in rm:
            if (key in r.room_name) or (key in r.host_name):
                rids.append(r.room_id)
        # 返回显示逻辑
        # 需要显示的内容 封面　　房间名　　主播名　　人数　　类名
        rms = []
        rcs = []
        rts = []
        for rid in rids:
            rm = mt.RoomMain.query.filter(mt.RoomMain.room_id==rid).first()
            rc = mt.RoomCount.query.filter(mt.RoomCount.r_id==rid).first()
            rt = mt.RoomType.query.filter(mt.RoomType.r_id==rid).first()
            rms.append(rm)
            rcs.append(rc)
            rts.append(rt)
        for rid,rm,rc,rt in zip(rids,rms,rcs,rts):
            d = dict()
            d['rid'] = rid
            d['img'] = rm.img
            d['rname'] = rm.room_name
            d['hname'] = rm.host_name
            d['isol'] = rm.is_oline
            d['pcount'] = rc.p_count
            d['type'] = rt.type
            result.append(d)
        return result

    # 获取列表页面接口
    def showList(self,type):
        result = []
        if type == 'all':
            rts = mt.RoomType.query.filter().all()
        else:
            # PC游戏', '主机游戏', '手机游戏', '娱乐', '其它'
            if type == 'pcgame':
                rts = mt.RoomType.query.filter(mt.RoomType.type == 'PC游戏').all()
            elif type == 'vgame':
                rts = mt.RoomType.query.filter(mt.RoomType.type == '主机游戏').all()
            elif type == 'mgame':
                rts = mt.RoomType.query.filter(mt.RoomType.type == '手机游戏').all()
            elif type == 'enjoy':
                rts = mt.RoomType.query.filter(mt.RoomType.type == '娱乐').all()
            elif type == 'other':
                rts = mt.RoomType.query.filter(mt.RoomType.type == '其它').all()
            else:
                rts = []

        # 需要显示的内容 封面　　房间名　　主播名　　人数　　类名
        rms = []
        rcs = []
        rids = []
        for rt in rts:
            rids.append(rt.r_id)
            rm = mt.RoomMain.query.filter(mt.RoomMain.room_id==rt.r_id).first()
            rc = mt.RoomCount.query.filter(mt.RoomCount.r_id==rt.r_id).first()
            rms.append(rm)
            rcs.append(rc)
        for rid,rm,rc,rt in zip(rids,rms,rcs,rts):
            d = dict()
            d['rid'] = rid
            d['img'] = rm.img
            d['rname'] = rm.room_name
            d['hname'] = rm.host_name
            d['isol'] = rm.is_oline
            d['pcount'] = rc.p_count
            d['type'] = rt.type
            result.append(d)
        return result

    # 分页
    def page_split(self,count):
        if  count % 25==0:
            page = count//25
        else:
            page = count//25 + 1
        return page

    def show_login(self):
        if session.get('islogin')[-1] == 1:
            return 1
        else:
            return 0

    def get_user(self):
        if session.get('is_login'):
            uid = int(session.get('is_login').split(':')[0])
            user = mt.UserMain.query.filter(mt.UserMain.user_id==uid).first()
            return user
        return None

    # 积分变动
    def change_bp(self,user):
        data = self.request.get_json()['bp']
        uid = user.user_id
        us = mt.UserScore.query.filter(mt.UserScore.u_id==uid).first()
        if us.score + data >= 0:
            us.score += data
            mt.db.session.add(us)
            mt.db.session.commit()
            return True
        else:
            return False

    def get_socre(self):
        user = self.get_user()
        us = mt.UserScore.query.filter(mt.UserScore.u_id==user.user_id).first()
        return us.score

    def save_comment(self,rid,uid,uname):
        # 存入数据库
        aname = self.request.form["uname"]
        acomment = self.request.form["ucomment"]
        print('uname', aname)
        print('comment', acomment)
        comment_data = mt.RoomComment(rid, acomment, uid, uname)
        mt.db.session.add(comment_data)
        mt.db.session.commit()
        return  (aname,acomment)

