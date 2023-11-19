import re  # 正则表达式，与文字匹配
import sqlite3  # 进行sqlite数据库操作
import urllib.error  # 进行excel操作
import time

import requests
import re
import random
import logging

import xlwt
findId = re.compile(r' <a href="https://movie.douban.com/subject/(.*?)/".*?>')
findurl = re.compile(r'<a href="(.*?)".*?class="">')
findName = re.compile(r'"name": "(.*?)",')
findActors = re.compile(r'<meta property="video:actor" content="(.*?)" />') #匹配演员
findDirector = re.compile(r'<meta property="video:director" content="(.*?)" />')  #匹配导演
findSummary = re.compile(r'<span property="v:summary".*?>\n\s+(.*?)\s+.*?<')
findRate = re.compile(r'<strong class="ll rating_num" property="v:average">(.*?)</strong>') #评分
findCountry = re.compile(r'<span class="pl">制片国家/地区:</span>(.*?)<br/>')
findType = re.compile(r'<span class="pl">类型:</span> <span property="v:genre">(.*?)</span')
findPicture = re.compile(r'  "image": "(.*?)",')
findTime = re.compile(r'"datePublished": "(.*?)",')




from fake_useragent import UserAgent

def main():
    baseurl = "https://movie.douban.com/top250?start="
    #hhttps://movie.douban.com/top250?start=0&filter=
    headers = {'User-Agent': UserAgent().random}
    getData(baseurl, headers)


def getData(baseurl ,headers):
    for i in range(1):
        url = baseurl+str(i*25)+"&filter="
        response = requests.get(url, headers=headers)
        print(response.text)
        movieData = response.text
        #Url = findurl.findall(movieData)
        id = findId.findall(movieData)
        url1 = findurl.findall(movieData)
        #print(response.text)
        for j in range(25):
            data = []
            print(url1[j])
            #data.append(str(id[j]))
            response = requests.get(url1[j], headers=headers)
            data.append(id[j])
            name = findName.findall(response.text)[0]
            data.append(name)
            rate = findRate.findall(response.text)[0]
            data.append(rate)
            director = findDirector.findall(response.text)[0]
            data.append(director)
            actors = findActors.findall(response.text)[0]
            data.append(actors)
            time = findTime.findall(response.text)[0]
            data.append(time)
            country = findCountry.findall(response.text)[0]
            data.append(country)
            type = findType.findall(response.text)[0]
            data.append(type)
            info = findSummary.findall(response.text)[0]
            data.append(info)
            data.append(url1[j])
            picture = findPicture.findall(response.text)[0]
            data.append(picture)

            print(data)




if __name__ == "__main__":
    # 调用函数
    main()