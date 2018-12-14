#-*- coding:utf-8 -*-
from flask import Flask,render_template,request
from mysql_table import *
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)

# 制定数据库的配置
app.config['SQLALCHEMY_DATABASE_URI']="mysql://root:123456@localhost/hardcore_tv"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True

# 创建数据库实例
db = SQLAlchemy(app)

def register_api(req):
    uname = req['user_name']
    upwd1 = req['u_passwd']
    upwd2 = req['u_passwd2']
    age = req['age']
    email = req['email']
    sex = req['sex']
    phone = req['phone']
    city = req['city']
    ps = req['ps']


@app.route('/',methods=['GET','POST'])
def hello_world():
    # user = UserFav.query.filter(UserFav.uid==None)
    # [db.delete(u) for u in user]
    # db.session.commit()
    return '欢迎来到Hardcore TV!'


@app.route('/lubo',methods=['GET','POST'])
def lubo():
    return render_template('TV.html')


@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        register_api(request.form)
        return '欢迎来到Hardcore TV'

if __name__ == '__main__':
    db.create_all()
    app.run()
