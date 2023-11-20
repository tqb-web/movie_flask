import re

from snownlp import SnowNLP
import sqlite3

# 连接数据库
con = sqlite3.connect('pythonMovie.db')
cur = con.cursor()

cur.execute('SELECT DISTINCT movie_id FROM reviews')
movie_ids = cur.fetchall()

# 遍历每个电影ID
count = 1

for movie_id in movie_ids:
    movie_id = movie_id[0]

    # 连接数据库
    con = sqlite3.connect('pythonMovie.db')
    cur = con.cursor()

    # 查询电影评论
    cur.execute('SELECT reviews FROM reviews WHERE movie_id = ?', (movie_id,))
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
        # 使用TextBlob进行情感分析
        comment_text = comment[0]
        comment_text = re.sub(r'\n', '', comment_text)
        if len(comment_text) == 0:
            continue
        sentiment_score = SnowNLP(comment_text).sentiments

        if sentiment_score <= min_score:
            min_score = sentiment_score
        if sentiment_score >= max_score:
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
    # print(score)
    # print(max_score)
    # print(min_score)
    print(count)
    count = count + 1
    con.close()

    con = sqlite3.connect('sentiment.db')
    cur = con.cursor()
    cur.execute(
        "update sentiment_score set reviews_ave_score=?, reviews_max_score=?, reviews_min_score=? where movie_id=?",
        (score, max_score, min_score, movie_id))
    # cur.execute(
    #     "INSERT INTO bar_reviews_sentiment (movie_id, positive_count, neutral_count, negative_count, very_positive_count, very_negative_count) VALUES (?, ?, ?, ?, ?, ?)",
    #     (movie_id, positive_count, neutral_count, negative_count, very_positive_count, very_negative_count))
    #
    # 提交并关闭数据库连接
    con.commit()
    con.close()
