# -*- coding: utf-8 -*-
# @Author : Felix Wang
# @time   : 2018/7/9 21:49

# 初始化文件
from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
import pymysql
import os
from flask_redis import FlaskRedis
app = Flask(__name__)

# 用于连接数据的数据库。
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:felixwang@127.0.0.1:3306/movie"
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:tp158917@127.0.0.1:3306/movie"
# 如果设置成 True (默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

# 文件上传路径
app.config['UP_DIR']=os.path.join(os.path.abspath(os.path.dirname(__file__)),'static/uploads/')
app.config["FC_DIR"] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/users/")

app.config["REDIS_URL"] = "redis://127.0.0.1:6379/0"


app.debug = True
app.config['SECRET_KEY']='abcdefg'

db = SQLAlchemy(app)  # 创建数据库
rd = FlaskRedis(app)

# 导入蓝图模块
from app.home import home as home_blueprint
from app.admin import admin as admin_blueprint

# 注册蓝图
# 区分路由,因为两个路由都是/index
app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint, url_prefix='/admin')  # 添加添加路由


@app.errorhandler(404)
def page_not_found(error):
    """
    404
    """
    return render_template("home/404.html"), 404