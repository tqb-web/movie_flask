# 导入所需的模块和类
from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required
import sqlite3

# 创建图表的 Blueprint
charts_bp = Blueprint('charts', __name__)


# 定义详细图表的路由
@charts_bp.route('/detailed_charts')
@login_required
def detailed_charts():
    return render_template("detailed_charts.html")


@charts_bp.route('/get_chart_data', methods=['POST'])
@login_required
def get_chart_data():
    year = request.form['year']
    category = request.form['category']
    top_num = request.form['top_num']

    # 从数据库中获取电影数据
    conn = sqlite3.connect('database/pythonMovie.db')
    c = conn.cursor()
    if category == 'box_office':
        c.execute(
            'SELECT movie_cname, movie_vote FROM pythonMovie WHERE movie_year LIKE ? ORDER BY movie_vote DESC LIMIT ?',
            (year + '%', top_num))
        movie_data = c.fetchall()
    elif category == 'score':
        c.execute(
            'SELECT movie_cname, movie_score FROM pythonMovie WHERE movie_year LIKE ? ORDER BY movie_score DESC LIMIT ?',
            (year + '%', top_num))
        movie_data = c.fetchall()
    elif category == 'num_comments':
        c.execute('SELECT movie_cname, comment FROM pythonMovie WHERE movie_year LIKE ? ORDER BY comment DESC LIMIT ?',
                  (year + '%', top_num))
        movie_data = c.fetchall()
    elif category == 'num_ratings':
        c.execute(
            'SELECT movie_cname, evaluation FROM pythonMovie WHERE movie_year LIKE ? ORDER BY evaluation DESC LIMIT ?',
            (year + '%', top_num))
        movie_data = c.fetchall()
    elif category == 'num_watched':
        c.execute(
            'SELECT movie_cname, movieWatched FROM pythonMovie WHERE movie_year LIKE ? ORDER BY movieWatched DESC LIMIT ?',
            (year + '%', top_num))
        movie_data = c.fetchall()
    elif category == 'num_wanted':
        c.execute(
            'SELECT movie_cname, movieWanttw FROM pythonMovie WHERE movie_year LIKE ? ORDER BY movieWanttw DESC LIMIT ?',
            (year + '%', top_num))
        movie_data = c.fetchall()
    else:
        movie_data = []

    c.close()
    conn.close()

    movie_chart_data = []
    for movie in movie_data:
        movie_chart_data.append({'value': movie[1], 'name': movie[0]})
    return jsonify(movie_chart_data)


@charts_bp.route('/get_chart_data_line', methods=['POST'])
@login_required
def get_chart_data_line():
    yearFrom = request.form['yearFrom']
    yearTo = request.form['yearTo']
    category = request.form['category']
    select_type = request.form['type']

    # 从数据库中获取电影数据
    conn = sqlite3.connect('database/pythonMovie.db')
    c = conn.cursor()

    if category == 'box_office':
        if select_type == 'total-value':
            c.execute(
                "SELECT substr(movie_year,1,4), sum(movie_vote) FROM pythonMovie WHERE substr(movie_year,1,4) >=? and substr(movie_year,1,4)<=? group by substr(movie_year,1,4)",
                (yearFrom, yearTo))
        else:
            c.execute(
                "SELECT substr(movie_year,1,4), avg(movie_vote) FROM pythonMovie WHERE substr(movie_year,1,4) >=? and substr(movie_year,1,4)<=? and movie_vote!=0 group by substr(movie_year,1,4)",
                (yearFrom, yearTo))
        movie_data = c.fetchall()
    elif category == 'num_comments':
        if select_type == 'total-value':
            c.execute(
                "SELECT substr(movie_year,1,4), sum(comment) FROM pythonMovie WHERE substr(movie_year,1,4) >=? and substr(movie_year,1,4)<=? group by substr(movie_year,1,4)",
                (yearFrom, yearTo))
        else:
            c.execute(
                "SELECT substr(movie_year,1,4), avg(comment) FROM pythonMovie WHERE substr(movie_year,1,4) >=? and substr(movie_year,1,4)<=? and comment!=0 group by substr(movie_year,1,4)",
                (yearFrom, yearTo))
        movie_data = c.fetchall()
    elif category == 'num_ratings':
        if select_type == 'total-value':
            c.execute(
                "SELECT substr(movie_year,1,4), sum(evaluation) FROM pythonMovie WHERE substr(movie_year,1,4) >=? and substr(movie_year,1,4)<=? group by substr(movie_year,1,4)",
                (yearFrom, yearTo))
        else:
            c.execute(
                "SELECT substr(movie_year,1,4), avg(evaluation) FROM pythonMovie WHERE substr(movie_year,1,4) >=? and substr(movie_year,1,4)<=? and evaluation!=0 group by substr(movie_year,1,4)",
                (yearFrom, yearTo))
        movie_data = c.fetchall()
    elif category == 'num_watched':
        if select_type == 'total-value':
            c.execute(
                "SELECT substr(movie_year,1,4), sum(movieWatched) FROM pythonMovie WHERE substr(movie_year,1,4) >=? and substr(movie_year,1,4)<=? group by substr(movie_year,1,4)",
                (yearFrom, yearTo))
        else:
            c.execute(
                "SELECT substr(movie_year,1,4), avg(movieWatched) FROM pythonMovie WHERE substr(movie_year,1,4) >=? and substr(movie_year,1,4)<=? and movieWatched!=0 group by substr(movie_year,1,4)",
                (yearFrom, yearTo))
        movie_data = c.fetchall()
    elif category == 'num_wanted':
        if select_type == 'total-value':
            c.execute(
                "SELECT substr(movie_year,1,4), sum(movieWanttw) FROM pythonMovie WHERE substr(movie_year,1,4) >=? and substr(movie_year,1,4)<=? group by substr(movie_year,1,4)",
                (yearFrom, yearTo))
        else:
            c.execute(
                "SELECT substr(movie_year,1,4), avg(movieWanttw) FROM pythonMovie WHERE substr(movie_year,1,4) >=? and substr(movie_year,1,4)<=? and movieWanttw!=0 group by substr(movie_year,1,4)",
                (yearFrom, yearTo))
        movie_data = c.fetchall()
    else:
        movie_data = []

    # print(movie_data)

    c.close()
    conn.close()

    return jsonify(movie_data)


