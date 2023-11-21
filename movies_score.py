import sqlite3
from collections import Counter  # 统计字频

from flask import Blueprint, render_template
from flask_login import login_required

movies_score_bp = Blueprint('movies_score', __name__)


@movies_score_bp.route('/score')
@login_required
def score():
    score1 = []  # 评分
    num1 = []  # 每个评分所统计出的电影数量
    movie_year1 = []  # 年份
    movie_num1 = []  # 每个年份所统计出的电影数量
    movie_year2 = []  # 年份
    movie_num2 = []  # 每个年份所统计出的电影数量
    score2 = []
    num2 = []
    res1 = {}
    res2 = {}
    res3 = {}
    con = sqlite3.connect("database/movie.db")
    cur = con.cursor()
    sql = "select score,count(score) from movie250 group by score"
    # res1 = dict(cur.fetchall())
    data = cur.execute(sql)
    for item1 in data:
        score1.append(str(item1[0]))
        num1.append(item1[1])
    for k, v in zip(score1, num1):
        res1.update({k: v, }, )

    sql2 = "select year_release,count(year_release) from movie250 group by year_release"
    data2 = cur.execute(sql2)
    for item2 in data2:
        movie_year1.append(str(item2[0]))
        movie_num1.append(item2[1])

    cur.close()
    con.close()

    con = sqlite3.connect("database/pythonMovie.db")
    cur = con.cursor()

    sql3 = "select movie_score,count(movie_score) from pythonMovie group by movie_score"
    data3 = cur.execute(sql3)

    for item3 in data3:
        score2.append(str(item3[0]))
        num2.append(item3[1])

    for k, v in zip(score2, num2):
        res2.update({k: v, }, )

    sql4 = 'select substr(movie_year,1,4),count(substr(movie_year,1,4)) from pythonMovie group by substr(movie_year,1,4)'
    data4 = cur.execute(sql4)
    # a = cur.fetchall()
    # print(a)

    for item4 in data4:
        # print(item4)
        movie_year2.append(str(item4[0]))
        movie_num2.append(item4[1])

    for k, v in zip(movie_year2, movie_num2):
        res3.update({k: v, }, )
    # print(res3)

    sql5 = 'select category,country from pythonMovie order by movie_score desc limit 500'
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

    movie_country = []
    nums_country = []
    for p in m:
        movie_country.append(p[0])
        nums_country.append(p[1])

    # 世界地图
    country_dict = {'波黑': 'Bosnia and Herzegovina', '北马其顿': 'Severna Makedonija',
                    '捷克斯洛伐克': 'Czechoslovakia', '中国台湾': 'China', '中国香港': 'China', '中国大陆': 'China',
                    '阿富汗': 'Afghanistan', '奥兰群岛': 'Aland Islands', '阿尔巴尼亚': 'Albania',
                    '阿尔及利亚': 'Algeria', '美属萨摩亚': 'American Samoa', '安道尔': 'Andorra', '安哥拉': 'Angola',
                    '安圭拉': 'Anguilla', '安提瓜和巴布达': 'Antigua and Barbuda', '阿根廷': 'Argentina',
                    '亚美尼亚': 'Armenia', '阿鲁巴': 'Aruba', '澳大利亚': 'Australia', '奥地利 Austria': 'Austria',
                    '奥地利': 'Austria', 'Austria': 'Austria', '奥地利': 'Austria', '阿塞拜疆': 'Azerbaijan',
                    '孟加拉': 'Bangladesh', '巴林': 'Bahrain', '巴哈马': 'Bahamas', '巴巴多斯': 'Barbados',
                    '白俄罗斯': 'Belarus', '比利时': 'Belgium', '伯利兹': 'Belize', '贝宁': 'Benin',
                    '百慕大': 'Bermuda', '不丹': 'Bhutan', '玻利维亚': 'Bolivia',
                    '波斯尼亚和黑塞哥维那': 'Bosnia and Herzegovina', '博茨瓦纳': 'Botswana', '布维岛': 'Bouvet Island',
                    '巴西': 'Brazil', '文莱': 'Brunei', '保加利亚': 'Bulgaria', '布基纳法索': 'Burkina Faso',
                    '布隆迪': 'Burundi', '柬埔寨': 'Cambodia', '喀麦隆': 'Cameroon', '加拿大': 'Canada',
                    '佛得角': 'Cape Verde', '中非': 'Central African Reo.', '乍得': 'Chad', '智利': 'Chile',
                    '圣诞岛': 'Christmas Islands', '科科斯（基林）群岛': 'Cocos (keeling) Islands',
                    '哥伦比亚': 'Colombia', '科摩罗': 'Comoros', '刚果（金）': 'Congo (Congo-Kinshasa)', '刚果': 'Congo',
                    '库克群岛': 'Cook Islands', '哥斯达黎加': 'Costa Rica', '科特迪瓦': 'Cote D’Ivoire',
                    '中国': 'China', '克罗地亚': 'Croatia', '古巴': 'Cuba', '捷克': 'Czech', '塞浦路斯': 'Cyprus',
                    '丹麦': 'Denmark', '吉布提': 'Djibouti', '多米尼加': 'Dominica', '东帝汶': 'Timor-Leste',
                    '厄瓜多尔': 'Ecuador', '埃及': 'Egypt', '赤道几内亚': 'Equatorial Guinea', '厄立特里亚': 'Eritrea',
                    '爱沙尼亚': 'Estonia', '埃塞俄比亚': 'Ethiopia', '法罗群岛': 'Faroe Islands', '斐济': 'Fiji',
                    '芬兰': 'Finland', '法国': 'France', '法国大都会': 'Franch Metropolitan',
                    '法属圭亚那': 'Franch Guiana', '法属波利尼西亚': 'French Polynesia', '加蓬': 'Gabon',
                    '冈比亚': 'Gambia', '格鲁吉亚': 'Georgia', '西德': 'Germany', '德国': 'Germany', '加纳': 'Ghana',
                    '直布罗陀': 'Gibraltar', '希腊': 'Greece', '格林纳达': 'Grenada', '瓜德罗普岛': 'Guadeloupe',
                    '关岛': 'Guam', '危地马拉': 'Guatemala', '根西岛': 'Guernsey', '几内亚比绍': 'Guinea-Bissau',
                    '几内亚': 'Guinea', '圭亚那': 'Guyana', '香港 （中国）': 'Hong Kong', '海地': 'Haiti',
                    '洪都拉斯': 'Honduras', '匈牙利': 'Hungary', '冰岛': 'Iceland', '印度': 'India',
                    '印度尼西亚': 'Indonesia', '伊朗': 'Iran', '伊拉克': 'Iraq', '爱尔兰': 'Ireland',
                    '马恩岛': 'Isle of Man', '以色列': 'Israel', '意大利': 'Italy', '牙买加': 'Jamaica',
                    '日本': 'Japan', '泽西岛': 'Jersey', '约旦': 'Jordan', '哈萨克斯坦': 'Kazakhstan',
                    '肯尼亚': 'Kenya', '基里巴斯': 'Kiribati', '韩国': 'Korea (South)', '朝鲜': 'Korea (North)',
                    '科威特': 'Kuwait', '吉尔吉斯斯坦': 'Kyrgyzstan', '老挝': 'Laos', '拉脱维亚': 'Latvia',
                    '黎巴嫩': 'Lebanon', '莱索托': 'Lesotho', '利比里亚': 'Liberia', '利比亚': 'Libya',
                    '列支敦士登': 'Liechtenstein', '立陶宛': 'Lithuania', '卢森堡': 'Luxembourg', '澳门（中国）': 'Macau',
                    '马其顿': 'Macedonia', '马拉维': 'Malawi', '马来西亚': 'Malaysia', '马达加斯加': 'Madagascar',
                    '马尔代夫': 'Maldives', '马里': 'Mali', '马耳他': 'Malta', '马绍尔群岛': 'Marshall Islands',
                    '马提尼克岛': 'Martinique', '毛里塔尼亚': 'Mauritania', '毛里求斯': 'Mauritius',
                    '马约特': 'Mayotte', '墨西哥': 'Mexico', '密克罗尼西亚': 'Micronesia', '摩尔多瓦': 'Moldova',
                    '摩纳哥': 'Monaco', '蒙古': 'Mongolia', '黑山': 'Montenegro', '蒙特塞拉特': 'Montserrat',
                    '摩洛哥': 'Morocco', '莫桑比克': 'Mozambique', '缅甸': 'Myanmar', '纳米比亚': 'Namibia',
                    '瑙鲁': 'Nauru', '尼泊尔': 'Nepal', '荷兰': 'Netherlands', '新喀里多尼亚': 'New Caledonia',
                    '新西兰': 'New Zealand', '尼加拉瓜': 'Nicaragua', '尼日尔': 'Niger', '尼日利亚': 'Nigeria',
                    '纽埃': 'Niue', '诺福克岛': 'Norfolk Island', '挪威': 'Norway', '阿曼': 'Oman',
                    '巴基斯坦': 'Pakistan', '帕劳': 'Palau', '巴勒斯坦': 'Palestine', '巴拿马': 'Panama',
                    '巴布亚新几内亚': 'Papua New Guinea', '巴拉圭': 'Paraguay', '秘鲁': 'Peru', '菲律宾': 'Philippines',
                    '皮特凯恩群岛': 'Pitcairn Islands', '波兰': 'Poland', '葡萄牙': 'Portugal',
                    '波多黎各': 'Puerto Rico', '卡塔尔': 'Qatar', '留尼汪岛': 'Reunion', '罗马尼亚': 'Romania',
                    '卢旺达': 'Rwanda', '俄罗斯联邦': 'Russian Federation', '苏联': 'Russia', '俄罗斯': 'Russia',
                    '圣赫勒拿': 'Saint Helena', '圣基茨和尼维斯': 'Saint Kitts-Nevis', '圣卢西亚': 'Saint Lucia',
                    '圣文森特和格林纳丁斯': 'Saint Vincent and the Grenadines', '萨尔瓦多': 'El Salvador',
                    '萨摩亚': 'Samoa', '圣马力诺': 'San Marino', '圣多美和普林西比': 'Sao Tome and Principe',
                    '沙特阿拉伯': 'Saudi Arabia', '塞内加尔': 'Senegal', '塞舌尔': 'Seychelles',
                    '塞拉利昂': 'Sierra Leone', '新加坡': 'Singapore', '塞尔维亚': 'Serbia', '斯洛伐克': 'Slovakia',
                    '斯洛文尼亚': 'Slovenia', '所罗门群岛': 'Solomon Islands', '索马里': 'Somalia',
                    '南非': 'South Africa', '西班牙': 'Spain', '斯里兰卡': 'Sri Lanka', '苏丹': 'Sudan',
                    '苏丹共和国': 'S. Sudan',
                    '苏里南': 'Suriname', '斯威士兰': 'Swaziland', '瑞典': 'Sweden', '瑞士': 'Switzerland',
                    '叙利亚': 'Syria', '塔吉克斯坦': 'Tajikistan', '坦桑尼亚': 'Tanzania', '台湾 （中国）': 'Taiwan',
                    '泰国': 'Thailand', '特立尼达和多巴哥': 'Trinidad and Tobago', '多哥': 'Togo', '托克劳': 'Tokelau',
                    '汤加': 'Tonga', '突尼斯': 'Tunisia', '土耳其': 'Turkey', '土库曼斯坦': 'Turkmenistan',
                    '图瓦卢': 'Tuvalu', '乌干达': 'Uganda', '乌克兰': 'Ukraine',
                    '阿拉伯联合酋长国': 'United Arab Emirates', '英国': 'United Kingdom', '美国': 'United States',
                    '乌拉圭': 'Uruguay', '乌兹别克斯坦': 'Uzbekistan', '瓦努阿图': 'Vanuatu', '梵蒂冈': 'Vatican City',
                    '委内瑞拉': 'Venezuela', '越南': 'Vietnam', '瓦利斯群岛和富图纳群岛': 'Wallis and Futuna',
                    '西撒哈拉': 'Western Sahara', '也门': 'Yemen', '南斯拉夫': 'Yugoslavia', '赞比亚': 'Zambia',
                    '津巴布韦': 'Zimbabwe', '刚果共和国': 'Dem. Rep. Congo', '中非共和国': 'Central African Rep.',
                    '利比亚共和国': 'Liberia', '科特迪瓦共和国': 'Côte d\'Ivoire', '西撒哈拉': 'W. Sahara'}

    result = []

    for country, value in m:
        result.append({'name': country_dict[country], 'value': value})

    # 获取所有英文名
    english_names = set(country_dict.values())

    # 添加缺失的国家到result中
    for name in english_names:
        exists = False
        for item in result:
            if item['name'] == name:
                exists = True
                break
        if not exists:
            result.append({'name': name, 'value': 0})

    lresult = []

    for item in result:
        index = next((i for i, x in enumerate(lresult) if x['name'] == item['name']), None)
        if index is None:
            lresult.append(item)
        else:
            lresult[index]['value'] += item['value']

    # 统计电影类型
    r = []
    for p in person_all:
        p = list(p)
        a = p[0].split(',', -1)
        for i in range(len(a)):
            r.append(a[i])
    counter = Counter(r)
    dictionary = dict(counter)
    m = counter.most_common()

    movie_category = []
    nums_category = []
    for p in m[1:]:
        movie_category.append(p[0])
        nums_category.append(p[1])

    sql = "select movie_score,sum(movie_vote) from pythonMovie group by movie_score"

    cur.execute(sql)
    sandian = cur.fetchall()

    sql = 'select substr(movie_year,1,4),sum(movie_vote) from pythonMovie where movie_score <= 8.0 group by substr(movie_year,1,4)'
    cur.execute(sql)
    datamin = cur.fetchall()

    sql = 'select substr(movie_year,1,4),sum(movie_vote) from pythonMovie where movie_score > 8.0 group by substr(movie_year,1,4)'
    cur.execute(sql)
    datamax = cur.fetchall()
    con.close()

    con = sqlite3.connect("database/sentiment.db")
    cur = con.cursor()
    cur.execute("select movie_score,comments_ave_score from sentiment_score")
    comments_score_data = cur.fetchall()
    comments_score_data = [[x[1], x[0]] for x in comments_score_data]
    con.close()
    # print(comments_score_data)

    con = sqlite3.connect("database/pythonMovie.db")
    cur = con.cursor()
    cur.execute(
        "select movieWatched,movieWanttw from pythonMovie where movieWatched!=0 order by movie_score desc limit 200")
    movie_ww_data = cur.fetchall()
    movie_ww_data = [[x[0], x[1]] for x in movie_ww_data]
    con.close()

    return render_template("score.html", score1=score1, num1=num1, res1=res1, movie_num1=movie_num1,
                           movie_year1=movie_year1,
                           num2=num2, score2=score2, res2=res2, movie_num2=movie_num2, movie_year2=movie_year2,
                           res3=res3, movie_country=movie_country, nums_country=nums_country,
                           movie_category=movie_category, nums_category=nums_category, sandians=sandian,
                           datamax=datamax, datamin=datamin, result=lresult, comments_score_data=comments_score_data,
                           movie_ww_data=movie_ww_data)
