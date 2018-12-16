#-*- coding:utf-8 -*-
from mysql_table import *
from config import  *
from flask import Flask,render_template,request,flash
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,IntegerField,RadioField,TextAreaField,widgets
from wtforms.validators import DataRequired,EqualTo,Email,NumberRange,Length
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)

# CSRF
app.config['SECRET_KEY'] = SECRET_KEY

# 制定数据库的配置
app.config['SQLALCHEMY_DATABASE_URI']="mysql://root:123456@localhost/hardcore_tv"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
# 未来移除  避免warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

# 创建数据库实例
db = SQLAlchemy(app)


class LoginForm(FlaskForm):
    uname = StringField('用户名',validators=[DataRequired()])
    upwd = StringField('密码',validators=[DataRequired()],widget=widgets.PasswordInput())
    submit = SubmitField('登录')

class RegisteForm(FlaskForm):
    uname = StringField('用户名',validators=[DataRequired(),Length(1,8)])
    upwd1 = StringField('密码',
                        validators=[DataRequired()],
                        widget=widgets.PasswordInput())
    upwd2 = StringField('确认密码',
                        validators=[DataRequired(),EqualTo('upwd1','密码不一致')],
                        widget=widgets.PasswordInput())
    age = IntegerField('年龄',validators=[DataRequired(),NumberRange(1,150)])
    email = StringField('邮箱',validators=[DataRequired(),Email()])

    # sex = RadioField('性别',validators=[DataRequired()])
    phone = StringField('手机',validators=[DataRequired(),Length(11,12)])
    city = StringField('城市',validators=[DataRequired(),Length(1,10)])
    ps = TextAreaField('签名')
    submit = SubmitField('注册')

def do_register(register):
    uname = register.uname.data
    upwd = register.upwd1.data
    age = register.age.data
    email = register.email.data

    # sex = register.sex.data
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
        user = UserMain.query.filter_by(user_name=uname).first()
        uid = user.user_id
        user_o = UserOther(uid,'男',phone,city,ps)
        db.session.add(user_o)
        db.session.commit()
        user_s = UserScore(uid,100)
        db.session.add(user_s)
        db.session.commit()
        user_g = UserGift(uid,0,0,0,0)
        db.session.add(user_g)
        db.session.commit()
    else:
        flash('有选项为空或者填写不正确')

@app.route('/',methods=['GET','POST'])
def index():
    return render_template('mainTest.html')


@app.route('/lubo',methods=['GET','POST'])
def lubo():
    return render_template('TV.html')


@app.route('/register',methods=['GET','POST'])
def register():
    register = RegisteForm(request.form)
    # if request.method == 'GET':
    #     return render_template('register.html',form=register)
    if request.method == 'POST':
        do_register(register)
    return render_template('register.html',form=register)

@app.route('/login',methods=['GET','POST'])
def login():
    login = LoginForm(request.form)
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
                else:
                    return render_template('mainTest.html')
    return render_template('login.html',form=login)


if __name__ == '__main__':
    createTables()
    app.run('0.0.0.0',port=5000)
