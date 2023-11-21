import base64
import io
import os
import sqlite3

from PIL import Image
from flask import render_template, request, jsonify, abort, Blueprint
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from newAnwser import main_ai

other_functions_bp = Blueprint('other_functions', __name__)


@other_functions_bp.route('/answerQuestion')
@login_required
def answerQuestion():
    return render_template("answerQuestion.html", user_id=current_user.id)


@other_functions_bp.route('/historyAnswer')
@login_required
def historyAnswer():
    conn = sqlite3.connect('database/userInfo.db')
    c = conn.cursor()
    c.execute('select * from chatHistory where userId = ?', (current_user.userid,))
    result = c.fetchall()

    # 将查询结果转换成列表
    questions = []
    for row in result:
        questions.append({
            'question': row[2],
            'answer': row[3],
            'time': row[4]
        })
    c.close()
    conn.close()
    return render_template("historyAnswer.html", questions=questions)


@other_functions_bp.route('/execute', methods=['POST'])
def execute():
    code = request.form['message']
    out = main_ai(code)
    conn = sqlite3.connect("database/userInfo.db")
    c = conn.cursor()
    c.execute('INSERT INTO chatHistory (userId, question, answer) VALUES (?, ?, ?)', (current_user.userid, code, out))
    conn.commit()
    c.close()
    conn.close()
    return out


@other_functions_bp.route('/personInfo')
@login_required
def personInfo():
    conn = sqlite3.connect('database/userInfo.db')
    c = conn.cursor()
    c.execute('SELECT * FROM usertable WHERE id=?', (current_user.userid,))
    users = c.fetchone()
    conn.close()
    return render_template("personInfo.html", users=users)


@other_functions_bp.route("/upload_avatar", methods=["POST"])
def upload_avatar():
    # 读取前端传递的Base64编码的字符串，转换为字节流
    image_data = base64.b64decode(request.form['image_data'].split(',')[1])
    if not image_data:
        return jsonify({"success": False, "error": "没有上传文件"})
    # 将字节流转换为图像
    image = Image.open(io.BytesIO(image_data))
    current_user_id = current_user.id
    path = f"static/assets/avatar/avatar_{current_user_id}.png"
    # 保存图像
    image.save(path)
    return jsonify({"success": True})


@other_functions_bp.route('/update1', methods=['POST', 'PUT'])
@login_required
def update1():
    username = request.form['username']
    email = request.form['email']
    phone = request.form['phone']
    gender = request.form['gender']
    hobby = request.form['hobby']
    conn = sqlite3.connect('database/userInfo.db')
    c = conn.cursor()
    c.execute('select * from usertable where username = ? and id != ?', (username, current_user.userid))
    pname = c.fetchone()
    c.execute('select * from usertable where email = ? and id != ?', (email, current_user.userid))
    pemail = c.fetchone()
    c.execute('select * from usertable where phone = ? and id != ?', (phone, current_user.userid))
    pphone = c.fetchone()
    if pname is not None or pemail is not None or pphone is not None:
        message = '修改失败！'
        return jsonify({'message': message})
    c.execute('UPDATE usertable SET username = ?,email = ?,phone = ?,gender = ?,hobby = ? WHERE id = ?',
              (username, email, phone, gender, hobby, current_user.userid))
    conn.commit()
    conn.close()
    message = '修改成功！'
    return jsonify({'message': message})


@other_functions_bp.route('/changepassword', methods=['POST', 'PUT'])
@login_required
def changepassword():
    old_password = request.form['old_password']
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']
    conn = sqlite3.connect('database/userInfo.db')
    c = conn.cursor()
    c.execute('select password from usertable WHERE id = ?', (current_user.userid,))
    hashed_password = c.fetchone()[0]

    if not check_password_hash(hashed_password, old_password):
        message = '原密码错误！'
        return jsonify({'message': message})

    if new_password != confirm_password:
        message = '两次输入的新密码不一致！'
        return jsonify({'message': message})

    new_hashed_password = generate_password_hash(new_password)
    c.execute('UPDATE usertable SET password = ? WHERE id = ?', (new_hashed_password, current_user.userid))
    conn.commit()
    conn.close()

    message = '密码修改成功！'
    return jsonify({'message': message})


@other_functions_bp.route('/reset_password', methods=['POST'])
@login_required
def reset_password():
    conn = sqlite3.connect('database/userInfo.db')
    c = conn.cursor()
    id = request.form['id']
    new_hashed_password = generate_password_hash('h12345678')
    c.execute('UPDATE usertable SET password = ? WHERE id = ?', (new_hashed_password, id))
    conn.commit()
    c.close()
    conn.close()
    message = '密码重置成功！'
    return jsonify({'message': message})


@other_functions_bp.route('/set_admin', methods=['POST'])
@login_required
def set_admin():
    if current_user.userid != 1:
        message = '你没有该权限！'
        return jsonify({'message': message})
    conn = sqlite3.connect('database/userInfo.db')
    c = conn.cursor()
    id = request.form['id']
    c.execute('UPDATE usertable SET is_admin = ? WHERE id = ?', (1, id))
    conn.commit()
    c.close()
    conn.close()
    message = '管理设置成功！'
    return jsonify({'message': message})


