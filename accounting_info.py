import re
import sqlite3
from collections import Counter

dbpath = "pythonMovie (2).db"
conn = sqlite3.connect(dbpath)
cursor = conn.cursor()

# 获取所有演员
all_actors = []
all_directors = []
cursor.execute("SELECT actors FROM pythonMovie")
for row in cursor.fetchall():
    actors = row[0].split()
    all_actors.extend(actors)

cursor.execute("SELECT director FROM pythonMovie")
for row in cursor.fetchall():
    directors = row[0].split()
    all_directors.extend(directors)

# 统计演员出现次数
actor_count = Counter(all_actors)
director_count = Counter(all_directors)

actor_id = 1
# 打印出演员出现的次数
for actor, count in actor_count.most_common():
    # 判断演员名是否包含英文字符
    if not re.search('[a-zA-Z]', actor):
        cursor.execute("insert into actors(actor_id,actor_name,movie_nums) values(?,?,?)", (actor_id, actor, count))
        print(f"{actor_id} {actor}: {count}部电影")
        actor_id += 1
        cursor.execute("select movie_id,movie_cname from pythonMovie where actors like ?", ('%' + actor + '%',))
        movies = cursor.fetchall()
        print(movies)
        for movie in movies:
            cursor.execute("insert into movies_actor(movie_id,movie_cname,actor_id) values(?,?,?)", (movie[0], movie[1], actor_id))
            conn.commit()

director_id = 1
for director, count in director_count.most_common():
    # 判断演员名是否包含英文字符
    if not re.search('[a-zA-Z]', director):
        cursor.execute("insert into directors(director_id,director_name,movie_nums) values(?,?,?)", (director_id, director, count))
        print(f"{director_id} {director}: {count}部电影")
        director_id += 1
        cursor.execute("select movie_id,movie_cname from pythonMovie where director like ?", ('%' + director + '%',))
        movies = cursor.fetchall()
        print(movies)
        for movie in movies:
            cursor.execute("insert into movies_director(movie_id,movie_cname,director_id) values(?,?,?)", (movie[0], movie[1], director_id))
            conn.commit()


conn.close()
