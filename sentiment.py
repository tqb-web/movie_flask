from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
import sqlite3

sentiment_bp = Blueprint('sentiment', __name__)


@sentiment_bp.route('/sentiment')
@login_required
def sentiment():
    return render_template("sentiment.html")


@sentiment_bp.route('/analyze_sentiment', methods=['POST'])
@login_required
def analyze_sentiment():
    # 获取前端传入的电影名
    movie_name = request.form.get('movie_name')

    # 连接数据库并查询电影评论
    con = sqlite3.connect('database/pythonMovie.db')
    cur = con.cursor()
    cur.execute('select movie_id from pythonMovie where movie_cname=?', (movie_name,))
    result = cur.fetchone()
    if result is not None:
        movie_id = result[0]
    else:
        movie_id = 1

    con.close()

    con = sqlite3.connect('database/sentiment.db')
    cur = con.cursor()
    cur.execute('select positive_count,neutral_count,negative_count from comments_sentiment where movie_id = ?',
                (movie_id,))
    data = cur.fetchone()

    # 对评论进行情感分析并统计情感得分区间
    positive_count = 0
    neutral_count = 0
    negative_count = 0
    if data:
        positive_count = data[0]
        neutral_count = data[1]
        negative_count = data[2]

    cur.execute(
        'select comments_ave_score,comments_max_score,comments_min_score from sentiment_score where movie_id = ?',
        (movie_id,))
    comments_data = cur.fetchone()

    comments_ave_score = 0
    comments_max_score = 0
    comments_min_score = 0

    if comments_data:
        comments_ave_score = comments_data[0]
        comments_max_score = comments_data[1]
        comments_min_score = comments_data[2]

    # 构建返回给前端的数据
    result = {
        'positive_count': positive_count,
        'neutral_count': neutral_count,
        'negative_count': negative_count,
        'comments_ave_score': comments_ave_score,
        'comments_max_score': comments_max_score,
        'comments_min_score': comments_min_score
    }
    con.close()
    return jsonify(result)


@sentiment_bp.route('/reviews_analyze_sentiment', methods=['POST'])
@login_required
def reviews_analyze_sentiment():
    # 获取前端传入的电影名
    movie_name = request.form.get('movie_name')

    # 连接数据库并查询电影评论
    con = sqlite3.connect('database/pythonMovie.db')
    cur = con.cursor()
    cur.execute('select movie_id from pythonMovie where movie_cname=?', (movie_name,))
    result = cur.fetchone()
    if result is not None:
        movie_id = result[0]
    else:
        movie_id = 1
    con.close()

    con = sqlite3.connect('database/sentiment.db')
    cur = con.cursor()
    cur.execute('select positive_count,neutral_count,negative_count from reviews_sentiment where movie_id = ?',
                (movie_id,))
    data = cur.fetchone()

    # 对评论进行情感分析并统计情感得分区间
    positive_count = 0
    neutral_count = 0
    negative_count = 0

    if data:
        positive_count = data[0]
        neutral_count = data[1]
        negative_count = data[2]

    cur.execute('select reviews_ave_score,reviews_max_score,reviews_min_score from sentiment_score where movie_id = ?',
                (movie_id,))
    reviews_data = cur.fetchone()

    reviews_ave_score = 0
    reviews_max_score = 0
    reviews_min_score = 0

    if reviews_data:
        reviews_ave_score = reviews_data[0]
        reviews_max_score = reviews_data[1]
        reviews_min_score = reviews_data[2]

    con.close()

    # 构建返回给前端的数据
    result = {
        'positive_count': positive_count,
        'neutral_count': neutral_count,
        'negative_count': negative_count,
        'reviews_ave_score': reviews_ave_score,
        'reviews_max_score': reviews_max_score,
        'reviews_min_score': reviews_min_score
    }

    return jsonify(result)


@sentiment_bp.route('/bar_analyze_sentiment', methods=['POST', 'GET'])
@login_required
def bar_analyze_sentiment():
    # 获取前端传入的电影名
    movie_name = request.form.get('movie_name')
    # 连接数据库并查询电影评论
    con = sqlite3.connect('database/pythonMovie.db')
    cur = con.cursor()
    cur.execute('select movie_id from pythonMovie where movie_cname=?', (movie_name,))
    result = cur.fetchone()
    if result is not None:
        movie_id = result[0]
    else:
        movie_id = 1
    con.close()

    con = sqlite3.connect('database/sentiment.db')
    cur = con.cursor()
    cur.execute(
        'select positive_count,neutral_count,negative_count,very_positive_count,very_negative_count from bar_comments_sentiment where movie_id = ?',
        (movie_id,))
    data = cur.fetchone()

    # 对评论进行情感分析并统计情感得分区间
    positive_count = 0
    neutral_count = 0
    negative_count = 0
    very_positive_count = 0
    very_negative_count = 0

    if data:
        positive_count = data[0]
        neutral_count = data[1]
        negative_count = data[2]
        very_positive_count = data[3]
        very_negative_count = data[4]

    con.close()

    # 构建返回给前端的数据
    result = {
        'positive_count': positive_count,
        'neutral_count': neutral_count,
        'negative_count': negative_count,
        'very_positive_count': very_positive_count,
        'very_negative_count': very_negative_count
    }
    # print(result)

    return jsonify(result)


@sentiment_bp.route('/bar_reviews_analyze_sentiment', methods=['POST', 'GET'])
@login_required
def bar_reviews_analyze_sentiment():
    # 获取前端传入的电影名
    movie_name = request.form.get('movie_name')
    # 连接数据库并查询电影评论
    con = sqlite3.connect('database/pythonMovie.db')
    cur = con.cursor()
    cur.execute('select movie_id from pythonMovie where movie_cname=?', (movie_name,))
    result = cur.fetchone()
    if result is not None:
        movie_id = result[0]
    else:
        movie_id = 1
    con.close()

    con = sqlite3.connect('database/sentiment.db')
    cur = con.cursor()
    cur.execute(
        'select positive_count,neutral_count,negative_count,very_positive_count,very_negative_count from bar_reviews_sentiment where movie_id = ?',
        (movie_id,))
    data = cur.fetchone()

    # 对评论进行情感分析并统计情感得分区间
    positive_count = 0
    neutral_count = 0
    negative_count = 0
    very_positive_count = 0
    very_negative_count = 0

    if data:
        positive_count = data[0]
        neutral_count = data[1]
        negative_count = data[2]
        very_positive_count = data[3]
        very_negative_count = data[4]

    con.close()

    # 构建返回给前端的数据
    result = {
        'positive_count': positive_count,
        'neutral_count': neutral_count,
        'negative_count': negative_count,
        'very_positive_count': very_positive_count,
        'very_negative_count': very_negative_count
    }
    # print(result)

    return jsonify(result)
