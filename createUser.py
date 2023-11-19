import sqlite3  # 进行sqlite数据库操作


#
#
# def main():
#     # sql = '''
#     #         create table usertable
#     #         (
#     #         id integer primary key autoincrement,
#     #         username VARCHAR(50) NOT NULL UNIQUE,
#     #         password VARCHAR(255) NOT NULL,
#     #         email TEXT UNIQUE,
#     #         phone varchar(20) UNIQUE,
#     #         gender TEXT CHECK (gender IN ('男', '女')),
#     #         register_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
#     #         hobby text,
#     #         is_admin BOOLEAN
#     #         )
#     #     '''
#
#     # sql = '''
#     #         create table chatHistory
#     #         (
#     #         id integer primary key autoincrement,
#     #         userId integer,
#     #         question text,
#     #         answer text,
#     #         timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
#     #         )
#     #     '''
#     sql = '''
#     CREATE TABLE feedback (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     userId integer,
#     userName TEXT,
#     subject TEXT,
#     message TEXT,
#     timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
#     is_new BOOLEAN
# );
#     '''
#     #sql = 'select * from questionAnswer'
#     #conn = sqlite3.connect("userInfo.db")
#     #sql = 'update usertable set is_admin = 1 where id = 1'
#     #sql = 'ALTER TABLE usertable ADD is_admin BOOLEAN'
#     # sql = 'DROP TABLE IF EXISTS questionAnswer'
#     # conn = sqlite3.connect("userInfo.db")
#     sql = 'select * from feedback'
#     conn = sqlite3.connect("feedback.db")
#
#     # sql = 'select * from usertable'
#     cursor = conn.cursor()
#     cursor.execute(sql)
#     all = cursor.fetchall()
#     for i in all:
#         print(i)
#     conn.commit()
#     conn.close()
#
#
# if __name__ == "__main__":
#     # 调用函数
#     main()

def main():
    moviename = '肖申克的救赎'
    con = sqlite3.connect("pythonMovie.db")
    c = con.cursor()
    c.execute('SELECT * FROM pythonMovie WHERE movie_cname = ?', (moviename,))
    movieInfo = c.fetchone()
    message = '电影名称:' + movieInfo[2] + '\n上映年份:' + movieInfo[3] + '\n票房:' + str(
        movieInfo[4]) + '万' + '\n评分:' + str(movieInfo[5]) + '\n类型:' + movieInfo[7] + '\n地区:' + movieInfo[
                  8] + '\n评论人数:' + str(movieInfo[9]) + '\n评价人数:' + str(movieInfo[10]) + '\n演员:' + movieInfo[
                  11] + '\n导演:' + movieInfo[12] + '\n看过人数:' + str(movieInfo[13]) + '\n想看人数:' + str(
        movieInfo[14])


if __name__ == "__main__":
    # 调用函数
    main()
