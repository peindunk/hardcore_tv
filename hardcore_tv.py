#-*- coding:utf-8 -*-
from mysql_table import *
from config import *
from form_model import LoginForm,RegisteForm
from flask import Flask,render_template,request,flash
from flask_sqlalchemy import SQLAlchemy
from spider.douyu import Douyu
import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)

# CSRF
app.config['SECRET_KEY'] = SECRET_KEY

# 制定数据库的配置
app.config['SQLALCHEMY_DATABASE_URI']="mysql://root:123456@localhost/hardcore_tv"
# 未来移除  避免warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

# 创建数据库实例
db = SQLAlchemy(app)

def do_login(login):
    if request.method == 'POST':
        uname = login.uname.data
        upwd = login.upwd.data
        user = UserMain.query.filter_by(user_name=uname).first()
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

def do_register(register):
    uname = register.uname.data
    upwd = register.upwd1.data
    age = register.age.data
    email = register.email.data

    sex = register.sex.data
    phone = register.phone.data
    city = register.city.data
    ps = register.ps.data

    un = UserMain.query.filter_by(user_name=uname).first()
    if un:
        flash('用户已经存在')
        return
    if register.validate_on_submit():
        print('验证通过')
        user_m = UserMain(uname,upwd,age,email)
        db.session.add(user_m)
        db.session.commit()
        user = UserMain.query.filter().all()[-1]
        print('user',user)
        uid = user.user_id
        user_o = UserOther(uid,sex,phone,city,ps)
        db.session.add(user_o)
        db.session.commit()
        user_s = UserScore(uid,100)
        db.session.add(user_s)
        db.session.commit()
        user_g = UserGift(uid,0,0,0,0)
        db.session.add(user_g)
        db.session.commit()
        flash('注册成功～～～～～')
    else:
        flash('有选项为空或者填写不正确')

# 录播显示数据接口
def lubo_visble():
    rid = 1555
    rm = RoomMain.query.filter(RoomMain.room_id==rid).first()
    rcm = RoomComment.query.filter(RoomComment.rid==rid).all()
    rc = RoomCount.query.filter(RoomCount.r_id==rid).first()
    rt = RoomType.query.filter(RoomType.r_id==rid).first()
    if rt:
        type = rt.type
    if rc:
        lv = rc.host_lv
        fans = rc.fans_num
        exp = rc.exp
        pcount = rc.p_count
    if rm:
        rname = rm.room_name
        hname = rm.host_name
        print(type,lv,fans,exp,pcount,rname,hname)
    user_com = []
    for item in rcm:
        user_com.append((item.uname,item.comment))
    # 显示逻辑　显示录像列表

@app.route('/',methods=['GET','POST'])
def index():
    result = ''
    if request.method=='POST':
        result = request.form['num']
        print(result)
    return render_template('mainTest.html',result=result)


@app.route('/lubo',methods=['GET','POST'])
def lubo():
    if request.method == "GET":
        lubo_visble()
    return render_template('TV.html')

@app.route('/register',methods=['GET','POST'])
def register():
    register = RegisteForm(request.form)
    if request.method == 'POST':
        do_register(register)
    return render_template('register.html',form=register)

@app.route('/login',methods=['GET','POST'])
def login():
    login = LoginForm(request.form)
    islogin = do_login(login)
    if islogin:
        return render_template('mainTest.html')
    return render_template('login.html',form=login)

@app.route('/all',methods=['GET','SET'])
def livelist():
    return render_template('livelist.html')

if __name__ == '__main__':
    # deleteAllTables()
    createTables()
    app.run('0.0.0.0',port=5000)
