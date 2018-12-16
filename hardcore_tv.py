#-*- coding:utf-8 -*-
from mysql_table import *
from flask import Flask,render_template,request
from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,SelectField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)

# 制定数据库的配置
app.config['SQLALCHEMY_DATABASE_URI']="mysql://root:123456@localhost/hardcore_tv"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
# 未来移除  不看warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

# 创建数据库实例
db = SQLAlchemy(app)


class LoginForm(FlaskForm):
    uname = StringField(label='用户名:',validators=[DataRequired('请输入用户名')],
                        description='请输入标题',render_kw={"required":"required"})
    submit = SubmitField('提交')

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
def index():
    # user = UserMain('xz','123456',25,'123@qq.com')
    # db.session.add(user)
    # db.session.commit()
    return render_template('mainTest.html')


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

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return  render_template('login.html')
    else:
        uname = request.form['uname']
        upwd = request.form['pwd']
        user = UserMain.query.filter_by(user_name=uname).first()
        if not user:
            return '没有此用户'
        else:
            if user.u_passwd == upwd:
                return '登录成功'
            else:
                return '登录失败'


if __name__ == '__main__':
    createTables()
    app.run()
