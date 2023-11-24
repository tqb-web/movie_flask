# 导入必要的库
import sqlite3

import jieba
from flask import Flask, send_file
from flask import render_template, redirect, url_for
from flask_cors import CORS
from flask_login import LoginManager, logout_user, login_required, current_user

from charts import charts_bp
from compare import compare_bp
from movies import movies_bp
from movies_score import movies_score_bp
from sentiment import sentiment_bp
from signup_login import signup_login_bp
from user import User
from user_validation import user_validation_bp
from wordcloud import wordcloud_bp
from other_functions import other_functions_bp

# 创建 Flask 应用
app = Flask(__name__)
jieba.load_userdict('./selfDefiningTxt.txt')

# 允许所有域名访问
CORS(app)

# 设置 Flask 应用的密钥和登录管理器
app.secret_key = 'tianqingbin'
login_manager = LoginManager()
login_manager.init_app(app)

# 注册蓝图
app.register_blueprint(signup_login_bp)
app.register_blueprint(user_validation_bp)
app.register_blueprint(movies_bp)
app.register_blueprint(movies_score_bp)
app.register_blueprint(charts_bp)
app.register_blueprint(wordcloud_bp)
app.register_blueprint(sentiment_bp)
app.register_blueprint(compare_bp)
app.register_blueprint(other_functions_bp)


# 首页路由
@app.route("/")
def home():
    return render_template("login.html")


@app.route('/logout', methods=['POST', 'PUT'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/get_avatar')
@login_required
def get_avatar():
    return send_file(f"static/assets/avatar/avatar_{current_user.id}.png")


@app.route('/index')
@login_required
def index():
    def query_database(sql, *params):
        con = sqlite3.connect('database/pythonMovie.db')
        cur = con.cursor()
        cur.execute(sql, params)
        result = cur.fetchall()
        cur.close()
        con.close()
        return result

    # 查询电影数据
    movie_data = query_database('SELECT * FROM pythonMovie')

    # 查询登录次数数据
    login_data = query_database('SELECT date, count FROM login_times WHERE userId = ?', current_user.userid)
    login_data_list = [list(item) for item in login_data]

    return render_template("index.html", nums=len(movie_data), userId=current_user.userid, data=login_data_list)


@app.route('/team')
@login_required
def team():
    return render_template("team.html")


@app.route('/aboutMe')
@login_required
def aboutMe():
    return render_template("aboutMe.html")


@login_manager.user_loader
def load_user(user_id):
    # 连接用户信息数据库
    conn = sqlite3.connect('database/userInfo.db')
    c = conn.cursor()
    # 查询用户信息
    c.execute('SELECT * FROM usertable WHERE id = ?', (user_id,))
    result = c.fetchone()
    # 关闭数据库连接
    c.close()
    conn.close()
    if result:
        # 创建 User 对象，并传入必要的参数
        user = User(result[0], result[1])
        user.email = result[3]
        user.phone = result[4]
        user.gender = result[5]
        user.register_time = result[6]
        user.hobby = result[7]
        user.is_admin = result[8]
        return user
    else:
        return None


# 数据合并函数
def combine(keys, values):
    res = []

    if len(keys) != len(values):
        return None
    for ind, key in enumerate(keys):
        dict_temp = {}

        dict_temp[key] = values[ind]
        res.append(dict_temp)
    return res


def mycombine(key, value):
    data = {}
    # keys与values分别为该数据的键数组，值的数组。这里循环为字典添加对应键值
    for k, v in zip(key, value):
        data.update({k: v, }, )
    # 最后将数据打包成json格式以字典的方式传送到前端
    # return render(request, 'index.html', {'data': json.dumps(data)})
    return data


if __name__ == '__main__':
    app.run()
