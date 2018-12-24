# -*- coding:utf-8 -*-
from flask import flash,jsonify
import mysql_table as mt

class API_Surface:
    def __init__(self,req):
        self.request = req

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
                    if user.u_passwd != upwd:
                        flash('密码不正确')
                        return 0
                    else:
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
            user_m = mt.UserMain(uname,upwd,age,email)
            mt.db.session.add(user_m)
            mt.db.session.commit()
            user = mt.UserMain.query.filter().all()[-1]
            print('user',user)
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
            flash('注册成功～～～～～')
        else:
            flash('有选项为空或者填写不正确')

    # 录播显示数据接口（等待前段页面）
    def lubo_visble(self):
        # 获取rid
        rid = 1555
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
            info["room_name"] = rname
            info["host_name"] = hname
            print(type,lv,fans,exp,pcount,rname,hname)

        if vl:
            for v in vl:
                info["video_url"] = v.video_url
                info["poster_url"] = v.poster_url
                info["video_name"] = v.video_name
        return  jsonify(info)

    def comment_visible(self):
        rid = 1
        rcm = mt.RoomComment.query.filter(mt.RoomComment.rid==rid).all()
        user_com = []
        for item in rcm:
            user_com.append(item.uname+":"+item.comment)
        return user_com


    def show_live(self):
        rid = 1
        rm = mt.RoomMain.query.filter(mt.RoomMain.room_id==rid).all()
        rc = mt.RoomCount.query.filter(mt.RoomCount.r_id==rid).first()
        rt = mt.RoomType.query.filter(mt.RoomType.r_id==rid).first()
        info = dict()
        if rm:
            live_url = rm.live_url
            rname = rm.room_name
            hname = rm.host_name
            info["live_url"] = live_url
            info["room_name"] = rname
            info["host_name"] = hname
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
        return jsonify(info)


    # 搜索接口  (等待完成)
    def search(self):
        # 获取搜索内容
        s = ''
        rm = mt.RoomMain.query.filter().all()
        result = []
        for r in rm:
            if (s in r.room_name) or (s in r.host_name):
                result.append(r.room_id)
        # 返回显示逻辑
        return result

    # 获取列表页面接口
    def showList(self):
        type = 'all'
        # 需要显示的内容
        rid = 1
        rm = mt.RoomMain.query.filter(mt.RoomMain.room_id == rid).all()
        rc = mt.RoomCount.query.filter(mt.RoomCount.r_id == rid).first()
        rt = mt.RoomType.query.filter(mt.RoomType.r_id == rid).first()
        info = dict()
        if rm:
            live_url = rm.live_url
            rname = rm.room_name
            hname = rm.host_name
            info["live_url"] = live_url
            info["room_name"] = rname
            info["host_name"] = hname
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

