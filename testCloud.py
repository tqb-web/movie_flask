import re
import sqlite3
from io import BytesIO

import jieba
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image  # 图片处理
from wordcloud import WordCloud

# 连接数据库
con = sqlite3.connect('pythonMovie.db')
cur = con.cursor()

# 获取电影ID和评论数据
# cur.execute('SELECT movie_id, GROUP_CONCAT(comments, " ") FROM comments GROUP BY movie_id')
cur.execute('SELECT movie_id, GROUP_CONCAT(reviews, " ") FROM reviews GROUP BY movie_id')

data = cur.fetchall()

con.close()

count = 1
for row in data:
    movie_id = row[0]
    comments = row[1]

    # 将多条评论数据合并为一个文本
    text = ''.join(comments)
    text = re.findall(r'[\u4e00-\u9fa5]', text)
    chinese_text = ''.join(text)

    # 分词处理
    cut = jieba.cut(chinese_text)
    comments = ' '.join(cut)
    comments = " ".join(word for word in comments.split() if len(word) > 1)
    if len(comments) == 0:
        continue
    # print(len(chinese_text))
    # print(chinese_text)
    # print(comments)

    # img = Image.open(r'.\static\assets\img\tree.jpg')  # 打开遮罩图片
    # img = Image.open(r'.\static\assets\img\bear.jpg')  # 打开遮罩图片
    # img_array = np.array(img)  # 将图片转换为数组

    # 生成词云图
    wc = WordCloud(width=800, height=500, background_color='white', font_path="msyh.ttc")
    wc.generate_from_text(comments)

    # 将词云图转换为二进制数据
    buffer = BytesIO()
    plt.imshow(wc)
    plt.axis('off')
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    img_data = buffer.getvalue()
    # plt.show()
    # print(img_data)
    print(count)
    count = count + 1

    con = sqlite3.connect('cloud.db')
    cur = con.cursor()
    # 将电影ID和词云图数据存入数据库
    # cur.execute('insert into cloud (movie_id,comments_wordcloud_data) values(?,?)', (movie_id, img_data))
    cur.execute('UPDATE cloud SET reviews_wordcloud_data = ? WHERE movie_id = ?', (img_data, movie_id))
    con.commit()

# 关闭数据库连接
cur.close()
con.close()
