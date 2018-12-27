# -*- coding:utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,IntegerField,RadioField,TextAreaField,widgets
from wtforms.validators import DataRequired,EqualTo,Email,NumberRange,Length

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

    sex = RadioField('性别',
                     choices=[('男','男'),('女','女'),('保密','保密')],
                     validators=[DataRequired()])
    phone = StringField('手机',validators=[DataRequired(),Length(11,12)])
    city = StringField('城市',validators=[DataRequired(),Length(1,10)])
    ps = TextAreaField('签名')
    submit = SubmitField('注册')