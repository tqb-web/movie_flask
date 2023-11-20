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

# 创建正则表达式
findId = re.compile(r'"id":"(.*?)",')  # 匹配电影id
findTitle = re.compile(r'"title":"(.*?)",')  # 匹配电影名字
findDate = re.compile(r'"release_date":"(.*?)",')  # 匹配上映日期
findVote = re.compile(r'"vote_count":(.*?),')  # 匹配票数
findScore = re.compile(r'"score":"(.*?)",')  # 匹配评分
findUrl = re.compile(r'"url":"(.*?)",')  # 匹配网址
findType = re.compile(r'"types":\[(.*?)],')  # 匹配类型
findRegion = re.compile(r'"regions":\[(.*?)],')  # 匹配地区
findComments = re.compile(r'全部 (.*?) 条')  # 匹配评论数
findEvaluation = re.compile(r'"ratingCount": "(.*?)",') #匹配评价人数
findActors = re.compile(r'<meta property="video:actor" content="(.*?)" />') #匹配演员
findDirector = re.compile(r'<meta property="video:director" content="(.*?)" />')  #匹配导演


def main():
    baseurl = "https://movie.douban.com/j/chart/top_list?type="
    c_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        #'Cookie': 'douban-fav-remind=1; ll="108258"; __utmv=30149280.25554; _ga=GA1.2.1722848685.1623638522; _vwo_uuid_v2=DBB1DBD3897AE905809C80738F7956ED9|bb2457ed4e06d584e4dbc2163ffbfeea; push_noty_num=0; push_doumail_num=0; ct=y; dbcl2="255541232:YmeBzpCwlfc"; bid=6tPNxstd3AE; Hm_lvt_16a14f3002af32bf3a75dfe352478639=1673504263; ck=rXN1; frodotk_db="dda0a68e31a8fd2a98e1f3aa94faf77e"; __utmc=30149280; __utmc=223695111; ap_v=0,6.0; __utmz=30149280.1673664598.14.4.utmcsr=127.0.0.1:5000|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmz=223695111.1673664598.12.4.utmcsr=127.0.0.1:5000|utmccn=(referral)|utmcmd=referral|utmcct=/; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1673671043%2C%22http%3A%2F%2F127.0.0.1%3A5000%2F%22%5D; _pk_ses.100001.4cf6=*; __utma=30149280.1722848685.1623638522.1673664598.1673671043.15; __utmb=30149280.0.10.1673671043; __utma=223695111.1771176326.1648689891.1673664598.1673671043.13; __utmb=223695111.0.10.1673671043; _pk_id.100001.4cf6=4c604b463dd7951e.1648689891.10.1673671236.1673664891.',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1 Edg/108.0.0.0',
    }

    headers = {'User-Agent': UserAgent().random}

    params = {
        'status': 'P',
    }

    html_nums = 31  # 爬取的页面数量
    # datalist = getData(baseurl, headers, html_nums, ave_nums, proxies)
    dbpath = "pythonMovie.db"
    getData(baseurl, headers, c_headers, params, html_nums, dbpath)
    savepath = "pythonMovie.xls"
    # 保存数据
    #saveData(datalist, savepath)
    #saveData2DB(datalist, dbpath)




