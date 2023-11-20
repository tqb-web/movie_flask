import re  # 正则表达式，与文字匹配
import sqlite3  # 进行sqlite数据库操作
import urllib.error  # 进行excel操作
import time

import requests
import re
import random

import xlwt

from fake_useragent import UserAgent

findActors = re.compile(r'<meta property="video:actor" content="(.*?)" />')
findDirector = re.compile(r'<meta property="video:director" content="(.*?)" />')
#findSummary = re.compile(r'<span property="v:summary">\n\s+(.*?)\s+<br')
findSummary = re.compile(r'<span property="v:summary".*?>\n\s+(.*?)\s+.*?<')
findWatched = re.compile(r'<a href=".*?">(.*?)人看过</a>')
findWanttw = re.compile(r'<a href=".*?">(.*?)人想看</a>')

headers = {
    'Cookie': 'douban-fav-remind=1; ll="108258"; __utmv=30149280.25554; _ga=GA1.2.1722848685.1623638522; _vwo_uuid_v2=DBB1DBD3897AE905809C80738F7956ED9|bb2457ed4e06d584e4dbc2163ffbfeea; bid=6tPNxstd3AE; Hm_lvt_16a14f3002af32bf3a75dfe352478639=1673504263; __utma=30149280.1722848685.1623638522.1674109686.1678198067.25; __utmz=30149280.1678198067.25.10.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utma=223695111.1771176326.1648689891.1674109694.1678198070.23; __utmz=223695111.1678198070.23.10.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __yadk_uid=E71P5xyfjntpvpdlnr2XGvk0Jrrxa3ax; __gads=ID=69bf677c0b2b335d-223455d1e9db00ae:T=1678198412:RT=1678198412:S=ALNI_MYAdo5i7_qb5GsncNKfbC6E43DMTw; __gpi=UID=00000bd35625ba05:T=1678198412:RT=1678198412:S=ALNI_MaAt9ltsaZg3UmUFoC84aOaX0brWw; _pk_ref.100001.4cf6=["","",1678247728,"https://cn.bing.com/"]; _pk_ses.100001.4cf6=*; ap_v=0,6.0; _pk_id.100001.4cf6=4c604b463dd7951e.1648689891.22.1678247740.1678198455.',
    'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1 Edg/110.0.0.0',
}

url = "https://movie.douban.com/subject/3765826"

response = requests.get(url, headers=headers)
print(response.text)

movieActors = findActors.findall(response.text)
movieDirector = findDirector.findall(response.text)[0]
movieSummary = findSummary.findall(response.text)
movieWatched = findWatched.findall(response.text)
movieWanttw = findWanttw.findall(response.text)
#print(movieActors)

# data = []
# actors = ''
# data.append('123')
#
# print(len(movieActors))
#
# for i in range(len(movieActors)):
#      actors += movieActors[i]
#      actors += ' '
#
# data.append(actors)
# #data.append(movieActors)
# data.append(movieDirector)
#
# print(data)

print(movieSummary)
print(movieWatched)
print(movieWanttw)
