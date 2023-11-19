from snownlp import SnowNLP
import sqlite3

# 连接数据库
con = sqlite3.connect('pythonMovie.db')
cur = con.cursor()

cur.execute('SELECT DISTINCT movie_id FROM comments')
movie_ids = cur.fetchall()

# 遍历每个电影ID
count = 1

for movie_id in movie_ids:
    movie_id = movie_id[0]

    # 连接数据库
    con = sqlite3.connect('pythonMovie.db')
    cur = con.cursor()

    cur.execute('select movie_score from pythonMovie where movie_id = ?', (movie_id,))
    movie_score = cur.fetchone()
    # 查询电影评论
    cur.execute('SELECT comments FROM comments WHERE movie_id = ?', (movie_id,))
    comments = cur.fetchall()

    # # 定义情感评分的阈值
    # positive_threshold = 0.8
    # neutral_threshold = 0.4
    # negative_threshold = 0.2
    # very_positive_threshold = 0.9
    # very_negative_threshold = 0.1
    #
    # # 统计情感评分段的数量
    # positive_count = 0
    # neutral_count = 0
    # negative_count = 0
    # very_positive_count = 0
    # very_negative_count = 0
    length = len(comments)
    total = 0
    max_score = 0
    min_score = 1
    for comment in comments:

        comment_text = comment[0]
        if len(comment_text) == 0:
            continue
        sentiment_score = SnowNLP(comment_text).sentiments
        if sentiment_score < min_score:
            min_score = sentiment_score
        if sentiment_score > max_score:
            max_score = sentiment_score

        total = total + sentiment_score

        # # 根据情感评分段的阈值进行分类
        # if sentiment_score >= positive_threshold:
        #     positive_count += 1
        # elif sentiment_score < positive_threshold and sentiment_score >= neutral_threshold:
        #     neutral_count += 1
        # elif sentiment_score < neutral_threshold and sentiment_score >= negative_threshold:
        #     negative_count += 1
        # elif sentiment_score < negative_threshold and sentiment_score >= very_negative_threshold:
        #     very_negative_count += 1
        # elif sentiment_score < very_negative_threshold:
        #     very_positive_count += 1
    # print(positive_count, neutral_count, negative_count, very_negative_count, very_positive_count)
    # 将统计结果插入到数据库
    score = total / length
    # print(length)
    # print(movie_score[0])
    # print(score)
    # print(max_score)
    # print(min_score)
    print(count)
    count = count + 1
    con.close()

    con = sqlite3.connect('sentiment.db')
    cur = con.cursor()
    # cur.execute("INSERT INTO bar_comments_sentiment (movie_id, positive_count, neutral_count, negative_count, very_positive_count, very_negative_count) VALUES (?, ?, ?, ?, ?, ?)",
    #             (movie_id, positive_count, neutral_count, negative_count, very_positive_count, very_negative_count))
    cur.execute(
        "insert into sentiment_score (movie_id, movie_score, comments_ave_score, comments_max_score, comments_min_score) values(?,?,?,?,?)",
        (movie_id, movie_score[0], score, max_score, min_score))

    # 提交并关闭数据库连接
    con.commit()
    con.close()

# # 连接数据库并查询电影评论
# con = sqlite3.connect('pythonMovie.db')
# cur = con.cursor()
# # cur.execute('SELECT movie_id, comments FROM comments')
# cur.execute('SELECT movie_id, reviews FROM reviews')
# data = cur.fetchall()
#
# i = 1
# # 创建字典来存储每部电影的情感评分数量
# sentiment_count = {}
# for comment in data:
#     movie_id = comment[0]
#     comment_text = comment[1]
#     if len(comment_text) == 0:
#         continue
#     sentiment_score = SnowNLP(comment_text).sentiments
#
#     # 根据情感得分更新情感评分数量
#     if movie_id not in sentiment_count:
#         sentiment_count[movie_id] = {'positive': 0, 'neutral': 0, 'negative': 0}
#     if sentiment_score < 0.5:
#         sentiment_count[movie_id]['negative'] += 1
#     elif sentiment_score > 0.5:
#         sentiment_count[movie_id]['positive'] += 1
#     else:
#         sentiment_count[movie_id]['neutral'] += 1
#     print(i)
#     i = i + 1
#     # print(comment_text)
#     # print(movie_id, sentiment_count[movie_id]['negative'], sentiment_count[movie_id]['positive'], sentiment_count[movie_id]['neutral'])
# con.close()
#
# con = sqlite3.connect('sentiment.db')
# cur = con.cursor()
# 将统计结果插入到 SQLite 数据库中
# for movie_id, sentiment_dict in sentiment_count.items():
#     cur.execute(
#         "INSERT INTO comments_sentiment (movie_id, positive_count, neutral_count, negative_count) VALUES (?, ?, ?, ?)",
#         (movie_id, sentiment_dict['positive'], sentiment_dict['neutral'], sentiment_dict['negative']))

# for movie_id, sentiment_dict in sentiment_count.items():
#     cur.execute(
#         "INSERT INTO reviews_sentiment (movie_id, positive_count, neutral_count, negative_count) VALUES (?, ?, ?, ?)",
#         (movie_id, sentiment_dict['positive'], sentiment_dict['neutral'], sentiment_dict['negative']))
#
# con.commit()
# con.close()