@charts_bp.route('/get_chart_data_month', methods=['POST'])
@login_required
def get_chart_data_month():
    year = request.form['year']
    # 从数据库中获取电影数据
    conn = sqlite3.connect('database/pythonMovie.db')
    c = conn.cursor()
    c.execute(
        'SELECT substr(movie_year,6,2), count(*), sum(movie_vote), sum(comment), sum(evaluation) FROM pythonMovie WHERE movie_year LIKE ? group BY substr(movie_year,6,2)',
        (year + '%',))
    movie_data = c.fetchall()
    c.close()
    conn.close()
    # print(movie_data)
    return jsonify(movie_data)


@charts_bp.route('/get_chart_data_people', methods=['POST'])
@login_required
def get_chart_data_people():
    people = request.form['people']
    category = request.form['category']
    type = request.form['type']
    top_num = request.form['top_num']
    conn = sqlite3.connect('database/pythonMovie.db')
    c = conn.cursor()

    if people == 'director':
        if category == 'movie_nums':
            c.execute('select director_name, movie_nums from directors order by movie_nums desc limit ?', (top_num,))
            people_data = c.fetchall()
        elif category == 'movie_score':
            c.execute(
                'select director_name, avg(movie_score) from directors,movies_director,pythonMovie where directors.director_id=movies_director.director_id and movies_director.movie_id=pythonMovie.movie_id group by director_name order by avg(movie_score) desc limit ?',
                (top_num,))
            people_data = c.fetchall()
        else:
            if type == 'total-value':
                c.execute(
                    f'select director_name, sum({category}) from directors,movies_director,pythonMovie where directors.director_id=movies_director.director_id and movies_director.movie_id=pythonMovie.movie_id group by director_name order by sum({category}) desc limit {top_num}'
                )
                people_data = c.fetchall()
            else:
                c.execute(
                    f'select director_name, avg({category}) from directors,movies_director,pythonMovie where directors.director_id=movies_director.director_id and movies_director.movie_id=pythonMovie.movie_id group by director_name order by avg({category}) desc limit {top_num}'
                )
                people_data = c.fetchall()
    else:
        if category == 'movie_nums':
            c.execute('select actor_name, movie_nums from actors order by movie_nums desc limit ?', (top_num,))
            people_data = c.fetchall()
        elif category == 'movie_score':
            c.execute(
                'select actor_name, avg(movie_score) from actors,movies_actor,pythonMovie where actors.actor_id=movies_actor.actor_id and movies_actor.movie_id=pythonMovie.movie_id group by actor_name order by avg(movie_score) desc limit ?',
                (top_num,))
            people_data = c.fetchall()
        else:
            if type == 'total-value':
                c.execute(
                    f'select actor_name, sum({category}) from actors,movies_actor,pythonMovie where actors.actor_id=movies_actor.actor_id and movies_actor.movie_id=pythonMovie.movie_id group by actor_name order by sum({category}) desc limit {top_num}'
                )
                people_data = c.fetchall()
            else:
                c.execute(
                    f'select actor_name, avg({category}) from actors,movies_actor,pythonMovie where actors.actor_id=movies_actor.actor_id and movies_actor.movie_id=pythonMovie.movie_id and actors.movie_nums>5 group by actor_name order by avg({category}) desc limit {top_num}'
                )
                people_data = c.fetchall()

    people_chart_data = []
    for people in people_data:
        people_chart_data.append({'value': people[1], 'name': people[0]})
    return jsonify(people_chart_data)
