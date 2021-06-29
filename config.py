"""
 -*- coding: utf-8 -*-
 @Time    : 2021/6/2 14:24
 @Author  : Sin
 @File    : config.py.py
 @Software: PyCharm
"""
DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD = 'sin227'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'f'


class Config(object):
    SECRET_KEY = 'a9087FFJFF9nnvc2@#$%FSD'
    # 格式为mysql+pymysql://数据库用户名:密码@数据库地址:端口号/数据库的名字?数据库格式
    #SQL_DATA_BASQ = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:sin227@localhost:3306/flask?charset=utf8'
