import os
from flask import session
from flask import render_template
from functools import wraps

# 保存用户头像
def save_avatar(nickname,avatar_file):
    base_dir = os.path.dirname(os.path.abspath(__name__))
    file_path = os.path.join(base_dir,'upload',nickname)
    avatar_file.save(file_path)

def login_required(view_func):
    '''登录验证装饰器'''
    @wraps(view_func)
    def check(*args,**kwargs):
        if 'uid' in session:
            return view_func(*args,**kwargs)
        else:
            return render_template('login.html',error='请先登录')
    return check