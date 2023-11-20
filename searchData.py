# 导入sqllite3模块
import sqlite3

from collections import Counter

# 1.硬盘上创建连接
con = sqlite3.connect('pythonMovie.db')
# 获取cursor对象
cur = con.cursor()

sql = 'SELECT country, substr(movie_year,1,4), SUM(movie_vote) FROM pythonMovie GROUP BY country, substr(movie_year,1,4)'
sql = 'select * from pythonMovie'
cur.execute(sql)
person_all = cur.fetchall()
i = 1
for p in person_all:
    print(i, end='')
    i = i+1
    print(p)
# # 执行sql创建表
# # sql = 'select substr(movie_year,1,4),count(substr(movie_year,1,4)) from pythonMovie group by substr(movie_year,1,4)'
# sql1 = 'delete from pythonMovie where rowid not in(select max(rowid) from pythonMovie group by movie_id) '
# sql = 'select * from pythonMovie'
# sql3 = 'select * from details'
# #sql4 = 'delete from details'
# #sql = 'select category,country from pythonMovie order by movie_score desc limit 0,1500'
# sql5 = 'select * from details where movieWatched = 0'
# try:
#     cur.execute(sql)
#     con.commit()
#     #cur.execute(sql)
#     # 获取所有数据
#     i=1
#     person_all = cur.fetchall()
#     for p in person_all:
#         print(i, end='')
#         i = i+1
#         print(p)
#     # 遍历
#     # count = 0
#     # listr = []
#     # s = []
#     # r = []
#     # a = []
#     # for p in person_all:
#     #     p = list(p)
#     #     a = p[0].split(',', -1)
#     #     for i in range(len(a)):
#     #         s.append(a[i])
#     # counter = Counter(s)
#     # dictionary = dict(counter)
#     # res = counter.most_common()
#     # print(res)
#
#     # for p in person_all:
#     #     #p = list(p)
#     #     head, sep, tail = p[0].partition(',')
#     #     r.append(tail)
#     #     head, sep, tail = p[1].partition(',')
#     #     s.append(head)
#     # counter = Counter(r)
#     # dictionary = dict(counter)
#     #
#     # res = counter.most_common()
#     # #print(res)
#     # movie_country = []
#     # nums_country = []
#     # for p in res:
#     #     movie_country.append(p[0])
#     #     nums_country.append(p[1])
#     # print(movie_country)
#     # print(nums_country)
# except Exception as e:
#     print(e)
#     print('查询失败')
# finally:
#     # 关闭游标
#     cur.close()
#     # 关闭连接
#     con.close()

import sqlite3
import csv

# 连接到SQLite3数据库并执行查询语句以检索数据和列名称
# conn = sqlite3.connect('pythonMovie.db')
# cursor = conn.cursor()
# cursor.execute('SELECT * FROM pythonMovie')
# data = cursor.fetchall()
# cursor.close()
# conn.close()
# column_names = [description[0] for description in cursor.description]
#
# # 将数据中的第一列移除
# data = [row[1:] for row in data]
#
# # 创建一个新的CSV文件并将列名称和数据写入其中
# with open('movie.csv', 'w', encoding='utf-8', newline='') as csvfile:
#     csvwriter = csv.writer(csvfile)
#     csvwriter.writerow(column_names[1:])
#     csvwriter.writerows(data)

# with open('movie.csv', newline='', encoding='utf-8') as csvfile:
#     csvreader = csv.reader(csvfile)
#     for row in csvreader:
#         print(', '.join(row))