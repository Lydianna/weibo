#!/usr/bin/env python
import os
from flask import Flask
from flask import render_template
from flask import redirect
from libs.db import db


app = Flask(__name__)
#初始化数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:19970111@localhost/weibo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = 'M\xd2\x16\xa0K\x01\x0f@\x9f(\xab2V\xd7\xe3\x00'
db.init_app(app)


@app.route('/')
def home():
    return redirect('/weibo/')

if __name__ == '__main__':
    from user import user_bp
    app.register_blueprint(user_bp, url_prefix='/user')

    from weibo import weibo_bp
    app.register_blueprint(weibo_bp,url_prefix='/weibo')
    app.debug = True
    app.run()