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

#findSummary = re.compile(r'<span property="v:summary">\n\s+(.*?)\s+<br')
findSummary = re.compile(r'<span property="v:summary".*?>\n\s+(.*?)\s+.*?<')
findWatched = re.compile(r'<a href=".*?">(.*?)人看过</a>')
findWanttw = re.compile(r'<a href=".*?">(.*?)人想看</a>')
findMovieid = re.compile(r'\d+')

dbpath = "pythonMovie.db"

con = sqlite3.connect(dbpath)
cur = con.cursor()

sql = 'select movie_id from details where movieWatched = 0'

cur.execute(sql)

movieId = cur.fetchall()

# 关闭游标
cur.close()
# 关闭连接
con.close()

api_url = 'http://www.zdopen.com/PrivateProxy/GetIP/?api=202303081918243387&akey=5ebe32d68944450a&fitter=2&timespan=6&type=1'

headers = {'User-Agent': UserAgent().random}

# params = {
#     'status': 'P',
# }

j = 1

for i in movieId:
    data = []
    #print(url)
    max_attempts = 10
    for attempt in range(max_attempts):
        url = 'https://movie.douban.com/subject/' + str(i[0])
        id = str(i[0])
        try:
            res = requests.get(api_url, headers=headers).text
            proxy_list = res.split('\r\n')
            for proxy in proxy_list:
                proxies = {
                    'http': 'http://202303081918243387:92110115@' + proxy,
                    'https': 'http://202303081918243387:92110115@' + proxy
                }
            #time.sleep(random.random())
            response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
            c_movieData = response.text
            response.raise_for_status()
            break  # 请求成功，跳出循环
        except requests.exceptions.Timeout as e:
            logging.error(f"请求超时：{e}")
            continue
        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP 错误：{e}")
            continue
        except requests.exceptions.RequestException as e:
            logging.error(f"其他异常：{e}")
            continue
        except requests.exceptions.ProxyError as e:
            logging.error(f"代理错误：{e}")
            continue

    movieSummary = findSummary.findall(c_movieData)
    movieWatched = findWatched.findall(c_movieData)
    movieWanttw = findWanttw.findall(c_movieData)
    data.append(str(i[0]))
    if len(movieWatched) == 0:
        data.append('0')
        a = 0
    else:
        data.append(movieWatched[0])
        a = movieWatched[0]

    if len(movieWanttw) == 0:
        data.append('0')
        b = 0
    else:
        data.append(movieWanttw[0])
        b = movieWanttw[0]

    if len(movieSummary) == 0:
        data.append('null')
        c = 'null'
    else:
        data.append(movieSummary[0])
        c = movieSummary[0]
    print(j, " ", url, " ", end="")
    j = j + 1
    print(data)

    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()

    # for index in range(len(data)):
    #     data[index] = '"' + data[index] + '"'
    # sql = '''
    #         insert into details(
    #         movie_id, movieWatched, movieWanttw, movieSummary)
    #         values(%s)''' % (",".join(data))

    sql = 'update details set movieWatched = ?, movieWanttw = ?, movieSummary = ? where movie_id = ?'
    cur.execute(sql, (a, b, c, id))
    conn.commit()

cur.close()
conn.close()