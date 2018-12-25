#-*- coding:utf-8 -*-
from mysql_table import *
from config import *
from form_model import LoginForm,RegisteForm
from flask import Flask,render_template,request
import api_for_surface as api
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)

# 制定数据库的配置
app.config['SQLALCHEMY_DATABASE_URI']="mysql://root:123456@localhost/hardcore_tv"
# 未来移除  避免warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# 创建数据库实例
db = SQLAlchemy(app)
# CSRF
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/',methods=['GET','POST'])
def index():
    return render_template('home_page.html')

@app.route('/lubo',methods=['GET','POST'])
def lubo():
    api_obj = api.API_Surface(request)
    if request.method == "GET":
        api_obj.lubo_visble()
        comment = api_obj.comment_visible()
    return render_template('TV_record1.html',comment = comment)

@app.route('/register',methods=['GET','POST'])
def register():
    api_obj = api.API_Surface(request)
    register = RegisteForm(request.form)
    if request.method == 'POST':
        api_obj.do_register(register)
    return render_template('register.html',form=register)

@app.route('/login',methods=['GET','POST'])
def login():
    login = LoginForm(request.form)
    api_obj = api.API_Surface(request)
    islogin = api_obj.do_login(login)
    if islogin:
        return render_template('mainTest.html')
    return render_template('login.html',form=login)

@app.route('/list/<type>',methods=['GET','POST'])
def livelist(type):
    return render_template('livelist.html')

@app.route('/live',methods=['GET','POST'])
def liveroom():
    return render_template('TV_live.html')

@app.route('/test')
def test():
    return render_template('mainTest.html')

if __name__ == '__main__':
    # deleteAllTables()
    createTables()
    app.run('0.0.0.0',port=5000)