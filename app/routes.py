"""
 -*- coding: utf-8 -*-
 @Time    : 2021/6/2 14:36
 @Author  : Sin
 @File    : routes.py
 @Software: PyCharm
 视图函数
"""
import math
import os

from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from app.froms import LoginForm, RegistrationForm, EditProfileForm, PostForm, CommentForm, AvatarForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post, Comment
from app import app, db
from datetime import datetime
from flask_sqlalchemy import Pagination


@app.route('/')
@app.route('/index/',methods=['GET','POST'])
# @login_required
def index(view='timestamp'):
    view = request.args.get('view', 'timestamp')
    filter = request.args.get('filter', 'default')
    print(str(filter))
    fil_change = {'default': 'default', 'yule': '娱乐八卦', 'zatan':'树洞杂谈' , 'qinggan':'情感天地','tucao': '不吐不快'}
    fil_result = fil_change[filter.strip("'")]
    user = {'username': '游客'}
    # 获取当前页数
    page = int(request.args.get('page', 1))
    # 获取每页显示数据
    per_page = int(request.args.get('perpage', 6))
    # context = {
    # 查询数据，摈弃字典
    if filter != "default":
        Post_filter = Post.query.filter_by(category=fil_result)
    else:
        Post_filter = Post.query
    if view == 'count':
        # flash('count')
        paginates = Post_filter.order_by('count').paginate(page, per_page, error_out=False)
    elif view == 'reply':
        # flash('reply')
        paginates = Post_filter.order_by('reply').paginate(page, per_page, error_out=False)
    else:
        # flash('timestamp')
        paginates = Post_filter.order_by('timestamp').paginate(page, per_page, error_out=False)
    # }
    posts = paginates.items
    # 总页数
    totalpage = math.ceil(paginates.total / per_page)
    # post = Post.query.all()
    # posts = []
    # for p in post:
    # posts.append({'author':p.author,'title':p.title,'body':p.body})
    # return render_template('index.html',title='我的',user=user,posts=posts,article=posts)

    return render_template('index.html',
                           title='我的',
                           posts=posts,
                           user=user,
                           paginate=paginates,
                           totalpage=totalpage
                           )



@app.route('/login', methods=['GET', 'POST'])
def login():
    # 判断当前用户是否验证，如果通过的话返回首页
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    # 创建表单实例
    form = LoginForm()
    # 对表格数据进行验证 validate_on_submit 等价于   request.method==' post '  and  from.validate()
    if form.validate_on_submit():
        # 根据表格里的数据进行查询，如果查询到数据返回User对象，否则返回None
        user = User.query.filter_by(username=form.username.data).first()
        # 判断用户不存在或者密码不正确
        if user is None:
            # 如果用户不存在

            return redirect(url_for('login'))
        elif not user.check_password(form.password.data):
            # 如果密码不正确
            flash('密码错误')
            # 然后重定向到登录页面
            return redirect(url_for('login'))
        # 这是一个非常方便的方法，当用户名和密码都正确时来解决记住用户是否记住登录状态的问题
        # 调用Flask-Login的login_user()函数，把用户标记为已登录。如果第二个参数（form.remember_me.data）为True，
        # 那么会在用户浏览器中写入一个长期有效的cookies，关闭浏览器再打开也是登录状态；
        # 为False，则直接关闭浏览器用户会话就过期，再访问需要重新登录。
        login_user(user, remember=form.remember_me.data)
        # 此时的next_page记录的是跳转至登录页面是的地址
        next_page = request.args.get('next')
        # 如果next_page记录的地址不存在那么就返回首页
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='登录', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    # 判断当前用户是否验证，如果通过的话返回首页
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data,
                    user_avatar='noavatar_big.gif')
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('恭喜你成为我们网站的新用户!')
        return redirect(url_for('login'))
    return render_template('register.html', title='发布新话题', form=form)


@app.route('/user/<username>/')
@login_required
def user(username):
    # .first_or_404() 当查询结果不存在时，会主动抛出异常，跳转到Flask默认的404页面
    user = User.query.filter_by(username=username).first_or_404()
    # post = Post.query.filter_by(user_id=user.id).all()
    # posts = []
    # for p in post:
    # posts.append({'author':user, 'title':p.title,'body':p.body})
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('perpage', 3))
    # context = {
    paginates = Post.query.filter_by(user_id=user.id).order_by('timestamp').paginate(page, per_page, error_out=True)
    # }
    posts = paginates.items
    totalpage = math.ceil(paginates.total / per_page)

    return render_template('user.html',
                           user=user,
                           posts=posts,
                           paginate=paginates,
                           totalpage=totalpage)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    # 对表格数据进行验证 validate_on_submit 等价于   request.method==' post '  and  from.validate()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        # 性别选择
        gender = ['男', '女', '保密']
        current_user.gender = gender[form.tag.data-1]
        db.session.commit()
        return redirect(url_for('user', username=current_user.username))
    # 填充字段
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='个人资料编辑', form=form)


@app.route('/edit_avatar', methods=['GET', 'POST'])
def edit_avatar():
    form = AvatarForm()
    if form.validate_on_submit():
        print('???')
        f = form.avatar.data
        print(f)
        filename = f.filename
        print(filename)
        upfile = os.getcwd()+('/app/static/avatar/')
        f.save('{}{}{}'.format(upfile,current_user.username,filename))
        current_user.user_avatar = ('{}{}'.format(current_user.username,filename))
        db.session.commit()

        return redirect(url_for('user', username=current_user.username))
    print('falske')
    return render_template('edit_avatar.html', form=form)

@app.route('/post/', methods=['GET', 'POST'])
@login_required
def post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        category = form.tag.choices[form.tag.data-1][1]
        newpost = Post(title=title, body=body, author=current_user, category=category, count=0, reply=0)
        db.session.add(newpost)
        db.session.commit()
        flash('发布成功!')
        return redirect(url_for('article',article_id=newpost.id))
    return render_template('NewPost.html', title='注册', form=form)


@app.route('/article/<article_id>/', methods=['GET', 'POST'])
@login_required
def article(article_id):
    article = Post.query.filter_by(id=article_id).first_or_404()
    comment = Comment.query.filter_by(post_id=article_id)
    # 获取当前页数
    page = int(request.args.get('page', 1))
    # 获取每页显示数据
    per_page = int(request.args.get('perpage', 3))

    paginates = comment.paginate(page, per_page, error_out=False)
    comments = paginates.items
    # 总页数
    totalpage = math.ceil(paginates.total / per_page)

    form = CommentForm()
    print('article')
    if form.validate_on_submit():
        print(article)
        body = form.body.data
        newcomment = Comment(body=body, author=current_user, article=article)
        db.session.add(newcomment)
        db.session.commit()

        flash('评论成功')
        return redirect(url_for('article',article_id=newcomment.article.id))

    return render_template('article.html',
                           article=article,
                           user=article.author,
                           form=form,
                           comments=comments,
                           paginate=paginates,
                           totalpage=totalpage)


# 在请求之前做出响应
@app.before_request
def get_last_time():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