@other_functions_bp.route('/cancel_admin', methods=['POST'])
@login_required
def cancel_admin():
    if current_user.userid != 1:
        message = '你没有该权限！'
        return jsonify({'message': message})
    conn = sqlite3.connect('database/userInfo.db')
    c = conn.cursor()
    id = request.form['id']
    c.execute('UPDATE usertable SET is_admin = ? WHERE id = ?', (0, id))
    conn.commit()
    c.close()
    conn.close()
    message = '管理取消成功！'
    return jsonify({'message': message})


@other_functions_bp.route('/delete_user', methods=['POST'])
@login_required
def delete_user():
    if current_user.userid != 1:
        message = '你没有该权限！'
        return jsonify({'message': message})
    conn = sqlite3.connect('database/userInfo.db')
    c = conn.cursor()
    id = request.form['id']
    # 删除用户头像文件
    avatar_path = os.path.join('static', 'assets', 'avatar', 'avatar_{}.png'.format(id))
    if os.path.exists(avatar_path):
        os.remove(avatar_path)
    c.execute('delete from usertable where id = ?', (id,))
    conn.commit()
    c.close()
    conn.close()
    message = '用户删除成功！'
    return jsonify({'message': message})


@other_functions_bp.route('/users')
@login_required
def users():
    if current_user.is_admin != 1:
        abort(403)
    conn = sqlite3.connect('database/userInfo.db')
    c = conn.cursor()
    c.execute('select * from usertable')
    result = c.fetchall()

    # 将查询结果转换成列表
    users = []
    for row in result:
        users.append({
            'id': row[0],
            'username': row[1],
            'email': row[3],
            'phone': row[4],
            'gender': row[5],
            'register_time': row[6],
            'hobby': row[7],
            'is_admin': '是' if row[8] == 1 else '否'
        })
    c.close()
    conn.close()

    return render_template('users.html', users=users)


def get_user_history(id):
    # 假设 user_history 表中保存了用户的历史问答记录，每个记录包含三个字段：question、answer、date
    # 这里使用 SQL 语句从数据库中查询数据
    sql = "SELECT question, answer, timestamp FROM chatHistory WHERE userId = ?"
    conn = sqlite3.connect('database/userInfo.db')
    cur = conn.cursor()
    cur.execute(sql, (id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    # 将查询结果转换为字典列表
    history = [{'question': row[0], 'answer': row[1], 'timestamp': row[2]} for row in rows]
    return history


# 处理 /get_history 路由的请求
@other_functions_bp.route('/get_history', methods=['POST', 'PUT', 'GET'])
@login_required
def get_history():
    id = request.args.get('id')
    # 假设 user 表中保存了用户的信息，每个记录包含四个字段：id、username、email、phone
    # 这里使用 SQL 语句从数据库中查询用户信息
    sql = "SELECT id, username FROM usertable WHERE id = ?"
    conn = sqlite3.connect('database/userInfo.db')
    cur = conn.cursor()
    cur.execute(sql, (id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        # 如果查询到了用户信息，则返回用户的历史问答记录
        history = get_user_history(id)
        return jsonify({'success': True, 'username': row[1], 'history': history})
    else:
        # 如果查询不到用户信息，则返回错误信息
        return jsonify({'success': False, 'message': '用户不存在'})


@other_functions_bp.route('/delete_feedback', methods=['POST'])
@login_required
def delete_feedback():
    feedback_id = request.form.get('feedback_id')
    # print(feedback_id)
    # 连接 SQLite3 数据库
    conn = sqlite3.connect('database/feedback.db')
    c = conn.cursor()

    # 执行 SQL 语句，删除相应的反馈记录
    c.execute('DELETE FROM feedback WHERE id=?', (feedback_id,))

    # 提交事务并关闭数据库连接
    conn.commit()
    conn.close()

    # 返回删除结果给前端
    return jsonify({'success': True})


@other_functions_bp.route('/feedback', methods=['POST'])
@login_required
def handle_feedback():
    subject = request.form.get('subject')
    message = request.form.get('message')

    if subject == "" or message == "":
        message = '信息不能为空!'
        return jsonify({'message': message})

    conn = sqlite3.connect('database/feedback.db')
    c = conn.cursor()
    c.execute("INSERT INTO feedback (userId, userName, subject, message, is_new) VALUES (?, ?, ?, ?,?)",
              (current_user.userid, current_user.username, subject, message, 1))
    conn.commit()
    conn.close()

    message = '反馈成功！'
    return jsonify({'message': message})


# 查看反馈信息
@other_functions_bp.route('/view_feedback', methods=['POST', 'PUT', 'GET'])
@login_required
def view_feedback():
    conn = sqlite3.connect('database/feedback.db')
    c = conn.cursor()
    c.execute('SELECT * FROM feedback ORDER BY timestamp DESC')
    feedbacks = c.fetchall()
    conn.close()
    return render_template('view_feedback.html', feedbacks=feedbacks)


# 查看反馈信息
@other_functions_bp.route('/view_feedback_1/<int:feedback_id>')
@login_required
def view_feedback_1(feedback_id):
    conn = sqlite3.connect('database/feedback.db')
    c = conn.cursor()
    c.execute('SELECT message FROM feedback WHERE id = ?', (feedback_id,))
    message = c.fetchone()[0]
    c.execute('update feedback set is_new = 0 where id = ?', (feedback_id,))
    conn.commit()
    conn.close()
    return jsonify({'content': message})
