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

headers = {'User-Agent': UserAgent().random}

findComments = re.compile(r'<span class="short">(.*?)</span>')  # 匹配电影评论
findId = re.compile(r'<div id="review_(.*?)_full" class="hidden">')
dbpath = "pythonMovie.db"


def main():
    count = 1
    api_url = 'http://www.zdopen.com/PrivateProxy/GetIP/?api=202303081918243387&akey=5ebe32d68944450a&fitter=2&timespan=6&type=1'
    conn = sqlite3.connect(dbpath)
    sql = "select movie_id from pythonMovie"
    cursor = conn.cursor()
    cursor.execute(sql)
    id = cursor.fetchall()
    for item in id:
        for i in range(0, 11):
            data = []
            max_attempt = 20
            for attempt in range(max_attempt):
                try:
                    res = requests.get(api_url, headers=headers).text
                    proxy_list = res.split('\r\n')
                    for proxy in proxy_list:
                        proxies = {
                            'http': 'http://202303081918243387:92110115@' + proxy,
                            'https': 'http://202303081918243387:92110115@' + proxy
                        }
                    # url = "https://movie.douban.com/subject/" + str(item[0]) + "/comments?start=" + str(i * 20) + "&limit=20"
                    url = "https://movie.douban.com/subject/" + str(item[0]) + "/reviews?start=" + str(i * 20)
                    response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
                    # response = requests.get(url, headers=headers)
                    response.raise_for_status()  # 检查响应状态码是否为200
                    movieData = response.text
                    print(movieData)
                    # data = findComments.findall(movieData)
                    break
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
            if len(data) != 0:
                for comment in data:
                    cursor.execute("INSERT INTO comments (movie_id, comments) VALUES (?, ?)", (item[0], comment))
                conn.commit()
            print(count, " ", end="")
            count = count + 1
            print(data)
    conn.close()


if __name__ == '__main__':
    main()
