"""
 -*- coding: utf-8 -*-
 @Time    : 2021/6/2 20:06
 @Author  : Sin
 @File    : models.py
 @Software: PyCharm
 用户数据库模型
"""
from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
# 简便实现用户类
from flask_login import UserMixin
from app import login
from hashlib import md5


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    gender = db.Column(db.String(10))
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime,default=datetime.utcnow())
    user_avatar = db.Column(db.String(140))

    # back是反向引用,User和Post是一对多的关系，backref是表示在Post中新建一个属性author，关联的是Post中的user_id外键关联的User对象。
    # lazy属性常用的值的含义，select就是访问到属性的时候，就会全部加载该属性的数据;joined则是在对关联的两个表进行join操作，从而获取到所有相关的对象;
    # dynamic则不一样，在访问属性的时候，并没有在内存中加载数据，而是返回一个query对象, 需要执行相应方法才可以获取对象，比如.all()
    post = db.relationship('Post', backref='author', lazy='dynamic')
    comment = db.relationship('Comment',backref='author',lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # __repr__()用于显示给开发人员。
    def __repr__(self):
        return '<用户名:{}>'.format(self.username)

    def avatar(self,size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://dn-qiniu-avatar.qbox.me/avatar/{}?d=identicon&s={}'.format(digest, size)


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    count = db.Column(db.Integer)
    reply = db.Column(db.Integer)
    category = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comment = db.relationship('Comment',backref=' ',lazy='dynamic')

    #def __repr__(self):
       # return '<Post {}>'.format(self.body)


class Comment(db.Model):
    __tablename__= 'comment'
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer,db.ForeignKey('post.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    body = db.Column(db.String(140),nullable=False)
    #post = db.relationship('Post',backref=db.backref('article'))
    #user = db.relationship('User',backref=db.backref('author'))



# 必须提供一个 user_loader 回调。这个回调用于从会话中存储的用户 ID 重新加载用户对象。
# 它应该接受一个用户的 unicode ID 作为参数，并且返回相应的用户对象
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
