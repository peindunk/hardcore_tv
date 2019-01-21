#-*- coding:utf-8 -*-
from mysql_table import *
from config import *
from form_model import LoginForm,RegisteForm
from flask import Flask,render_template,request,session,jsonify
import api_for_surface as api
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)

# 制定数据库的配置
app.config['SQLALCHEMY_DATABASE_URI']="mysql://root:123456@localhost/hardcore_tv"
# 未来移除  避免warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_POOL_SIZE'] = 100
# 创建数据库实例
db = SQLAlchemy(app)
# CSRF
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/',methods=['GET','POST'])
def index():
    api_obj = api.API_Surface(request)
    # if request.method == "GET":
    result = api_obj.show_index()
    print(session.get('is_login'))
    user = api_obj.get_user()
    return render_template('home_page.html',result=result,user=user)

@app.route('/lubo/<int:id>',methods=['GET','POST'])
def lubo(id):
    api_obj = api.API_Surface(request)
    user = api_obj.get_user()
    if request.method == "GET":
        info,vl = api_obj.lubo_visble(id)
        comment = api_obj.comment_visible(id)
        print(comment)
    return render_template('TV_record1.html',comment=comment,info=info,videolist=vl,user=user)

@app.route('/get_comment',methods=['GET','POST'])
def get_comment():
    api_obj = api.API_Surface(request)
    user = api_obj.get_user()
    uid = user.user_id
    uname = user.user_name
    rid =  int(request.form["idnumber"].split('/')[-1])
    ccom = api_obj.save_comment(rid,uid,uname)
    return "%s:%s"%(ccom)


@app.route('/register',methods=['GET','POST'])
def register():
    sucess = 0
    api_obj = api.API_Surface(request)
    register = RegisteForm(request.form)
    if request.method == 'POST':
        sucess = api_obj.do_register(register)
    return render_template('register.html',form=register,sucess=sucess)

@app.route('/login',methods=['GET','POST'])
def login():
    login = LoginForm(request.form)
    api_obj = api.API_Surface(request)
    islogin = api_obj.do_login(login)
    if islogin:
        return render_template('skip.html')
    return render_template('login.html',form=login)

@app.route('/list/<type>/<int:p>',methods=['GET','POST'])
def livelist(type,p):
    apiobj = api.API_Surface(request)
    user = apiobj.get_user()
    if request.method == "GET":
        result = apiobj.showList(type)
        if result:
            page = apiobj.page_split(len(result))
            if p==1:
                visible = result[0:25]
            else:
                visible = result[(p-1)*25:(p-1)*25+25]
            return render_template('livelist.html',result=visible,page=page,current=p,type=type,user=user)
        else:
            return '<a href="/">无结果 请返回首页<a>'
    else:
        key = request.form['search']
        if not key:
            return "<a href='/list/all/1'>没有搜索内容 请返回重新输入<a>"
        result = apiobj.search(key)
        page = apiobj.page_split(len(result))
        if p == 1:
            visible = result[0:25]
        else:
            visible = result[(p - 1) * 25:(p - 1) * 25 + 25]
        return render_template('livelist.html',key=key,current=p,page=page,result=visible,user=user)

@app.route('/live/<int:id>',methods=['GET','POST'])
def liveroom(id):
    apiobj = api.API_Surface(request)
    score = None
    user = apiobj.get_user()
    if user:
        score = apiobj.get_socre()
    info = apiobj.show_live(id)
    return render_template('TV_live.html',info = info,user=user,score=score)

@app.route('/test')
def test():
    return render_template('mainTest.html')

@app.route('/skip/<status>')
def skip(status):
    if status == 'logout':
        session.pop('is_login')
    return render_template('skip.html')

@app.route('/ads',methods=['GET','POST'])
def ads():
    apiobj = api.API_Surface(request)
    user = apiobj.get_user()
    return render_template('ads.html',user=user)

@app.route('/bp',methods=['GET','POST'])
def add_sub_bp():
    print('改变积分')
    apiobj = api.API_Surface(request)
    user = apiobj.get_user()
    info = dict()
    if apiobj.change_bp(user):
        info['status'] = 'success'
    else:
        info['status'] = 'fail'
    return jsonify(info)

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/showpoint')
def showbp():
    apiobj = api.API_Surface(request)
    score = apiobj.get_socre()
    info = dict()
    info['bp'] = score
    return jsonify(info)

if __name__ == '__main__':
    # deleteAllTables()
    createTables()
    app.run('0.0.0.0',port=5000)
