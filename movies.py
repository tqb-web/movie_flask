from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required
import sqlite3

movies_bp = Blueprint('movies', __name__)


@movies_bp.route('/movie')
@login_required
def movie():
    return render_template("movie.html")


@movies_bp.route('/get_movies_data', methods=['POST', 'PUT', 'GET'])
def get_movies_data():
    # 获取电影数据并将其以JSON格式返回
    con = sqlite3.connect("database/pythonMovie.db")
    cur = con.cursor()
    sql = "select * from pythonMovie"
    rows = cur.execute(sql)

    i = 1
    movies = []
    for row in rows:
        movie = {
            'id': i,
            'name': row[2],
            'year': row[3],
            'vote': row[4],
            'score': row[5],
            'link': row[6],
            'category': row[7],
            'country': row[8],
            'comment': row[9],
            'evaluation': row[10]
        }
        i = i + 1
        movies.append(movie)
    # 关闭游标和连接
    cur.close()
    con.close()
    movies_data = {'movies': movies}
    return jsonify(movies_data)


@movies_bp.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    return render_template("search.html")


@movies_bp.route('/search_results', methods=['GET', 'POST'])
@login_required
def search_results():
    # 从查询字符串参数中获取搜索条件
    keyword = request.args.get('keyword')
    category = request.args.get('category')
    movie_score = request.args.get('movie_score')
    movie_vote = request.args.get('movie_vote')
    movie_year = request.args.get('movie_year')
    country = request.args.get('country')
    limit = request.args.get('limit')
    conn = sqlite3.connect('database/pythonMovie.db')
    cursor = conn.cursor()
    query = "SELECT * FROM pythonMovie WHERE (movie_cname LIKE ? OR director LIKE ? OR movieSummary LIKE ? OR actors LIKE ?)"
    params = ('%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%')

    if category:
        query += " AND category LIKE ?"
        params += ('%' + category + '%',)

    if movie_score:
        query += " AND movie_score >= ?"
        params += (movie_score,)

    if movie_vote:
        query += " AND movie_vote >= ?"
        params += (movie_vote,)

    if movie_year:
        query += " AND movie_year LIKE ?"
        params += ('%' + movie_year + '%',)

    if country:
        query += " AND country LIKE ?"
        params += ('%' + country + '%',)

    query += " LIMIT ?"
    params += (limit,)

    movies = cursor.execute(query, params).fetchall()

    cursor.close()
    conn.close()
    return jsonify(movies)
