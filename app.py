import base64
import datetime
import io
import os
import sqlite3
from collections import Counter  # 统计字频

import jieba
from PIL import Image
from flask import Flask, send_file
from flask import render_template, request, redirect, url_for, jsonify, abort
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from flask_cors import CORS

from newAnwser import main_ai

app = Flask(__name__)
jieba.load_userdict('./selfDefiningTxt.txt')

# 允许所有域名访问
CORS(app)

app.secret_key = 'tianqingbin'
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):
    def __init__(self, userid, username):
        self.id = userid
        self.userid = userid
        self.username = username

    def __repr__(self):
        return self.userid


@app.route("/")
def home():
    return render_template("login.html")


@app.route('/logout', methods=['POST', 'PUT'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    db = sqlite3.connect("database/userInfo.db")
    username = request.form["username"]
    password = request.form["password"]
    cursor = db.cursor()
    query = "SELECT * FROM usertable WHERE username=?"
    params = (username,)
    cursor.execute(query, params)
    user = cursor.fetchone()
    if user is None:
        error_message = "账号不存在！"
        return render_template("login.html", error=error_message)

    if not check_password_hash(user[2], password):
        error_message = "密码错误，请重试！"
        return render_template("login.html", error=error_message)
    db = sqlite3.connect("database/userInfo.db")
    query = "SELECT id FROM usertable WHERE username=?"
    params = (username,)
    cursor.execute(query, params)
    userid = cursor.fetchone()[0]
    # print(userid)
    user = User(userid, username)
    login_user(user)
    db.close()

    # 获取当前日期
    current_date = datetime.datetime.now().date()
    date_string = current_date.strftime('%Y-%m-%d')

    con = sqlite3.connect('database/pythonMovie.db')
    # 获取cursor对象
    cur = con.cursor()
    # 查询数据库中是否已经存在对应用户ID和日期的记录
    cur.execute('SELECT * FROM login_times WHERE userId = ? AND date = ?', (current_user.userid, date_string))
    row = cur.fetchone()
    if row:
        # 如果记录已存在，则将对应用户ID和日期的登录次数加1
        cur.execute('UPDATE login_times SET count = count + 1 WHERE userId = ? AND date = ?',
                    (current_user.userid, date_string))
        con.commit()
    else:
        # 如果记录不存在，则在数据库中插入一条新记录，用户ID、日期和登录次数初始值为1
        cur.execute('INSERT INTO login_times (userId, date, count) VALUES (?, ?, ?)',
                    (current_user.userid, date_string, 1))
        con.commit()
    # 关闭游标
    cur.close()
    # 关闭连接
    con.close()
    return redirect(url_for('index'))


@app.route('/get_avatar')
@login_required
def get_avatar():
    return send_file(f"static/assets/avatar/avatar_{current_user.id}.png")


@app.route("/check_username", methods=["POST"])
def check_username():
    db = sqlite3.connect("database/userInfo.db")
    username = request.form["username"]
    cursor = db.cursor()
    query = "SELECT * FROM usertable WHERE username=?"
    params = (username,)
    cursor.execute(query, params)
    user = cursor.fetchone()
    exists = user is not None
    return jsonify({"exists": exists})


@app.route("/check_username_afterLogin", methods=["POST"])
def check_username_afterLogin():
    db = sqlite3.connect("database/userInfo.db")
    username = request.form["username"]
    cursor = db.cursor()
    cursor.execute('select * from usertable where username = ? and id != ?', (username, current_user.userid))
    user = cursor.fetchone()
    exists = user is not None
    return jsonify({"exists": exists})


@app.route("/check_phone", methods=["POST"])
def check_phone():
    db = sqlite3.connect("database/userInfo.db")
    phone = request.form["phone"]
    cursor = db.cursor()
    query = "SELECT * FROM usertable WHERE phone=?"
    params = (phone,)
    cursor.execute(query, params)
    user = cursor.fetchone()
    exists = user is not None
    return jsonify({"exists": exists})


@app.route("/check_email", methods=["POST"])
def check_email():
    db = sqlite3.connect("database/userInfo.db")
    email = request.form["email"]
    cursor = db.cursor()
    query = "SELECT * FROM usertable WHERE email=?"
    params = (email,)
    cursor.execute(query, params)
    user = cursor.fetchone()
    exists = user is not None
    return jsonify({"exists": exists})


@app.route("/register", methods=["POST"])
def register():
    db = sqlite3.connect("database/userInfo.db")
    username = request.form["username"]
    password = request.form["r_password"]
    cpassword = request.form["cpassword"]
    hashed_password = generate_password_hash(password)
    cursor = db.cursor()
    sql = "SELECT * FROM usertable WHERE username=?"
    params = (username,)
    cursor.execute(sql, params)
    user = cursor.fetchone()
    is_admin = 0
    if user or (password != cpassword):
        error_message = "注册失败，请按要求填写！"
        return render_template("login.html", error=error_message)
    else:
        query = "INSERT INTO usertable (username, password, is_admin) VALUES (?, ?, ?)"
        params = (username, hashed_password, is_admin)
        cursor.execute(query, params)
        query = "SELECT id FROM usertable WHERE username=?"
        params = (username,)
        cursor.execute(query, params)
        user_id = cursor.fetchone()[0]
        default_avatar_path = os.path.join(app.static_folder, "assets", "avatar", "avatar_default.png")
        default_avatar = Image.open(default_avatar_path)
        new_avatar_filename = "avatar_{}.png".format(user_id)
        new_avatar_path = os.path.join(app.static_folder, "assets", "avatar", new_avatar_filename)
        default_avatar.save(new_avatar_path)
        db.commit()
        db.close()
        error_message = "注册成功，请登录！"
        return render_template("login.html", error=error_message)


@app.route('/index')
@login_required
def index():
    # 1.硬盘上创建连接
    con = sqlite3.connect('database/pythonMovie.db')
    # 获取cursor对象
    cur = con.cursor()
    # 执行sql创建表
    sql = 'select * from pythonMovie'
    cur.execute(sql)
    # 获取所有数据
    person_all = cur.fetchall()
    # 关闭游标
    cur.close()
    # 关闭连接
    con.close()

    con = sqlite3.connect('database/pythonMovie.db')
    # 获取cursor对象
    cur = con.cursor()

    cur.execute('select date,count from login_times where userId = ?', (current_user.userid,))
    data = cur.fetchall()
    data_list = [list(item) for item in data]
    # print(data_list)
    # 关闭游标
    cur.close()
    # 关闭连接
    con.close()

    return render_template("index.html", nums=len(person_all), userId=current_user.userid, data=data_list)


@app.route('/movie')
@login_required
def movie():
    datalist = []
    con = sqlite3.connect("database/movie.db")
    cur = con.cursor()
    sql = "select * from movie250"
    data = cur.execute(sql)
    for item in data:
        datalist.append(item)
    cur.close()
    con.close()
    # print(datalist)
    return render_template("movie.html", movies=datalist)


@app.route('/pMovie')
@login_required
def pmovie():
    return render_template("pMovie.html")


@app.route('/get_movies_data', methods=['POST', 'PUT', 'GET'])
def get_movies_data():
    # 获取电影数据并将其以JSON格式返回
    con = sqlite3.connect("database/pythonMovie.db")
    cur = con.cursor()
    sql = "select * from pythonMovie"
    rows = cur.execute(sql)

    i = 1
    movies = []
    for row in rows:
        movie = {
            'id': i,
            'name': row[2],
            'year': row[3],
            'vote': row[4],
            'score': row[5],
            'link': row[6],
            'category': row[7],
            'country': row[8],
            'comment': row[9],
            'evaluation': row[10]
        }
        i = i + 1
        movies.append(movie)
    # 关闭游标和连接
    cur.close()
    con.close()
    movies_data = {'movies': movies}
    # print(movies_data)
    return jsonify(movies_data)


@app.route('/score')
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


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    return render_template("search.html")


@app.route('/search_results', methods=['GET', 'POST'])
@login_required
def search_results():
    # 从查询字符串参数中获取搜索条件
    keyword = request.args.get('keyword')
    category = request.args.get('category')
    movie_score = request.args.get('movie_score')
    movie_vote = request.args.get('movie_vote')
    movie_year = request.args.get('movie_year')
    country = request.args.get('country')
    limit = request.args.get('limit')
    conn = sqlite3.connect('database/pythonMovie.db')
    cursor = conn.cursor()
    query = "SELECT * FROM pythonMovie WHERE (movie_cname LIKE ? OR director LIKE ? OR movieSummary LIKE ? OR actors LIKE ?)"
    params = ('%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%')

    if category:
        query += " AND category LIKE ?"
        params += ('%' + category + '%',)

    if movie_score:
        query += " AND movie_score >= ?"
        params += (movie_score,)

    if movie_vote:
        query += " AND movie_vote >= ?"
        params += (movie_vote,)

    if movie_year:
        query += " AND movie_year LIKE ?"
        params += ('%' + movie_year + '%',)

    if country:
        query += " AND country LIKE ?"
        params += ('%' + country + '%',)

    query += " LIMIT ?"
    params += (limit,)

    movies = cursor.execute(query, params).fetchall()

    cursor.close()
    conn.close()
    return jsonify(movies)


@app.route('/detailed_charts')
@login_required
def detailed_charts():
    return render_template("detailed_charts.html")


@app.route('/get_chart_data', methods=['POST'])
@login_required
def get_chart_data():
    year = request.form['year']
    category = request.form['category']
    top_num = request.form['top_num']

    # 从数据库中获取电影数据
    conn = sqlite3.connect('database/pythonMovie.db')
    c = conn.cursor()
    if category == 'box_office':
        c.execute(
            'SELECT movie_cname, movie_vote FROM pythonMovie WHERE movie_year LIKE ? ORDER BY movie_vote DESC LIMIT ?',
            (year + '%', top_num))
        movie_data = c.fetchall()
    elif category == 'score':
        c.execute(
            'SELECT movie_cname, movie_score FROM pythonMovie WHERE movie_year LIKE ? ORDER BY movie_score DESC LIMIT ?',
            (year + '%', top_num))
        movie_data = c.fetchall()
    elif category == 'num_comments':
        c.execute('SELECT movie_cname, comment FROM pythonMovie WHERE movie_year LIKE ? ORDER BY comment DESC LIMIT ?',
                  (year + '%', top_num))
        movie_data = c.fetchall()
    elif category == 'num_ratings':
        c.execute(
            'SELECT movie_cname, evaluation FROM pythonMovie WHERE movie_year LIKE ? ORDER BY evaluation DESC LIMIT ?',
            (year + '%', top_num))
        movie_data = c.fetchall()
    elif category == 'num_watched':
        c.execute(
            'SELECT movie_cname, movieWatched FROM pythonMovie WHERE movie_year LIKE ? ORDER BY movieWatched DESC LIMIT ?',
            (year + '%', top_num))
        movie_data = c.fetchall()
    elif category == 'num_wanted':
        c.execute(
            'SELECT movie_cname, movieWanttw FROM pythonMovie WHERE movie_year LIKE ? ORDER BY movieWanttw DESC LIMIT ?',
            (year + '%', top_num))
        movie_data = c.fetchall()
    else:
        movie_data = []

    c.close()
    conn.close()

    movie_chart_data = []
    for movie in movie_data:
        movie_chart_data.append({'value': movie[1], 'name': movie[0]})
    return jsonify(movie_chart_data)


@app.route('/get_chart_data_line', methods=['POST'])
@login_required
def get_chart_data_line():
    yearFrom = request.form['yearFrom']
    yearTo = request.form['yearTo']
    category = request.form['category']
    select_type = request.form['type']

    # 从数据库中获取电影数据
    conn = sqlite3.connect('database/pythonMovie.db')
    c = conn.cursor()

    if category == 'box_office':
        if select_type == 'total-value':
            c.execute(
                "SELECT substr(movie_year,1,4), sum(movie_vote) FROM pythonMovie WHERE substr(movie_year,1,4) >=? and substr(movie_year,1,4)<=? group by substr(movie_year,1,4)",
                (yearFrom, yearTo))
        else:
            c.execute(
                "SELECT substr(movie_year,1,4), avg(movie_vote) FROM pythonMovie WHERE substr(movie_year,1,4) >=? and substr(movie_year,1,4)<=? and movie_vote!=0 group by substr(movie_year,1,4)",
                (yearFrom, yearTo))
        movie_data = c.fetchall()
    elif category == 'num_comments':
        if select_type == 'total-value':
            c.execute(
                "SELECT substr(movie_year,1,4), sum(comment) FROM pythonMovie WHERE substr(movie_year,1,4) >=? and substr(movie_year,1,4)<=? group by substr(movie_year,1,4)",
                (yearFrom, yearTo))
        else:
            c.execute(
                "SELECT substr(movie_year,1,4), avg(comment) FROM pythonMovie WHERE substr(movie_year,1,4) >=? and substr(movie_year,1,4)<=? and comment!=0 group by substr(movie_year,1,4)",
                (yearFrom, yearTo))
        movie_data = c.fetchall()
    elif category == 'num_ratings':
        if select_type == 'total-value':
            c.execute(
                "SELECT substr(movie_year,1,4), sum(evaluation) FROM pythonMovie WHERE substr(movie_year,1,4) >=? and substr(movie_year,1,4)<=? group by substr(movie_year,1,4)",
                (yearFrom, yearTo))
        else:
            c.execute(
                "SELECT substr(movie_year,1,4), avg(evaluation) FROM pythonMovie WHERE substr(movie_year,1,4) >=? and substr(movie_year,1,4)<=? and evaluation!=0 group by substr(movie_year,1,4)",
                (yearFrom, yearTo))
        movie_data = c.fetchall()
    elif category == 'num_watched':
        if select_type == 'total-value':
            c.execute(
                "SELECT substr(movie_year,1,4), sum(movieWatched) FROM pythonMovie WHERE substr(movie_year,1,4) >=? and substr(movie_year,1,4)<=? group by substr(movie_year,1,4)",
                (yearFrom, yearTo))
        else:
            c.execute(
                "SELECT substr(movie_year,1,4), avg(movieWatched) FROM pythonMovie WHERE substr(movie_year,1,4) >=? and substr(movie_year,1,4)<=? and movieWatched!=0 group by substr(movie_year,1,4)",
                (yearFrom, yearTo))
        movie_data = c.fetchall()
    elif category == 'num_wanted':
        if select_type == 'total-value':
            c.execute(
                "SELECT substr(movie_year,1,4), sum(movieWanttw) FROM pythonMovie WHERE substr(movie_year,1,4) >=? and substr(movie_year,1,4)<=? group by substr(movie_year,1,4)",
                (yearFrom, yearTo))
        else:
            c.execute(
                "SELECT substr(movie_year,1,4), avg(movieWanttw) FROM pythonMovie WHERE substr(movie_year,1,4) >=? and substr(movie_year,1,4)<=? and movieWanttw!=0 group by substr(movie_year,1,4)",
                (yearFrom, yearTo))
        movie_data = c.fetchall()
    else:
        movie_data = []

    # print(movie_data)

    c.close()
    conn.close()

    return jsonify(movie_data)


@app.route('/get_chart_data_month', methods=['POST'])
@login_required
def get_chart_data_month():
    year = request.form['year']
    # 从数据库中获取电影数据
    conn = sqlite3.connect('database/pythonMovie.db')
    c = conn.cursor()
    c.execute(
        'SELECT substr(movie_year,6,2), count(*), sum(movie_vote), sum(comment), sum(evaluation) FROM pythonMovie WHERE movie_year LIKE ? group BY substr(movie_year,6,2)',
        (year + '%',))
    movie_data = c.fetchall()
    c.close()
    conn.close()
    # print(movie_data)
    return jsonify(movie_data)


@app.route('/get_chart_data_people', methods=['POST'])
@login_required
def get_chart_data_people():
    people = request.form['people']
    category = request.form['category']
    type = request.form['type']
    top_num = request.form['top_num']
    conn = sqlite3.connect('database/pythonMovie.db')
    c = conn.cursor()

    if people == 'director':
        if category == 'movie_nums':
            c.execute('select director_name, movie_nums from directors order by movie_nums desc limit ?', (top_num,))
            people_data = c.fetchall()
        elif category == 'movie_score':
            c.execute(
                'select director_name, avg(movie_score) from directors,movies_director,pythonMovie where directors.director_id=movies_director.director_id and movies_director.movie_id=pythonMovie.movie_id group by director_name order by avg(movie_score) desc limit ?',
                (top_num,))
            people_data = c.fetchall()
        else:
            if type == 'total-value':
                c.execute(
                    f'select director_name, sum({category}) from directors,movies_director,pythonMovie where directors.director_id=movies_director.director_id and movies_director.movie_id=pythonMovie.movie_id group by director_name order by sum({category}) desc limit {top_num}'
                )
                people_data = c.fetchall()
            else:
                c.execute(
                    f'select director_name, avg({category}) from directors,movies_director,pythonMovie where directors.director_id=movies_director.director_id and movies_director.movie_id=pythonMovie.movie_id group by director_name order by avg({category}) desc limit {top_num}'
                )
                people_data = c.fetchall()
    else:
        if category == 'movie_nums':
            c.execute('select actor_name, movie_nums from actors order by movie_nums desc limit ?', (top_num,))
            people_data = c.fetchall()
        elif category == 'movie_score':
            c.execute(
                'select actor_name, avg(movie_score) from actors,movies_actor,pythonMovie where actors.actor_id=movies_actor.actor_id and movies_actor.movie_id=pythonMovie.movie_id group by actor_name order by avg(movie_score) desc limit ?',
                (top_num,))
            people_data = c.fetchall()
        else:
            if type == 'total-value':
                c.execute(
                    f'select actor_name, sum({category}) from actors,movies_actor,pythonMovie where actors.actor_id=movies_actor.actor_id and movies_actor.movie_id=pythonMovie.movie_id group by actor_name order by sum({category}) desc limit {top_num}'
                )
                people_data = c.fetchall()
            else:
                c.execute(
                    f'select actor_name, avg({category}) from actors,movies_actor,pythonMovie where actors.actor_id=movies_actor.actor_id and movies_actor.movie_id=pythonMovie.movie_id and actors.movie_nums>5 group by actor_name order by avg({category}) desc limit {top_num}'
                )
                people_data = c.fetchall()

    people_chart_data = []
    for people in people_data:
        people_chart_data.append({'value': people[1], 'name': people[0]})
    return jsonify(people_chart_data)


@app.route('/cloud')
@login_required
def word():
    return render_template("cloud.html")


# @app.route("/generate_wordcloud", methods=["POST"])
# def generate_wordcloud():
#     movie_name = request.form.get("movie_name")
#
#     con = sqlite3.connect('database/pythonMovie.db')
#     cur = con.cursor()
#     cur.execute(
#         'SELECT comments.comments FROM comments INNER JOIN pythonMovie ON pythonMovie.movie_id=comments.movie_id WHERE pythonMovie.movie_cname=?',
#         (movie_name,))
#     data = cur.fetchall()
#     text = ""
#     for item in data:
#         text = text + item[0]
#     text = re.findall(r'[\u4e00-\u9fa5]', text)
#     chinese_text = ''.join(text)
#     cut = jieba.cut(chinese_text)
#     comments = ' '.join(cut)
#     # 删除单字
#     comments = " ".join(word for word in comments.split() if len(word) > 1)
#     if len(comments) == 0:
#         comments = movie_name
#
#     img = Image.open(r'.\static\assets\img\tree.jpg')  # 打开遮罩图片
#     img_array = np.array(img)  # 将图片转换为数组
#
#     wc = WordCloud(
#         width=800,  # 设置词云图的宽度为800像素
#         height=400,  # 设置词云图的高度为400像素
#         background_color='white',
#         mask=img_array,
#         font_path="msyh.ttc"  # 字体所在位置：C:\Windows\Fonts
#     )
#     wc.generate_from_text(comments)
#
#     plt.imshow(wc)
#     plt.axis('off')  # 是否显示坐标轴
#
#     # 将生成的词云图转换为base64格式
#     buffer = BytesIO()
#     plt.savefig(buffer, format="png")
#     buffer.seek(0)
#     img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
#     cur.close()
#     con.close()
#     # 在后端显示词云图
#     return {"wordcloud": '<img src="data:image/png;base64,{}">'.format(img_base64)}


@app.route("/generate_wordcloud", methods=["POST"])
def generate_wordcloud():
    movie_name = request.form.get("movie_name")

    # 连接数据库
    con = sqlite3.connect('database/pythonMovie.db')
    cur = con.cursor()
    cur.execute('select movie_id from pythonMovie where movie_cname=?', (movie_name,))
    result = cur.fetchone()
    if result is not None:
        movie_id = result[0]
    else:
        movie_id = 1

    cur.close()
    con.close()

    con = sqlite3.connect('database/cloud.db')
    cur = con.cursor()
    cur.execute('select comments_wordcloud_data,reviews_wordcloud_data from cloud where movie_id=?', (movie_id,))
    data = cur.fetchone()

    if data is not None and data[0] is not None:
        # 获取词云图的二进制数据
        img_data = data[0]
        img_data1 = data[1]

        # 将二进制数据转换为base64格式
        img_base64 = base64.b64encode(img_data).decode("utf-8")
        img_base641 = base64.b64encode(img_data1).decode("utf-8")

        # 构建返回给前端的数据
        result = {
            'wordcloud': '<img src="data:image/png;base64,{}" style="width:100%;">'.format(img_base64),
            'wordcloud1': '<img src="data:image/png;base64,{}" style="width:100%;">'.format(img_base641)
        }

        cur.close()
        con.close()

        # 返回词云图的base64数据给前端
        # return {"wordcloud": '<img src="data:image/png;base64,{}">'.format(img_base64)}
        return result
    else:
        # 数据库中没有词云图数据
        return {"wordcloud": None, "wordcloud1": None}


@app.route('/sentiment')
@login_required
def sentiment():
    return render_template("sentiment.html")


@app.route('/analyze_sentiment', methods=['POST'])
@login_required
def analyze_sentiment():
    # 获取前端传入的电影名
    movie_name = request.form.get('movie_name')

    # 连接数据库并查询电影评论
    con = sqlite3.connect('database/pythonMovie.db')
    cur = con.cursor()
    cur.execute('select movie_id from pythonMovie where movie_cname=?', (movie_name,))
    result = cur.fetchone()
    if result is not None:
        movie_id = result[0]
    else:
        movie_id = 1

    con.close()

    con = sqlite3.connect('database/sentiment.db')
    cur = con.cursor()
    cur.execute('select positive_count,neutral_count,negative_count from comments_sentiment where movie_id = ?',
                (movie_id,))
    data = cur.fetchone()

    # 对评论进行情感分析并统计情感得分区间
    positive_count = 0
    neutral_count = 0
    negative_count = 0
    if data:
        positive_count = data[0]
        neutral_count = data[1]
        negative_count = data[2]

    cur.execute(
        'select comments_ave_score,comments_max_score,comments_min_score from sentiment_score where movie_id = ?',
        (movie_id,))
    comments_data = cur.fetchone()

    comments_ave_score = 0
    comments_max_score = 0
    comments_min_score = 0

    if comments_data:
        comments_ave_score = comments_data[0]
        comments_max_score = comments_data[1]
        comments_min_score = comments_data[2]

    # 构建返回给前端的数据
    result = {
        'positive_count': positive_count,
        'neutral_count': neutral_count,
        'negative_count': negative_count,
        'comments_ave_score': comments_ave_score,
        'comments_max_score': comments_max_score,
        'comments_min_score': comments_min_score
    }
    con.close()
    return jsonify(result)


@app.route('/reviews_analyze_sentiment', methods=['POST'])
@login_required
def reviews_analyze_sentiment():
    # 获取前端传入的电影名
    movie_name = request.form.get('movie_name')

    # 连接数据库并查询电影评论
    con = sqlite3.connect('database/pythonMovie.db')
    cur = con.cursor()
    cur.execute('select movie_id from pythonMovie where movie_cname=?', (movie_name,))
    result = cur.fetchone()
    if result is not None:
        movie_id = result[0]
    else:
        movie_id = 1
    con.close()

    con = sqlite3.connect('database/sentiment.db')
    cur = con.cursor()
    cur.execute('select positive_count,neutral_count,negative_count from reviews_sentiment where movie_id = ?',
                (movie_id,))
    data = cur.fetchone()

    # 对评论进行情感分析并统计情感得分区间
    positive_count = 0
    neutral_count = 0
    negative_count = 0

    if data:
        positive_count = data[0]
        neutral_count = data[1]
        negative_count = data[2]

    cur.execute('select reviews_ave_score,reviews_max_score,reviews_min_score from sentiment_score where movie_id = ?',
                (movie_id,))
    reviews_data = cur.fetchone()

    reviews_ave_score = 0
    reviews_max_score = 0
    reviews_min_score = 0

    if reviews_data:
        reviews_ave_score = reviews_data[0]
        reviews_max_score = reviews_data[1]
        reviews_min_score = reviews_data[2]

    con.close()

    # 构建返回给前端的数据
    result = {
        'positive_count': positive_count,
        'neutral_count': neutral_count,
        'negative_count': negative_count,
        'reviews_ave_score': reviews_ave_score,
        'reviews_max_score': reviews_max_score,
        'reviews_min_score': reviews_min_score
    }

    return jsonify(result)


@app.route('/bar_analyze_sentiment', methods=['POST', 'GET'])
@login_required
def bar_analyze_sentiment():
    # 获取前端传入的电影名
    movie_name = request.form.get('movie_name')
    # 连接数据库并查询电影评论
    con = sqlite3.connect('database/pythonMovie.db')
    cur = con.cursor()
    cur.execute('select movie_id from pythonMovie where movie_cname=?', (movie_name,))
    result = cur.fetchone()
    if result is not None:
        movie_id = result[0]
    else:
        movie_id = 1
    con.close()

    con = sqlite3.connect('database/sentiment.db')
    cur = con.cursor()
    cur.execute(
        'select positive_count,neutral_count,negative_count,very_positive_count,very_negative_count from bar_comments_sentiment where movie_id = ?',
        (movie_id,))
    data = cur.fetchone()

    # 对评论进行情感分析并统计情感得分区间
    positive_count = 0
    neutral_count = 0
    negative_count = 0
    very_positive_count = 0
    very_negative_count = 0

    if data:
        positive_count = data[0]
        neutral_count = data[1]
        negative_count = data[2]
        very_positive_count = data[3]
        very_negative_count = data[4]

    con.close()

    # 构建返回给前端的数据
    result = {
        'positive_count': positive_count,
        'neutral_count': neutral_count,
        'negative_count': negative_count,
        'very_positive_count': very_positive_count,
        'very_negative_count': very_negative_count
    }
    # print(result)

    return jsonify(result)


@app.route('/bar_reviews_analyze_sentiment', methods=['POST', 'GET'])
@login_required
def bar_reviews_analyze_sentiment():
    # 获取前端传入的电影名
    movie_name = request.form.get('movie_name')
    # 连接数据库并查询电影评论
    con = sqlite3.connect('database/pythonMovie.db')
    cur = con.cursor()
    cur.execute('select movie_id from pythonMovie where movie_cname=?', (movie_name,))
    result = cur.fetchone()
    if result is not None:
        movie_id = result[0]
    else:
        movie_id = 1
    con.close()

    con = sqlite3.connect('database/sentiment.db')
    cur = con.cursor()
    cur.execute(
        'select positive_count,neutral_count,negative_count,very_positive_count,very_negative_count from bar_reviews_sentiment where movie_id = ?',
        (movie_id,))
    data = cur.fetchone()

    # 对评论进行情感分析并统计情感得分区间
    positive_count = 0
    neutral_count = 0
    negative_count = 0
    very_positive_count = 0
    very_negative_count = 0

    if data:
        positive_count = data[0]
        neutral_count = data[1]
        negative_count = data[2]
        very_positive_count = data[3]
        very_negative_count = data[4]

    con.close()

    # 构建返回给前端的数据
    result = {
        'positive_count': positive_count,
        'neutral_count': neutral_count,
        'negative_count': negative_count,
        'very_positive_count': very_positive_count,
        'very_negative_count': very_negative_count
    }
    # print(result)

    return jsonify(result)


@app.route('/movieCompare')
@login_required
def movieCompare():
    return render_template("movieCompare.html")


# 定义获取所有电影的路由
@app.route("/get_all_movies", methods=["POST", "GET"])
def get_all_movies():
    conn = sqlite3.connect("database/pythonMovie.db")
    cur = conn.cursor()
    cur.execute("SELECT movie_id,movie_cname FROM pythonMovie limit 100")
    movies = [{'movie_id': row[0], 'movie_cname': row[1]} for row in cur.fetchall()]
    conn.close()
    return jsonify({'movies': movies})


# 定义获取所有导演的路由
@app.route("/get_all_directors", methods=["POST", "GET"])
def get_all_directors():
    conn = sqlite3.connect("database/pythonMovie.db")
    cur = conn.cursor()
    cur.execute("SELECT director_id,director_name FROM directors where movie_nums>=3 limit 100")
    directors = [{'director_id': row[0], 'director_name': row[1]} for row in cur.fetchall()]
    conn.close()
    return jsonify({'directors': directors})


# 定义获取所有演员的路由
@app.route("/get_all_actors", methods=["POST", "GET"])
def get_all_actors():
    conn = sqlite3.connect("database/pythonMovie.db")
    cur = conn.cursor()
    cur.execute("SELECT actor_id,actor_name FROM actors where movie_nums>=5 limit 100")
    actors = [{'actor_id': row[0], 'actor_name': row[1]} for row in cur.fetchall()]
    conn.close()
    return jsonify({'actors': actors})


# 定义对比两个电影的路由
@app.route("/compare_movies", methods=["POST"])
def compare_movies():
    movie_id_1 = request.form.get("movie_id_1")
    movie_id_2 = request.form.get("movie_id_2")
    conn = sqlite3.connect("database/pythonMovie.db")
    c = conn.cursor()
    # 查询第一个电影的数据
    c.execute("SELECT * FROM pythonMovie WHERE movie_id = ?", (movie_id_1,))
    movie1 = c.fetchone()
    # 查询第二个电影的数据
    c.execute("SELECT * FROM pythonMovie WHERE movie_id = ?", (movie_id_2,))
    movie2 = c.fetchone()
    conn.close()
    # 构造返回数据

    movie1_nums = 0
    movie2_nums = 0
    if movie1 and movie2:
        for i in [4, 5, 9, 10, 13, 14]:
            if movie1[i] > movie2[i]:
                movie1_nums += 1
            elif movie1[i] < movie2[i]:
                movie2_nums += 1
    if not movie1 or not movie2:
        return jsonify({"movie1": {
            "name": '--',
            "score": '--',
            "box_office": '--',
            "type": '--',
            "release_time": '--',
            "comments_nums": '--',
            "evaluation_nums": '--',
            "movieWatched_nums": '--',
            "movieWanttw_nums": '--',
            "moviegreater": '--'
            # 其他数据...
        },
            "movie2": {
                "name": '--',
                "score": '--',
                "box_office": '--',
                "type": '--',
                "release_time": '--',
                "comments_nums": '--',
                "evaluation_nums": '--',
                "movieWatched_nums": '--',
                "movieWanttw_nums": '--',
                "moviegreater": '--'
                # 其他数据...
            }
        })
    data = {
        "movie1": {
            "name": movie1[2],
            "score": movie1[5],
            "box_office": movie1[4],
            "type": movie1[7],
            "release_time": movie1[3],
            "comments_nums": movie1[9],
            "evaluation_nums": movie1[10],
            "movieWatched_nums": movie1[13],
            "movieWanttw_nums": movie1[14],
            "moviegreater": movie1_nums
            # 其他数据...
        },
        "movie2": {
            "name": movie2[2],
            "score": movie2[5],
            "box_office": movie2[4],
            "type": movie2[7],
            "release_time": movie2[3],
            "comments_nums": movie2[9],
            "evaluation_nums": movie2[10],
            "movieWatched_nums": movie2[13],
            "movieWanttw_nums": movie2[14],
            "moviegreater": movie2_nums
            # 其他数据...
        }
    }
    return jsonify(data)


# 定义对比两个导演的路由
@app.route("/compare_directors", methods=["POST"])
def compare_directors():
    director_id_1 = request.form.get("director_id_1")
    director_id_2 = request.form.get("director_id_2")
    conn = sqlite3.connect("database/pythonMovie.db")
    c = conn.cursor()
    # 查询第一个电影的数据
    c.execute(
        "SELECT director_name, round(avg(movie_score), 1), movie_nums, round(avg(movie_vote)), round(avg(comment)), round(avg(evaluation)), round(avg(movieWatched)), round(avg(movieWanttw)) FROM pythonMovie,directors,movies_director where directors.director_id=movies_director.director_id and movies_director.movie_id=pythonMovie.movie_id and directors.director_id=?",
        (director_id_1,))
    director1 = c.fetchone()
    # 查询第二个电影的数据
    c.execute(
        "SELECT director_name, round(avg(movie_score), 1), movie_nums, round(avg(movie_vote)), round(avg(comment)), round(avg(evaluation)), round(avg(movieWatched)), round(avg(movieWanttw)) FROM pythonMovie,directors,movies_director where directors.director_id=movies_director.director_id and movies_director.movie_id=pythonMovie.movie_id and directors.director_id=?",
        (director_id_2,))
    director2 = c.fetchone()
    conn.close()
    # 构造返回数据

    director1_nums = 0
    director2_nums = 0
    if None not in director1 and None not in director2:
        for i in range(1, 7):
            if director1[i] > director2[i]:
                director1_nums += 1
            elif director1[i] < director2[i]:
                director2_nums += 1
    if None in director1 or None in director2:
        return jsonify({"director1": {
            "name": '--',
            "score": '--',
            "movienums": '--',
            "box_office": '--',
            "comments_nums": '--',
            "evaluation_nums": '--',
            "movieWatched_nums": '--',
            "movieWanttw_nums": '--',
            "directorgreater": '--'
            # 其他数据...
        },
            "director2": {
                "name": '--',
                "score": '--',
                "movienums": '--',
                "box_office": '--',
                "comments_nums": '--',
                "evaluation_nums": '--',
                "movieWatched_nums": '--',
                "movieWanttw_nums": '--',
                "directorgreater": '--'
                # 其他数据...
            }
        })
    data = {
        "director1": {
            "name": director1[0],
            "score": director1[1],
            "movienums": director1[2],
            "box_office": director1[3],
            "comments_nums": director1[4],
            "evaluation_nums": director1[5],
            "movieWatched_nums": director1[6],
            "movieWanttw_nums": director1[7],
            "directorgreater": director1_nums
            # 其他数据...
        },
        "director2": {
            "name": director2[0],
            "score": director2[1],
            "movienums": director2[2],
            "box_office": director2[3],
            "comments_nums": director2[4],
            "evaluation_nums": director2[5],
            "movieWatched_nums": director2[6],
            "movieWanttw_nums": director2[7],
            "directorgreater": director2_nums
            # 其他数据...
        }
    }
    return jsonify(data)


# 定义对比两个演员的路由
@app.route("/compare_actors", methods=["POST"])
def compare_actors():
    actor_id_1 = request.form.get("actor_id_1")
    actor_id_2 = request.form.get("actor_id_2")
    conn = sqlite3.connect("database/pythonMovie.db")
    c = conn.cursor()
    # 查询第一个电影的数据
    c.execute(
        "SELECT actor_name, round(avg(movie_score), 1), movie_nums, round(avg(movie_vote)), round(avg(comment)), round(avg(evaluation)), round(avg(movieWatched)), round(avg(movieWanttw)) FROM pythonMovie,actors,movies_actor where actors.actor_id=movies_actor.actor_id and movies_actor.movie_id=pythonMovie.movie_id and actors.actor_id=?",
        (actor_id_1,))
    actor1 = c.fetchone()
    # 查询第二个电影的数据
    c.execute(
        "SELECT actor_name, round(avg(movie_score), 1), movie_nums, round(avg(movie_vote)), round(avg(comment)), round(avg(evaluation)), round(avg(movieWatched)), round(avg(movieWanttw)) FROM pythonMovie,actors,movies_actor where actors.actor_id=movies_actor.actor_id and movies_actor.movie_id=pythonMovie.movie_id and actors.actor_id=?",
        (actor_id_2,))
    actor2 = c.fetchone()
    conn.close()
    # 构造返回数据

    actor1_nums = 0
    actor2_nums = 0
    if None not in actor1 and None not in actor2:
        for i in range(1, 7):
            if actor1[i] > actor2[i]:
                actor1_nums += 1
            elif actor1[i] < actor2[i]:
                actor2_nums += 1
    if None in actor1 or None in actor2:
        return jsonify({"actor1": {
            "name": '--',
            "score": '--',
            "movienums": '--',
            "box_office": '--',
            "comments_nums": '--',
            "evaluation_nums": '--',
            "movieWatched_nums": '--',
            "movieWanttw_nums": '--',
            "directorgreater": '--'
            # 其他数据...
        },
            "actor2": {
                "name": '--',
                "score": '--',
                "movienums": '--',
                "box_office": '--',
                "comments_nums": '--',
                "evaluation_nums": '--',
                "movieWatched_nums": '--',
                "movieWanttw_nums": '--',
                "directorgreater": '--'
                # 其他数据...
            }
        })
    data = {
        "actor1": {
            "name": actor1[0],
            "score": actor1[1],
            "movienums": actor1[2],
            "box_office": actor1[3],
            "comments_nums": actor1[4],
            "evaluation_nums": actor1[5],
            "movieWatched_nums": actor1[6],
            "movieWanttw_nums": actor1[7],
            "actorgreater": actor1_nums
            # 其他数据...
        },
        "actor2": {
            "name": actor2[0],
            "score": actor2[1],
            "movienums": actor2[2],
            "box_office": actor2[3],
            "comments_nums": actor2[4],
            "evaluation_nums": actor2[5],
            "movieWatched_nums": actor2[6],
            "movieWanttw_nums": actor2[7],
            "actorgreater": actor2_nums
            # 其他数据...
        }
    }
    return jsonify(data)


@app.route('/team')
@login_required
def team():
    return render_template("team.html")


@app.route('/aboutMe')
@login_required
def aboutMe():
    return render_template("aboutMe.html")


@app.route('/answerQuestion')
@login_required
def answerQuestion():
    return render_template("answerQuestion.html", user_id=current_user.id)


@app.route('/historyAnswer')
@login_required
def historyAnswer():
    conn = sqlite3.connect('database/userInfo.db')
    c = conn.cursor()
    c.execute('select * from chatHistory where userId = ?', (current_user.userid,))
    result = c.fetchall()

    # 将查询结果转换成列表
    questions = []
    for row in result:
        questions.append({
            'question': row[2],
            'answer': row[3],
            'time': row[4]
        })
    c.close()
    conn.close()
    # print(questions)
    return render_template("historyAnswer.html", questions=questions)


@app.route('/execute', methods=['POST'])
def execute():
    code = request.form['message']
    out = main_ai(code)
    conn = sqlite3.connect("database/userInfo.db")
    c = conn.cursor()
    c.execute('INSERT INTO chatHistory (userId, question, answer) VALUES (?, ?, ?)', (current_user.userid, code, out))
    conn.commit()
    c.close()
    conn.close()
    return out


@app.route('/personInfo')
@login_required
def personInfo():
    conn = sqlite3.connect('database/userInfo.db')
    c = conn.cursor()
    c.execute('SELECT * FROM usertable WHERE id=?', (current_user.userid,))
    users = c.fetchone()
    conn.close()
    return render_template("personInfo.html", users=users)


@app.route("/upload_avatar", methods=["POST"])
def upload_avatar():
    # 读取前端传递的Base64编码的字符串，转换为字节流
    image_data = base64.b64decode(request.form['image_data'].split(',')[1])
    if not image_data:
        return jsonify({"success": False, "error": "没有上传文件"})
    # 将字节流转换为图像
    image = Image.open(io.BytesIO(image_data))
    current_user_id = current_user.id
    path = f"static/assets/avatar/avatar_{current_user_id}.png"
    # 保存图像
    image.save(path)
    return jsonify({"success": True})


@app.route('/update1', methods=['POST', 'PUT'])
@login_required
def update1():
    username = request.form['username']
    email = request.form['email']
    phone = request.form['phone']
    gender = request.form['gender']
    hobby = request.form['hobby']
    conn = sqlite3.connect('database/userInfo.db')
    c = conn.cursor()
    c.execute('select * from usertable where username = ? and id != ?', (username, current_user.userid))
    pname = c.fetchone()
    c.execute('select * from usertable where email = ? and id != ?', (email, current_user.userid))
    pemail = c.fetchone()
    c.execute('select * from usertable where phone = ? and id != ?', (phone, current_user.userid))
    pphone = c.fetchone()
    if pname is not None or pemail is not None or pphone is not None:
        message = '修改失败！'
        return jsonify({'message': message})
    c.execute('UPDATE usertable SET username = ?,email = ?,phone = ?,gender = ?,hobby = ? WHERE id = ?',
              (username, email, phone, gender, hobby, current_user.userid))
    conn.commit()
    conn.close()
    message = '修改成功！'
    return jsonify({'message': message})


@app.route('/changepassword', methods=['POST', 'PUT'])
@login_required
def changepassword():
    old_password = request.form['old_password']
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']
    conn = sqlite3.connect('database/userInfo.db')
    c = conn.cursor()
    c.execute('select password from usertable WHERE id = ?', (current_user.userid,))
    hashed_password = c.fetchone()[0]

    if not check_password_hash(hashed_password, old_password):
        message = '原密码错误！'
        return jsonify({'message': message})

    if new_password != confirm_password:
        message = '两次输入的新密码不一致！'
        return jsonify({'message': message})

    new_hashed_password = generate_password_hash(new_password)
    c.execute('UPDATE usertable SET password = ? WHERE id = ?', (new_hashed_password, current_user.userid))
    conn.commit()
    conn.close()

    message = '密码修改成功！'
    return jsonify({'message': message})


@app.route('/reset_password', methods=['POST'])
@login_required
def reset_password():
    conn = sqlite3.connect('database/userInfo.db')
    c = conn.cursor()
    id = request.form['id']
    new_hashed_password = generate_password_hash('h12345678')
    c.execute('UPDATE usertable SET password = ? WHERE id = ?', (new_hashed_password, id))
    conn.commit()
    c.close()
    conn.close()
    message = '密码重置成功！'
    return jsonify({'message': message})


@app.route('/set_admin', methods=['POST'])
@login_required
def set_admin():
    if current_user.userid != 1:
        message = '你没有该权限！'
        return jsonify({'message': message})
    conn = sqlite3.connect('database/userInfo.db')
    c = conn.cursor()
    id = request.form['id']
    c.execute('UPDATE usertable SET is_admin = ? WHERE id = ?', (1, id))
    conn.commit()
    c.close()
    conn.close()
    message = '管理设置成功！'
    return jsonify({'message': message})


@app.route('/cancel_admin', methods=['POST'])
@login_required
def cancel_admin():
    if current_user.userid != 1:
        message = '你没有该权限！'
        return jsonify({'message': message})
    conn = sqlite3.connect('database/userInfo.db')
    c = conn.cursor()
    id = request.form['id']
    c.execute('UPDATE usertable SET is_admin = ? WHERE id = ?', (0, id))
    conn.commit()
    c.close()
    conn.close()
    message = '管理取消成功！'
    return jsonify({'message': message})


@app.route('/delete_user', methods=['POST'])
@login_required
def delete_user():
    if current_user.userid != 1:
        message = '你没有该权限！'
        return jsonify({'message': message})
    conn = sqlite3.connect('database/userInfo.db')
    c = conn.cursor()
    id = request.form['id']
    # 删除用户头像文件
    avatar_path = os.path.join('static', 'assets', 'avatar', 'avatar_{}.png'.format(id))
    if os.path.exists(avatar_path):
        os.remove(avatar_path)
    c.execute('delete from usertable where id = ?', (id,))
    conn.commit()
    c.close()
    conn.close()
    message = '用户删除成功！'
    return jsonify({'message': message})


@app.route('/users')
@login_required
def users():
    if current_user.is_admin != 1:
        abort(403)
    conn = sqlite3.connect('database/userInfo.db')
    c = conn.cursor()
    c.execute('select * from usertable')
    result = c.fetchall()

    # 将查询结果转换成列表
    users = []
    for row in result:
        users.append({
            'id': row[0],
            'username': row[1],
            'email': row[3],
            'phone': row[4],
            'gender': row[5],
            'register_time': row[6],
            'hobby': row[7],
            'is_admin': '是' if row[8] == 1 else '否'
        })
    c.close()
    conn.close()

    return render_template('users.html', users=users)


def get_user_history(id):
    # 假设 user_history 表中保存了用户的历史问答记录，每个记录包含三个字段：question、answer、date
    # 这里使用 SQL 语句从数据库中查询数据
    sql = "SELECT question, answer, timestamp FROM chatHistory WHERE userId = ?"
    conn = sqlite3.connect('database/userInfo.db')
    cur = conn.cursor()
    cur.execute(sql, (id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    # 将查询结果转换为字典列表
    history = [{'question': row[0], 'answer': row[1], 'timestamp': row[2]} for row in rows]
    return history


# 处理 /get_history 路由的请求
@app.route('/get_history', methods=['POST', 'PUT', 'GET'])
@login_required
def get_history():
    id = request.args.get('id')
    # 假设 user 表中保存了用户的信息，每个记录包含四个字段：id、username、email、phone
    # 这里使用 SQL 语句从数据库中查询用户信息
    sql = "SELECT id, username FROM usertable WHERE id = ?"
    conn = sqlite3.connect('database/userInfo.db')
    cur = conn.cursor()
    cur.execute(sql, (id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        # 如果查询到了用户信息，则返回用户的历史问答记录
        history = get_user_history(id)
        return jsonify({'success': True, 'username': row[1], 'history': history})
    else:
        # 如果查询不到用户信息，则返回错误信息
        return jsonify({'success': False, 'message': '用户不存在'})


@app.route('/delete_feedback', methods=['POST'])
@login_required
def delete_feedback():
    feedback_id = request.form.get('feedback_id')
    # print(feedback_id)
    # 连接 SQLite3 数据库
    conn = sqlite3.connect('database/feedback.db')
    c = conn.cursor()

    # 执行 SQL 语句，删除相应的反馈记录
    c.execute('DELETE FROM feedback WHERE id=?', (feedback_id,))

    # 提交事务并关闭数据库连接
    conn.commit()
    conn.close()

    # 返回删除结果给前端
    return jsonify({'success': True})


@app.route('/feedback', methods=['POST'])
@login_required
def handle_feedback():
    subject = request.form.get('subject')
    message = request.form.get('message')

    if subject == "" or message == "":
        message = '信息不能为空!'
        return jsonify({'message': message})

    conn = sqlite3.connect('database/feedback.db')
    c = conn.cursor()
    c.execute("INSERT INTO feedback (userId, userName, subject, message, is_new) VALUES (?, ?, ?, ?,?)",
              (current_user.userid, current_user.username, subject, message, 1))
    conn.commit()
    conn.close()

    message = '反馈成功！'
    return jsonify({'message': message})


# 查看反馈信息
@app.route('/view_feedback', methods=['POST', 'PUT', 'GET'])
@login_required
def view_feedback():
    conn = sqlite3.connect('database/feedback.db')
    c = conn.cursor()
    c.execute('SELECT * FROM feedback ORDER BY timestamp DESC')
    feedbacks = c.fetchall()
    conn.close()
    return render_template('view_feedback.html', feedbacks=feedbacks)


# 查看反馈信息
@app.route('/view_feedback_1/<int:feedback_id>')
@login_required
def view_feedback_1(feedback_id):
    conn = sqlite3.connect('database/feedback.db')
    c = conn.cursor()
    c.execute('SELECT message FROM feedback WHERE id = ?', (feedback_id,))
    message = c.fetchone()[0]
    c.execute('update feedback set is_new = 0 where id = ?', (feedback_id,))
    conn.commit()
    conn.close()
    return jsonify({'content': message})


@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('database/userInfo.db')
    c = conn.cursor()
    c.execute('SELECT * FROM usertable WHERE id = ?', (user_id,))
    result = c.fetchone()
    c.close()
    conn.close()
    if result:
        # 创建 User 对象，并传入必要的参数
        user = User(result[0], result[1])
        user.email = result[3]
        user.phone = result[4]
        user.gender = result[5]
        user.register_time = result[6]
        user.hobby = result[7]
        user.is_admin = result[8]
        return user
    else:
        return None


def combine(keys, values):
    res = []

    if len(keys) != len(values):
        return None
    for ind, key in enumerate(keys):
        dict_temp = {}

        dict_temp[key] = values[ind]
        res.append(dict_temp)
    return res


def mycombine(key, value):
    data = {}
    # keys与values分别为该数据的键数组，值的数组。这里循环为字典添加对应键值
    for k, v in zip(key, value):
        data.update({k: v, }, )
    # 最后将数据打包成json格式以字典的方式传送到前端
    # return render(request, 'index.html', {'data': json.dumps(data)})
    return data


if __name__ == '__main__':
    app.run()
