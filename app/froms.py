"""
 -*- coding: utf-8 -*-
 @Time    : 2021/6/2 15:20
 @Author  : Sin
 @File    : froms.py
 @Software: PyCharm
 表单信息
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User,Post


class LoginForm(FlaskForm):
    # DataRequired，当你在当前表格没有输入而直接到下一个表格时会提示你输入
    username = StringField('用户名', validators=[DataRequired(message='请输入用户名')])
    password = PasswordField('密码', validators=[DataRequired(message='请输入密码')])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')


class RegistrationForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(message='请输入用户名')])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    password2 = PasswordField('确认密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('注册')

    # 自定义验证器validate_(写需要验证的字段名如username，)
    # 校验用户名是否重复
    def validate_username(self, username):
        # 通过.data 获取到前端传入数据， 与数据库对比。
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('用户名重复了，请您重新换一个呗!')

    # 校验邮箱是否重复
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            print('xxxxxxxxxxxxxx')
            raise ValidationError('邮箱重复了，请您重新换一个呗!')


class EditProfileForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(message='请输入用户名')])
    about_me = TextAreaField('关于我', validators=[Length(min=0, max=140)])
    submit = SubmitField('提交')

    def validate_username(self, username):
        # 通过.data 获取到前端传入数据， 与数据库对比。
        user = User.query.filter_by(username=username.data).first()
        # 判断用户名是否存在或者没有修改
        if user is not None and user.username != username.data:
            raise ValidationError('用户名重复了，请您重新换一个呗!')


class PostForm(FlaskForm):
    title = StringField('标题',validators=[DataRequired(message='标题不能为空')])
    body = TextAreaField('文章内容',validators=[DataRequired(message='请输入文章内容')])
    submit = SubmitField('发布')


class CommentForm(FlaskForm):
    body = TextAreaField('评论',validators=[DataRequired(message='评论不能为空')])
    submit = SubmitField('发布')