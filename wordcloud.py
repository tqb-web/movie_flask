from flask import Blueprint, render_template, request
from flask_login import login_required
import sqlite3
import base64

wordcloud_bp = Blueprint('wordcloud', __name__)


@wordcloud_bp.route('/cloud')
@login_required
def word():
    return render_template("cloud.html")


@wordcloud_bp.route("/generate_wordcloud", methods=["POST"])
def generate_wordcloud():
    movie_name = request.form.get("movie_name")

    # 连接数据库
    con = sqlite3.connect('database/pythonMovie.db')
    cur = con.cursor()
    cur.execute('select movie_id from pythonMovie where movie_cname=?', (movie_name,))
    result = cur.fetchone()
    if result is not None:
        movie_id = result[0]
    else:
        movie_id = 1

    cur.close()
    con.close()

    con = sqlite3.connect('database/cloud.db')
    cur = con.cursor()
    cur.execute('select comments_wordcloud_data,reviews_wordcloud_data from cloud where movie_id=?', (movie_id,))
    data = cur.fetchone()

    if data is not None and data[0] is not None:
        # 获取词云图的二进制数据
        img_data = data[0]
        img_data1 = data[1]

        # 将二进制数据转换为base64格式
        img_base64 = base64.b64encode(img_data).decode("utf-8")
        img_base641 = base64.b64encode(img_data1).decode("utf-8")

        # 构建返回给前端的数据
        result = {
            'wordcloud': '<img src="data:image/png;base64,{}" style="width:100%;">'.format(img_base64),
            'wordcloud1': '<img src="data:image/png;base64,{}" style="width:100%;">'.format(img_base641)
        }

        cur.close()
        con.close()

        # 返回词云图的base64数据给前端
        return result
    else:
        # 数据库中没有词云图数据
        return {"wordcloud": None, "wordcloud1": None}
