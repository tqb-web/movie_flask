# -*- coding: utf-8 -*-
from collections import Counter
from time import sleep

from fake_useragent import UserAgent

import requests
import re

import sqlite3

findComments = re.compile(r'全部 (.*?) 条')

baseurl = 'https://movie.douban.com/subject/'

ua = UserAgent()

headers = {
    "User-Agent": ua.random,
}

# headers = {
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#     'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
#     'Cache-Control': 'max-age=0',
#     'Connection': 'keep-alive',
#     # 'Cookie': 'douban-fav-remind=1; ll="108258"; __utmv=30149280.25554; _ga=GA1.2.1722848685.1623638522; _vwo_uuid_v2=DBB1DBD3897AE905809C80738F7956ED9|bb2457ed4e06d584e4dbc2163ffbfeea; push_noty_num=0; push_doumail_num=0; ct=y; dbcl2="255541232:YmeBzpCwlfc"; bid=6tPNxstd3AE; Hm_lvt_16a14f3002af32bf3a75dfe352478639=1673504263; ck=rXN1; frodotk_db="dda0a68e31a8fd2a98e1f3aa94faf77e"; __utmc=30149280; __utmc=223695111; ap_v=0,6.0; __utmz=30149280.1673664598.14.4.utmcsr=127.0.0.1:5000|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmz=223695111.1673664598.12.4.utmcsr=127.0.0.1:5000|utmccn=(referral)|utmcmd=referral|utmcct=/; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1673671043%2C%22http%3A%2F%2F127.0.0.1%3A5000%2F%22%5D; _pk_ses.100001.4cf6=*; __utma=30149280.1722848685.1623638522.1673664598.1673671043.15; __utmb=30149280.0.10.1673671043; __utma=223695111.1771176326.1648689891.1673664598.1673671043.13; __utmb=223695111.0.10.1673671043; _pk_id.100001.4cf6=4c604b463dd7951e.1648689891.10.1673671236.1673664891.',
#     'Sec-Fetch-Dest': 'document',
#     'Sec-Fetch-Mode': 'navigate',
#     'Sec-Fetch-Site': 'none',
#     'Sec-Fetch-User': '?1',
#     'Upgrade-Insecure-Requests': '1',
#     'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1 Edg/108.0.0.0',
# }

params = {
    'status': 'P',
}

con = sqlite3.connect('pythonMovie.db')
# 获取cursor对象
cur = con.cursor()
# 执行sql创建表

sql = 'select * from pythonMovie'
bsql = 'select * from details'

sql1 = 'delete from pythonMovie'

#sql1 = 'delete from pythonMovie where movie_id in (select movie_id from pythonMovie group by movie_id having count(*)>1)'
# sql1 = 'delete from pythonMovie where rowid not in(select max(rowid) from pythonMovie group by movie_id) '
# sql2 = 'update pythonMovie set evaluation = 0 WHERE evaluation = "x"'
#
# sql5 = 'ALTER TABLE pythonMovie drop COLUMN movieWatched'
# cur.execute(sql5)
#
# sql6 = 'ALTER TABLE pythonMovie drop COLUMN movieWanttw'
# cur.execute(sql6)
#
# sql7 = 'ALTER TABLE pythonMovie drop COLUMN movieSummary'
# cur.execute(sql7)

# sql5 = 'ALTER TABLE pythonMovie ADD COLUMN movieWatched numeric;'
# cur.execute(sql5)
#
# sql6 = 'ALTER TABLE pythonMovie ADD COLUMN movieWanttw numeric;'
# cur.execute(sql6)
#
# sql7 = 'ALTER TABLE pythonMovie ADD COLUMN movieSummary text;'
# cur.execute(sql7)

#hbsql = 'UPDATE pythonMovie SET movieWatched = details.movieWatched, movieWanttw = details.movieWanttw, movieSummary = details.movieSummary FROM details WHERE pythonMovie.movie_id = details.movie_id'
sql5 = 'select category,country from pythonMovie order by movie_score desc limit 0,1500'
cur.execute(sql5)
# 获取所有数据
person_all = cur.fetchall()
s = []
for p in person_all:
    head, sep, tail = p[1].partition(',')  # 匹配国家
    s.append(head)

counter = Counter(s)  # 统计高分电影国家及对应数量
dictionary = dict(counter)

m = counter.most_common()
#print(m)

