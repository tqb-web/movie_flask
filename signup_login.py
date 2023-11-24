import os

from PIL import Image
from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, current_user
import sqlite3
import datetime
from flask import current_app
from user import User

signup_login_bp = Blueprint('signup_login', __name__)


@signup_login_bp.route('/register', methods=["POST"])
def register():
    db = sqlite3.connect("database/userInfo.db")
    username = request.form["username"]
    password = request.form["r_password"]
    cpassword = request.form["cpassword"]
    hashed_password = generate_password_hash(password)
    cursor = db.cursor()
    sql = "SELECT * FROM usertable WHERE username=?"
    params = (username,)
    cursor.execute(sql, params)
    user = cursor.fetchone()
    is_admin = 0
    if user or (password != cpassword):
        error_message = "注册失败，请按要求填写！"
        return render_template("login.html", error=error_message)
    else:
        query = "INSERT INTO usertable (username, password, is_admin) VALUES (?, ?, ?)"
        params = (username, hashed_password, is_admin)
        cursor.execute(query, params)
        query = "SELECT id FROM usertable WHERE username=?"
        params = (username,)
        cursor.execute(query, params)
        user_id = cursor.fetchone()[0]
        default_avatar_path = os.path.join(current_app.static_folder, "assets", "avatar", "avatar_default.png")
        default_avatar = Image.open(default_avatar_path)
        new_avatar_filename = "avatar_{}.png".format(user_id)
        new_avatar_path = os.path.join(current_app.static_folder, "assets", "avatar", new_avatar_filename)
        default_avatar.save(new_avatar_path)
        db.commit()
        db.close()
        error_message = "注册成功，请登录！"
        return render_template("login.html", error=error_message)


@signup_login_bp.route('/login', methods=['GET', 'POST'])
def login():
    db = sqlite3.connect("database/userInfo.db")
    username = request.form["username"]
    password = request.form["password"]
    cursor = db.cursor()
    query = "SELECT * FROM usertable WHERE username=?"
    params = (username,)
    cursor.execute(query, params)
    user = cursor.fetchone()
    if user is None:
        error_message = "账号不存在！"
        return render_template("login.html", error=error_message)

    if not check_password_hash(user[2], password):
        error_message = "密码错误，请重试！"
        return render_template("login.html", error=error_message)
    db = sqlite3.connect("database/userInfo.db")
    query = "SELECT id FROM usertable WHERE username=?"
    params = (username,)
    cursor.execute(query, params)
    userid = cursor.fetchone()[0]
    # print(userid)
    user = User(userid, username)
    login_user(user)
    db.close()

    # 获取当前日期
    current_date = datetime.datetime.now().date()
    date_string = current_date.strftime('%Y-%m-%d')

    con = sqlite3.connect('database/pythonMovie.db')
    # 获取cursor对象
    cur = con.cursor()
    # 查询数据库中是否已经存在对应用户ID和日期的记录
    cur.execute('SELECT * FROM login_times WHERE userId = ? AND date = ?', (current_user.userid, date_string))
    row = cur.fetchone()
    if row:
        # 如果记录已存在，则将对应用户ID和日期的登录次数加1
        cur.execute('UPDATE login_times SET count = count + 1 WHERE userId = ? AND date = ?',
                    (current_user.userid, date_string))
        con.commit()
    else:
        # 如果记录不存在，则在数据库中插入一条新记录，用户ID、日期和登录次数初始值为1
        cur.execute('INSERT INTO login_times (userId, date, count) VALUES (?, ?, ?)',
                    (current_user.userid, date_string, 1))
        con.commit()
    # 关闭游标
    cur.close()
    # 关闭连接
    con.close()
    return redirect(url_for('index'))
