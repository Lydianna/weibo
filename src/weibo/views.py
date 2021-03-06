import datetime

from math import ceil
from flask  import Blueprint
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import abort

from .models import Weibo
from user.logic import login_required
from libs.db import db
from user.models import User

weibo_bp = Blueprint('weibo',import_name='weibo')
weibo_bp.template_folder = './templates'

@weibo_bp.route('/')
@weibo_bp.route('/index')
def index():
    '''显示最新的前 50 条微博'''
    # 获取微博数据
    page = int(request.args.get('page', 1))
    n_per_page = 10
    offset = (page - 1) * n_per_page
    # 当前页要显示的微博
    # select * from weibo order by updated desc limit 10 offset 20;
    wb_list = Weibo.query.order_by(Weibo.updated.desc()).limit(10).offset(offset)
    n_weibo = Weibo.query.count()  # 微博总数
    n_page = 5 if n_weibo >= 50 else ceil(n_weibo / n_per_page)  # 总页数

    # 获取微博对应的作者
    uid_list = {wb.uid for wb in wb_list}  # 取出微博对应的用户 ID
    # select id, nickname from user id in ...;
    users = dict(User.query.filter(User.id.in_(uid_list)).values('id', 'nickname'))
    return render_template('index.html', page=page, n_page=n_page, wb_list=wb_list, users=users)



@weibo_bp.route('/post',methods=('POST','GET'))
@login_required
def post():
    if request.method == 'POST':
        content = request.form.get('content').strip()
        if not content:
            return render_template('post.html',error='微博内容不允许为空')
        else:
            weibo = Weibo(uid=session['uid'],content=content)
            weibo.updated = datetime.datetime.now()
            db.session.add(weibo)
            db.session.commit()
            return redirect('/weibo/show?wid=%s' % weibo.id)
    else:
        return render_template('post.html')


@weibo_bp.route('/edit')
@login_required
def edit():
    if request.method == 'POST':
        wid = int(request.form.get('wid'))
        content = request.form.get('content').strip()
        if not content:
            return render_template('post.html',error='微博内容不允许为空')
        else:
            weibo =Weibo.query.get(wid)
            if weibo.uid != session['uid']:
                abort(403)
            weibo.content = content
            weibo.updated = datetime.datetime.now()
            db.session.add(weibo)
            db.session.commit()
            return redirect('/weibo/show?wid=%s' % weibo.id)
    else:
        wid = request.args.get('wid')
        weibo = Weibo.query.get(wid)
        return render_template('edit.html', weibo=weibo)


@weibo_bp.route('/show')
def show():
    wid = int(request.args.get('wid'))
    weibo = Weibo.query.get(wid)
    if weibo is None:
        abort(404)
    else:
        user = User.query.get(weibo.uid)
        return render_template('show.html',weibo=weibo,user=user)


@weibo_bp.route('/delete')
@login_required
def delete():
    wid = int(request.args.get('wid'))
    Weibo.query.filter_by(id=wid).delete()
    db.session.commit()
    return redirect('/')