country_dict = {'波黑': 'Bosnia and Herzegovina', '北马其顿': 'Severna Makedonija', '捷克斯洛伐克': 'Czechoslovakia', '中国台湾': 'China', '中国香港': 'China', '中国大陆': 'China', '阿富汗': 'Afghanistan', '奥兰群岛': 'Aland Islands', '阿尔巴尼亚': 'Albania', '阿尔及利亚': 'Algeria', '美属萨摩亚': 'American Samoa', '安道尔': 'Andorra', '安哥拉': 'Angola', '安圭拉': 'Anguilla', '安提瓜和巴布达': 'Antigua and Barbuda', '阿根廷': 'Argentina', '亚美尼亚': 'Armenia', '阿鲁巴': 'Aruba', '澳大利亚': 'Australia', '奥地利 Austria': 'Austria', '奥地利': 'Austria', 'Austria': 'Austria', '奥地利': 'Austria', '阿塞拜疆': 'Azerbaijan', '孟加拉': 'Bangladesh', '巴林': 'Bahrain', '巴哈马': 'Bahamas', '巴巴多斯': 'Barbados', '白俄罗斯': 'Belarus', '比利时': 'Belgium', '伯利兹': 'Belize', '贝宁': 'Benin', '百慕大': 'Bermuda', '不丹': 'Bhutan', '玻利维亚': 'Bolivia', '波斯尼亚和黑塞哥维那': 'Bosnia and Herzegovina', '博茨瓦纳': 'Botswana', '布维岛': 'Bouvet Island', '巴西': 'Brazil', '文莱': 'Brunei', '保加利亚': 'Bulgaria', '布基纳法索': 'Burkina Faso', '布隆迪': 'Burundi', '柬埔寨': 'Cambodia', '喀麦隆': 'Cameroon', '加拿大': 'Canada', '佛得角': 'Cape Verde', '中非': 'Central African Republic', '乍得': 'Chad', '智利': 'Chile', '圣诞岛': 'Christmas Islands', '科科斯（基林）群岛': 'Cocos (keeling) Islands', '哥伦比亚': 'Colombia', '科摩罗': 'Comoros', '刚果（金）': 'Congo (Congo-Kinshasa)', '刚果': 'Congo', '库克群岛': 'Cook Islands', '哥斯达黎加': 'Costa Rica', '科特迪瓦': 'Cote D’Ivoire', '中国': 'China', '克罗地亚': 'Croatia', '古巴': 'Cuba', '捷克': 'Czech', '塞浦路斯': 'Cyprus', '丹麦': 'Denmark', '吉布提': 'Djibouti', '多米尼加': 'Dominica', '东帝汶': 'Timor-Leste', '厄瓜多尔': 'Ecuador', '埃及': 'Egypt', '赤道几内亚': 'Equatorial Guinea', '厄立特里亚': 'Eritrea', '爱沙尼亚': 'Estonia', '埃塞俄比亚': 'Ethiopia', '法罗群岛': 'Faroe Islands', '斐济': 'Fiji', '芬兰': 'Finland', '法国': 'France', '法国大都会': 'Franch Metropolitan', '法属圭亚那': 'Franch Guiana', '法属波利尼西亚': 'French Polynesia', '加蓬': 'Gabon', '冈比亚': 'Gambia', '格鲁吉亚': 'Georgia', '西德': 'Germany', '德国': 'Germany', '加纳': 'Ghana', '直布罗陀': 'Gibraltar', '希腊': 'Greece', '格林纳达': 'Grenada', '瓜德罗普岛': 'Guadeloupe', '关岛': 'Guam', '危地马拉': 'Guatemala', '根西岛': 'Guernsey', '几内亚比绍': 'Guinea-Bissau', '几内亚': 'Guinea', '圭亚那': 'Guyana', '香港 （中国）': 'Hong Kong', '海地': 'Haiti', '洪都拉斯': 'Honduras', '匈牙利': 'Hungary', '冰岛': 'Iceland', '印度': 'India', '印度尼西亚': 'Indonesia', '伊朗': 'Iran', '伊拉克': 'Iraq', '爱尔兰': 'Ireland', '马恩岛': 'Isle of Man', '以色列': 'Israel', '意大利': 'Italy', '牙买加': 'Jamaica', '日本': 'Japan', '泽西岛': 'Jersey', '约旦': 'Jordan', '哈萨克斯坦': 'Kazakhstan', '肯尼亚': 'Kenya', '基里巴斯': 'Kiribati', '韩国': 'Korea (South)', '朝鲜': 'Korea (North)', '科威特': 'Kuwait', '吉尔吉斯斯坦': 'Kyrgyzstan', '老挝': 'Laos', '拉脱维亚': 'Latvia', '黎巴嫩': 'Lebanon', '莱索托': 'Lesotho', '利比里亚': 'Liberia', '利比亚': 'Libya', '列支敦士登': 'Liechtenstein', '立陶宛': 'Lithuania', '卢森堡': 'Luxembourg', '澳门（中国）': 'Macau', '马其顿': 'Macedonia', '马拉维': 'Malawi', '马来西亚': 'Malaysia', '马达加斯加': 'Madagascar', '马尔代夫': 'Maldives', '马里': 'Mali', '马耳他': 'Malta', '马绍尔群岛': 'Marshall Islands', '马提尼克岛': 'Martinique', '毛里塔尼亚': 'Mauritania', '毛里求斯': 'Mauritius', '马约特': 'Mayotte', '墨西哥': 'Mexico', '密克罗尼西亚': 'Micronesia', '摩尔多瓦': 'Moldova', '摩纳哥': 'Monaco', '蒙古': 'Mongolia', '黑山': 'Montenegro', '蒙特塞拉特': 'Montserrat', '摩洛哥': 'Morocco', '莫桑比克': 'Mozambique', '缅甸': 'Myanmar', '纳米比亚': 'Namibia', '瑙鲁': 'Nauru', '尼泊尔': 'Nepal', '荷兰': 'Netherlands', '新喀里多尼亚': 'New Caledonia', '新西兰': 'New Zealand', '尼加拉瓜': 'Nicaragua', '尼日尔': 'Niger', '尼日利亚': 'Nigeria', '纽埃': 'Niue', '诺福克岛': 'Norfolk Island', '挪威': 'Norway', '阿曼': 'Oman', '巴基斯坦': 'Pakistan', '帕劳': 'Palau', '巴勒斯坦': 'Palestine', '巴拿马': 'Panama', '巴布亚新几内亚': 'Papua New Guinea', '巴拉圭': 'Paraguay', '秘鲁': 'Peru', '菲律宾': 'Philippines', '皮特凯恩群岛': 'Pitcairn Islands', '波兰': 'Poland', '葡萄牙': 'Portugal', '波多黎各': 'Puerto Rico', '卡塔尔': 'Qatar', '留尼汪岛': 'Reunion', '罗马尼亚': 'Romania', '卢旺达': 'Rwanda', '俄罗斯联邦': 'Russian Federation', '苏联': 'Russian', '俄罗斯': 'Russian', '圣赫勒拿': 'Saint Helena', '圣基茨和尼维斯': 'Saint Kitts-Nevis', '圣卢西亚': 'Saint Lucia', '圣文森特和格林纳丁斯': 'Saint Vincent and the Grenadines', '萨尔瓦多': 'El Salvador', '萨摩亚': 'Samoa', '圣马力诺': 'San Marino', '圣多美和普林西比': 'Sao Tome and Principe', '沙特阿拉伯': 'Saudi Arabia', '塞内加尔': 'Senegal', '塞舌尔': 'Seychelles', '塞拉利昂': 'Sierra Leone', '新加坡': 'Singapore', '塞尔维亚': 'Serbia', '斯洛伐克': 'Slovakia', '斯洛文尼亚': 'Slovenia', '所罗门群岛': 'Solomon Islands', '索马里': 'Somalia', '南非': 'South Africa', '西班牙': 'Spain', '斯里兰卡': 'Sri Lanka', '苏丹': 'Sudan', '苏里南': 'Suriname', '斯威士兰': 'Swaziland', '瑞典': 'Sweden', '瑞士': 'Switzerland', '叙利亚': 'Syria', '塔吉克斯坦': 'Tajikistan', '坦桑尼亚': 'Tanzania', '台湾 （中国）': 'Taiwan', '泰国': 'Thailand', '特立尼达和多巴哥': 'Trinidad and Tobago', '多哥': 'Togo', '托克劳': 'Tokelau', '汤加': 'Tonga', '突尼斯': 'Tunisia', '土耳其': 'Turkey', '土库曼斯坦': 'Turkmenistan', '图瓦卢': 'Tuvalu', '乌干达': 'Uganda', '乌克兰': 'Ukraine', '阿拉伯联合酋长国': 'United Arab Emirates', '英国': 'United Kingdom', '美国': 'United States', '乌拉圭': 'Uruguay', '乌兹别克斯坦': 'Uzbekistan', '瓦努阿图': 'Vanuatu', '梵蒂冈': 'Vatican City', '委内瑞拉': 'Venezuela', '越南': 'Vietnam', '瓦利斯群岛和富图纳群岛': 'Wallis and Futuna', '西撒哈拉': 'Western Sahara', '也门': 'Yemen', '南斯拉夫': 'Yugoslavia', '赞比亚': 'Zambia', '津巴布韦': 'Zimbabwe'}

