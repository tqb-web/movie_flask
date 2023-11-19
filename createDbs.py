import re  # 正则表达式，与文字匹配
import sqlite3  # 进行sqlite数据库操作
import urllib.error  # 进行excel操作
import time

import requests
import re
import random
import logging

import xlwt

from fake_useragent import UserAgent

def main():
    dbpath = "pythonMovie.db"
    # dbpath = "pythonMovie (2).db"
    # dbpath = "sentiment.db"
    # dbpath = "cloud.db"
    # sql = '''
    #         create table pythonMovie
    #         (
    #         id integer primary key autoincrement,
    #         movie_id bigint,
    #         movie_cname varchar,
    #         movie_year varchar,
    #         movie_vote numeric,
    #         movie_score numeric,
    #         info_link text,
    #         category text,
    #         country text,
    #         comment numeric,
    #         evaluation numeric,
    #         actors text,
    #         director text,
    #         movieWatched numeric,
    #         movieWanttw numeric,
    #         movieSummary text
    #         )
    #     '''
    # sql = '''
    #         create table details
    #         (
    #         id integer primary key autoincrement,
    #         movie_id bigint,
    #         movieWatched numeric,
    #         movieWanttw numeric,
    #         movieSummary text
    #         )
    #     '''

    # sql = '''
    #     CREATE TABLE login_times (
    #     id INTEGER PRIMARY KEY AUTOINCREMENT,
    #     userId INTEGER NOT NULL,
    #     date TEXT NOT NULL,
    #     count INTEGER NOT NULL
    # )
    # '''
    # sql = '''
    #     CREATE TABLE comments (
    #     id INTEGER PRIMARY KEY AUTOINCREMENT,
    #     movie_id INTEGER NOT NULL,
    #     comments text
    # )
    # '''
    # sql = '''
    #     CREATE TABLE reviews (
    #     id INTEGER PRIMARY KEY AUTOINCREMENT,
    #     movie_id INTEGER NOT NULL,
    #     reviews text
    # )
    # '''
    # sql = "select * from reviews"
    # sql = "delete from reviews"
#     sql = '''
#     CREATE TABLE IF NOT EXISTS comments_sentiment (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         movie_id INTEGER NOT NULL,
#         positive_count INTEGER,
#         neutral_count INTEGER,
#         negative_count INTEGER
#     )
# '''
#     sql = '''
#     CREATE TABLE IF NOT EXISTS reviews_sentiment (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         movie_id INTEGER NOT NULL,
#         positive_count INTEGER,
#         neutral_count INTEGER,
#         negative_count INTEGER
#     )
# '''

    # sql = '''
    #     CREATE TABLE IF NOT EXISTS cloud (
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         movie_id INTEGER NOT NULL,
    #         comments_wordcloud_data blob,
    #         reviews_wordcloud_data blob
    #     )
    # '''

    # sql = '''
    # CREATE TABLE IF NOT EXISTS bar_reviews_sentiment
    #             (
    #             id INTEGER PRIMARY KEY AUTOINCREMENT,
    #             movie_id INT,
    #             positive_count INT,
    #             neutral_count INT,
    #             negative_count INT,
    #             very_positive_count INT,
    #             very_negative_count INT
    #             )
    # '''
    # sql = '''
    #     CREATE TABLE IF NOT EXISTS sentiment_score
    #                 (
    #                 id INTEGER PRIMARY KEY AUTOINCREMENT,
    #                 movie_id INT,
    #                 movie_score numeric,
    #                 comments_ave_score numeric,
    #                 reviews_ave_score numeric,
    #                 comments_max_score numeric,
    #                 reviews_max_score numeric,
    #                 comments_min_score numeric,
    #                 reviews_min_score numeric
    #                 )
    #     '''
    sql = '''
        CREATE TABLE IF NOT EXISTS actors
                    (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    actor_id INT,
                    actor_name varchar,
                    movie_nums int
                    )
        '''
    # sql = '''
    #     CREATE TABLE IF NOT EXISTS directors
    #                 (
    #                 id INTEGER PRIMARY KEY AUTOINCREMENT,
    #                 director_id INT,
    #                 director_name varchar,
    #                 movie_nums int
    #                 )
    #     '''
    # sql = '''
    #     CREATE TABLE IF NOT EXISTS movies_actor
    #                 (
    #                 id INTEGER PRIMARY KEY AUTOINCREMENT,
    #                 movie_id bigint,
    #                 movie_cname varchar,
    #                 actor_id INT
    #                 )
    #     '''
    # sql = '''
    #     CREATE TABLE IF NOT EXISTS movies_director
    #                 (
    #                 id INTEGER PRIMARY KEY AUTOINCREMENT,
    #                 movie_id bigint,
    #                 movie_cname varchar,
    #                 director_id INT
    #                 )
    #     '''
    # sql = "select * from comments_sentiment"
    # sql = "select * from reviews_sentiment"
    # sql = "select * from sentiment_score"
    # sql = "delete from cloud"
    # sql = "drop table sentiment_score"
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute(sql)
    # all = cursor.fetchall()
    # for a in all:
    #     print(a)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    # 调用函数
    main()