logging.basicConfig(filename='log.txt', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def getData(baseurl, headers, c_headers, params, html_nums, dbpath):
    global count    # 统计电影数量
    count = 0
    datalist = []
    api_url = 'http://www.zdopen.com/PrivateProxy/GetIP/?api=202303081918243387&akey=5ebe32d68944450a&fitter=2&timespan=6&type=1'
    for i in range(1, html_nums + 1):
        max_attempt = 10
        for attempt in range(max_attempt):
            url = baseurl + str(i) + "&amp;interval_id=100:90"
            try:
                res = requests.get(api_url, headers=headers).text
                proxy_list = res.split('\r\n')
                for proxy in proxy_list:
                    proxies = {
                        'http':'http://202303081918243387:92110115@'+proxy,
                        'https':'http://202303081918243387:92110115@'+proxy
                    }
                response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
                movieData = response.text
                response.raise_for_status()  # 检查响应状态码是否为200
                print(i, " ", end="")
                print(movieData)
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

        movieId = findId.findall(movieData)
        length = len(movieId)
        count = count + length

        for j in range(length):
            data = []
            movieId = findId.findall(movieData)[j]
            data.append(movieId)

            movieTitle = findTitle.findall(movieData)[j]
            data.append(movieTitle)

            moviedate = findDate.findall(movieData)[j]
            data.append(moviedate)

            movieVote = findVote.findall(movieData)[j]
            data.append(movieVote)

            movieScore = findScore.findall(movieData)[j]
            data.append(movieScore)

            movieUrl = findUrl.findall(movieData)[j]
            data.append(movieUrl)

            movieType = findType.findall(movieData)[j]
            movieType = movieType.replace('"', '')
            data.append(movieType)

            movieRegion = findRegion.findall(movieData)[j]
            movieRegion = movieRegion.replace('"', '')
            data.append(movieRegion)

            #url = 'https://movie.douban.com/subject/' + str(movieId)
            max_attempts = 10
            for attempt in range(max_attempts):
                url = 'https://movie.douban.com/subject/' + str(movieId)
                try:
                    res = requests.get(api_url, headers=headers).text
                    proxy_list = res.split('\r\n')
                    for proxy in proxy_list:
                        proxies = {
                            'http': 'http://202303081918243387:92110115@' + proxy,
                            'https': 'http://202303081918243387:92110115@' + proxy
                        }
                    response = requests.get(url, params=params, headers=c_headers, proxies=proxies, timeout=10)
                    c_movieData = response.text
                    response.raise_for_status()
                    time.sleep(random.random())
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


            comment = findComments.findall(c_movieData)
            evaluation = findEvaluation.findall(c_movieData)
            movieActors = findActors.findall(c_movieData)
            movieDirector = findDirector.findall(c_movieData)

            actors = ''
            director = ''


            for a in range(len(movieActors)):
                actors += movieActors[a]
                actors += ' '

            for b in range(len(movieDirector)):
                director += movieDirector[b]
                director += ' '

            if len(comment) == 0:
                data.append('0')
            else:
                data.append(comment[0])

            if len(evaluation) == 0:
                data.append('x')
            else:
                data.append(evaluation[0])

            if len(actors) == 0:
                data.append('x')
            else:
                data.append(actors)

            if len(director) == 0:
                data.append('x')
            else:
                data.append(director)
            #print(count)
            print(j,end="")
            print(data)

            conn = sqlite3.connect(dbpath)
            cur = conn.cursor()

            for index in range(len(data)):
                data[index] = '"' + data[index] + '"'
            sql = '''
                    insert into pythonMovie(
                    movie_id, movie_cname, movie_year, movie_vote, movie_score, info_link, category, country, comment, evaluation, actors, director)
                    values(%s)''' % (",".join(data))
            cur.execute(sql)
            conn.commit()

            #datalist.append(data)
    cur.close()
    conn.close()
    #return datalist




#
# def saveData2DB(datalist, dbpath):
#     init_db(dbpath)
#     conn = sqlite3.connect(dbpath)
#     cur = conn.cursor()
#
#     for data in datalist:
#         for index in range(len(data)):
#             data[index] = '"' + data[index] + '"'
#         sql = '''
#                 insert into pythonMovie(
#                 movie_id, movie_cname, movie_year, movie_vote, movie_score, info_link, category, country, comment, evaluation, actors, director)
#                 values(%s)''' % (",".join(data))
#         cur.execute(sql)
#         conn.commit()
#     sql1 = 'delete from pythonMovie where rowid not in(select max(rowid) from pythonMovie group by movie_id) '  # 删除重复数据
#     cur.execute(sql1)
#     conn.commit()
#     cur.close()
#     conn.close


# # 保存数据
# def saveData(datalist, savepath):
#     print("save...")
#     book = xlwt.Workbook(encoding="utf-8")  # 创建workbook对象
#     sheet = book.add_sheet('pythonMovie', cell_overwrite_ok=True)  # 创建工作表
#
#     # 制作表头
#     col = ("电影id", "电影名", "上映年份", "票房", "评分", "链接", "类型", "地区", "评论数量", "评价人数", "演员", "导演")
#     for i in range(0, len(col)):
#         sheet.write(0, i, col[i])
#
#     for i in range(0, 10):
#     #for i in range(0, 3):
#         # print("第%d条"%(i+1))
#         data = datalist[i]
#         for j in range(0, len(col)):
#             sheet.write(i + 1, j, data[j])
#
#     book.save(savepath)  # 保存


if __name__ == "__main__":
    # 调用函数
    main()
