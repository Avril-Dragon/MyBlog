"""
 -*- coding: utf-8 -*-
 @Time    : 2021/6/2 14:30
 @Author  : Sin
 @File    : __init__.py
 @Software: PyCharm
"""

from flask import Flask
# 导入配置文件
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
#from app.models import User

app = Flask(__name__)
# 添加配置信息
app.config.from_object(Config)

# 建立数据库关系
db = SQLAlchemy(app)
# 绑定app与数据库
migrate = Migrate(app,db)
# 创建用户对象
login = LoginManager(app)
# 登录管理对象 login_manager 的 login_view 属性，指定登录页面的视图函数
login.login_view = 'login'

from app import routes, models