result = []

for country, value in m:
    result.append({'name': country_dict[country], 'value': value})


print(result)

cur.execute(sql)
con.commit()


# sql8 = 'SELECT * FROM pythonMovie JOIN details ON pythonMovie.movie_id = details.movie_id'
# cur.execute(sql8)
#
# con.commit()
all = cur.fetchall()

#
# cur.execute(bsql)
# data = cur.fetchall()
#
# cur.execute(sql)
#
# for i in all:
#     cur.execute("INSERT INTO pythonMovie (movieWatched, movieWanttw, movieSummary) VALUES (?, ?, ?) where movie_id = i[0]",
#               (value1, value2, value3))

# a = 1
# for i in all:
#     print(a, " ", end="")
#     a = a+1
#     print(i)

cur.close()
con.close()

# id_all = cur.fetchall()
# id_all = list(id_all)
# nums = len(id_all)
#
# movieId = []
# for item in id_all:
#     movieId.append(str(item[0]))
#
# data = []
# for i in range(nums):
#     url = baseurl + str(movieId[i])
#     print(url)
#     response = requests.get(url, headers=headers)
#     #print(response)
#     movieData = response.text
#     print(movieData)
#
#     comment = findComments.findall(movieData)
#     if len(comment) == 0:
#         data.append('0')
#         continue
#     data.append(comment[0])
#
#     print(comment[0])
# print(data)
# print(len(data))
