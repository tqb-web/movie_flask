import sqlite3

from flask import render_template, request, jsonify, Blueprint
from flask_login import login_required

compare_bp = Blueprint('compare', __name__)


@compare_bp.route('/movieCompare')
@login_required
def movieCompare():
    return render_template("movieCompare.html")


# 定义获取所有电影的路由
@compare_bp.route("/get_all_movies", methods=["POST", "GET"])
def get_all_movies():
    conn = sqlite3.connect("database/pythonMovie.db")
    cur = conn.cursor()
    cur.execute("SELECT movie_id,movie_cname FROM pythonMovie limit 100")
    movies = [{'movie_id': row[0], 'movie_cname': row[1]} for row in cur.fetchall()]
    conn.close()
    return jsonify({'movies': movies})


# 定义获取所有导演的路由
@compare_bp.route("/get_all_directors", methods=["POST", "GET"])
def get_all_directors():
    conn = sqlite3.connect("database/pythonMovie.db")
    cur = conn.cursor()
    cur.execute("SELECT director_id,director_name FROM directors where movie_nums>=3 limit 100")
    directors = [{'director_id': row[0], 'director_name': row[1]} for row in cur.fetchall()]
    conn.close()
    return jsonify({'directors': directors})


# 定义获取所有演员的路由
@compare_bp.route("/get_all_actors", methods=["POST", "GET"])
def get_all_actors():
    conn = sqlite3.connect("database/pythonMovie.db")
    cur = conn.cursor()
    cur.execute("SELECT actor_id,actor_name FROM actors where movie_nums>=5 limit 100")
    actors = [{'actor_id': row[0], 'actor_name': row[1]} for row in cur.fetchall()]
    conn.close()
    return jsonify({'actors': actors})


# 定义对比两个电影的路由
@compare_bp.route("/compare_movies", methods=["POST"])
def compare_movies():
    movie_id_1 = request.form.get("movie_id_1")
    movie_id_2 = request.form.get("movie_id_2")
    conn = sqlite3.connect("database/pythonMovie.db")
    c = conn.cursor()
    # 查询第一个电影的数据
    c.execute("SELECT * FROM pythonMovie WHERE movie_id = ?", (movie_id_1,))
    movie1 = c.fetchone()
    # 查询第二个电影的数据
    c.execute("SELECT * FROM pythonMovie WHERE movie_id = ?", (movie_id_2,))
    movie2 = c.fetchone()
    conn.close()
    # 构造返回数据

    movie1_nums = 0
    movie2_nums = 0
    if movie1 and movie2:
        for i in [4, 5, 9, 10, 13, 14]:
            if movie1[i] > movie2[i]:
                movie1_nums += 1
            elif movie1[i] < movie2[i]:
                movie2_nums += 1
    if not movie1 or not movie2:
        return jsonify({"movie1": {
            "name": '--',
            "score": '--',
            "box_office": '--',
            "type": '--',
            "release_time": '--',
            "comments_nums": '--',
            "evaluation_nums": '--',
            "movieWatched_nums": '--',
            "movieWanttw_nums": '--',
            "moviegreater": '--'
            # 其他数据...
        },
            "movie2": {
                "name": '--',
                "score": '--',
                "box_office": '--',
                "type": '--',
                "release_time": '--',
                "comments_nums": '--',
                "evaluation_nums": '--',
                "movieWatched_nums": '--',
                "movieWanttw_nums": '--',
                "moviegreater": '--'
                # 其他数据...
            }
        })
    data = {
        "movie1": {
            "name": movie1[2],
            "score": movie1[5],
            "box_office": movie1[4],
            "type": movie1[7],
            "release_time": movie1[3],
            "comments_nums": movie1[9],
            "evaluation_nums": movie1[10],
            "movieWatched_nums": movie1[13],
            "movieWanttw_nums": movie1[14],
            "moviegreater": movie1_nums
            # 其他数据...
        },
        "movie2": {
            "name": movie2[2],
            "score": movie2[5],
            "box_office": movie2[4],
            "type": movie2[7],
            "release_time": movie2[3],
            "comments_nums": movie2[9],
            "evaluation_nums": movie2[10],
            "movieWatched_nums": movie2[13],
            "movieWanttw_nums": movie2[14],
            "moviegreater": movie2_nums
            # 其他数据...
        }
    }
    return jsonify(data)


# 定义对比两个导演的路由
@compare_bp.route("/compare_directors", methods=["POST"])
def compare_directors():
    director_id_1 = request.form.get("director_id_1")
    director_id_2 = request.form.get("director_id_2")
    conn = sqlite3.connect("database/pythonMovie.db")
    c = conn.cursor()
    # 查询第一个电影的数据
    c.execute(
        "SELECT director_name, round(avg(movie_score), 1), movie_nums, round(avg(movie_vote)), round(avg(comment)), round(avg(evaluation)), round(avg(movieWatched)), round(avg(movieWanttw)) FROM pythonMovie,directors,movies_director where directors.director_id=movies_director.director_id and movies_director.movie_id=pythonMovie.movie_id and directors.director_id=?",
        (director_id_1,))
    director1 = c.fetchone()
    # 查询第二个电影的数据
    c.execute(
        "SELECT director_name, round(avg(movie_score), 1), movie_nums, round(avg(movie_vote)), round(avg(comment)), round(avg(evaluation)), round(avg(movieWatched)), round(avg(movieWanttw)) FROM pythonMovie,directors,movies_director where directors.director_id=movies_director.director_id and movies_director.movie_id=pythonMovie.movie_id and directors.director_id=?",
        (director_id_2,))
    director2 = c.fetchone()
    conn.close()
    # 构造返回数据

    director1_nums = 0
    director2_nums = 0
    if None not in director1 and None not in director2:
        for i in range(1, 7):
            if director1[i] > director2[i]:
                director1_nums += 1
            elif director1[i] < director2[i]:
                director2_nums += 1
    if None in director1 or None in director2:
        return jsonify({"director1": {
            "name": '--',
            "score": '--',
            "movienums": '--',
            "box_office": '--',
            "comments_nums": '--',
            "evaluation_nums": '--',
            "movieWatched_nums": '--',
            "movieWanttw_nums": '--',
            "directorgreater": '--'
            # 其他数据...
        },
            "director2": {
                "name": '--',
                "score": '--',
                "movienums": '--',
                "box_office": '--',
                "comments_nums": '--',
                "evaluation_nums": '--',
                "movieWatched_nums": '--',
                "movieWanttw_nums": '--',
                "directorgreater": '--'
                # 其他数据...
            }
        })
    data = {
        "director1": {
            "name": director1[0],
            "score": director1[1],
            "movienums": director1[2],
            "box_office": director1[3],
            "comments_nums": director1[4],
            "evaluation_nums": director1[5],
            "movieWatched_nums": director1[6],
            "movieWanttw_nums": director1[7],
            "directorgreater": director1_nums
            # 其他数据...
        },
        "director2": {
            "name": director2[0],
            "score": director2[1],
            "movienums": director2[2],
            "box_office": director2[3],
            "comments_nums": director2[4],
            "evaluation_nums": director2[5],
            "movieWatched_nums": director2[6],
            "movieWanttw_nums": director2[7],
            "directorgreater": director2_nums
            # 其他数据...
        }
    }
    return jsonify(data)


# 定义对比两个演员的路由
@compare_bp.route("/compare_actors", methods=["POST"])
def compare_actors():
    actor_id_1 = request.form.get("actor_id_1")
    actor_id_2 = request.form.get("actor_id_2")
    conn = sqlite3.connect("database/pythonMovie.db")
    c = conn.cursor()
    # 查询第一个电影的数据
    c.execute(
        "SELECT actor_name, round(avg(movie_score), 1), movie_nums, round(avg(movie_vote)), round(avg(comment)), round(avg(evaluation)), round(avg(movieWatched)), round(avg(movieWanttw)) FROM pythonMovie,actors,movies_actor where actors.actor_id=movies_actor.actor_id and movies_actor.movie_id=pythonMovie.movie_id and actors.actor_id=?",
        (actor_id_1,))
    actor1 = c.fetchone()
    # 查询第二个电影的数据
    c.execute(
        "SELECT actor_name, round(avg(movie_score), 1), movie_nums, round(avg(movie_vote)), round(avg(comment)), round(avg(evaluation)), round(avg(movieWatched)), round(avg(movieWanttw)) FROM pythonMovie,actors,movies_actor where actors.actor_id=movies_actor.actor_id and movies_actor.movie_id=pythonMovie.movie_id and actors.actor_id=?",
        (actor_id_2,))
    actor2 = c.fetchone()
    conn.close()
    # 构造返回数据

    actor1_nums = 0
    actor2_nums = 0
    if None not in actor1 and None not in actor2:
        for i in range(1, 7):
            if actor1[i] > actor2[i]:
                actor1_nums += 1
            elif actor1[i] < actor2[i]:
                actor2_nums += 1
    if None in actor1 or None in actor2:
        return jsonify({"actor1": {
            "name": '--',
            "score": '--',
            "movienums": '--',
            "box_office": '--',
            "comments_nums": '--',
            "evaluation_nums": '--',
            "movieWatched_nums": '--',
            "movieWanttw_nums": '--',
            "directorgreater": '--'
            # 其他数据...
        },
            "actor2": {
                "name": '--',
                "score": '--',
                "movienums": '--',
                "box_office": '--',
                "comments_nums": '--',
                "evaluation_nums": '--',
                "movieWatched_nums": '--',
                "movieWanttw_nums": '--',
                "directorgreater": '--'
                # 其他数据...
            }
        })
    data = {
        "actor1": {
            "name": actor1[0],
            "score": actor1[1],
            "movienums": actor1[2],
            "box_office": actor1[3],
            "comments_nums": actor1[4],
            "evaluation_nums": actor1[5],
            "movieWatched_nums": actor1[6],
            "movieWanttw_nums": actor1[7],
            "actorgreater": actor1_nums
            # 其他数据...
        },
        "actor2": {
            "name": actor2[0],
            "score": actor2[1],
            "movienums": actor2[2],
            "box_office": actor2[3],
            "comments_nums": actor2[4],
            "evaluation_nums": actor2[5],
            "movieWatched_nums": actor2[6],
            "movieWanttw_nums": actor2[7],
            "actorgreater": actor2_nums
            # 其他数据...
        }
    }
    return jsonify(data)
