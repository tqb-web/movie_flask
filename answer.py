# 相关模块导入
import jieba.posseg as pseg
import jieba
from fuzzywuzzy import fuzz
from py2neo import Graph

## 建立neo4j对象，便于后续执行cyphere语句
graph = Graph("http://localhost:7474//browser/", auth=('neo4j', '123456'))

## 用户意图的判断
# 设计八类问题的匹配模板
movieSummary = ['这部电影主要讲的是什么？', '这部电影的主要内容是什么？', '这部电影主要说的什么问题？',
                '这部电影主要讲述的什么内容？', '这部电影的简介']
director = ['这部电影的导演是谁？', '这部电影是谁拍的？']
actors = ['这部电影是谁主演的？', '这部电影的主演都有谁？', '这部电影的主演是谁？', '这部电影的主角是谁？', '这部电影的演员都有谁？', '谁出演了这部电影']
movie_year = ['这部电影是什么时候播出的？', '这部电影是什么时候上映的？']
country = ['这部电影是那个国家的？', '这部电影是哪个地区的？']
category = ['这部电影的类型是什么？', '这是什么类型的电影', '这部电影是什么类型的']
movie_score = ['这部电影的评分是多少？', '这部电影的评分怎么样？', '这部电影的得分是多少分？']
evaluation = ['这部电影的评价人数是多少？', '这部有多少人评价过？', '有多少人评价过这部']
comment = ['这部电影的评论人数是多少？', '这部有多少人评论过？', '有多少人评论过这部']
movie_vote = ['这部电影的票房是多少？', '这部获得了票房？']
movieWatched = ['看过这部电影的人数是多少？', '这部电影有多少人看过？', '有多少人看过这部电影？']
movieWanttw = ['想看这部电影的人数是多少？', '这部电影有多少人想看？', '有多少人想看这部电影？']

# 设计八类问题的回答模板
movieSummaryResponse = '{}这部电影主要讲述{}'
directorResponse = '{}这部电影的导演为{}'
actorsResponse = '{}这部电影的主演为{}'
movie_yearResponse = '{}这部电影的上映时间为{}'
countryResponse = '{}这部电影是{}的'
categoryResponse = '{}这部电影的类型是{}'
movie_scoreResponse = '{}这部电影的评分为{}'
evaluationResponse = '{}这部电影评价的人数为{}人'
commentResponse = '{}这部电影评论的人数为{}人'
movie_voteResponse = '{}这部电影评论的票房是{}万'
movieWatchedResponse = '看过{}这部电影的人数为{}人'
movieWanttwResponse = '想看{}这部电影的人数为{}人'
# 用户意图模板字典
stencil = {'movieSummary': movieSummary, 'director': director, 'actors': actors, 'movie_year': movie_year,
           'country': country, 'category': category,
           'movie_score': movie_score, 'evaluation': evaluation, 'comment': comment, 'movie_vote': movie_vote,
           'movieWatched': movieWatched, 'movieWanttw': movieWanttw}
# 图谱回答模板字典
responseDict = {'movieSummaryResponse': movieSummaryResponse, 'directorResponse': directorResponse,
                'actorsResponse': actorsResponse,
                'movie_yearResponse': movie_yearResponse, 'countryResponse': countryResponse,
                'categoryResponse': categoryResponse,
                'movie_scoreResponse': movie_scoreResponse, 'evaluationResponse': evaluationResponse,
                'commentResponse': commentResponse, 'movie_voteResponse': movie_voteResponse,
                'movieWatchedResponse': movieWatchedResponse, 'movieWanttwResponse': movieWanttwResponse}


# 由模板匹配程度猜测用户意图
## 模糊匹配参考文献：https://blog.csdn.net/Lynqwest/article/details/109806055
def AssignIntension(text):
    '''
    :param text: 用户输入的待匹配文本
    :return: dict:各种意图的匹配值
    '''
    stencilDegree = {}
    for key, value in stencil.items():
        score = 0
        for item in value:
            degree = fuzz.partial_ratio(text, item)
            score += degree
        stencilDegree[key] = score / len(value)

    return stencilDegree


## 问句实体的提取
## 结巴分词参考文献：https://blog.csdn.net/smilejiasmile/article/details/80958010
def getMovieName(text):
    '''
    :param text:用户输入内容
    :return: 输入内容中的电影名称
    '''
    movieName = ''
    jieba.load_userdict('./selfDefiningTxt.txt')
    words = pseg.cut(text)
    for w in words:
        ## 提取对话中的电影名称
        if w.flag == 'tqb':
            movieName = w.word
    return movieName


## cyphere语句生成，知识图谱查询，返回问句结果
## py2neo执行cyphere参考文献：https://blog.csdn.net/qq_38486203/article/details/79826028
def SearchGraph(movieName, stencilDcit={}):
    '''
    :param movieName:待查询的电影名称
    :param stencilDcit: 用户意图匹配程度字典
    :return: 用户意图分类，知识图谱查询结果
    '''
    result = ""
    classification = [k for k, v in stencilDcit.items() if v == max(stencilDcit.values())][0]
    ## python中执行cyphere语句实现查询操作
    cyphere = 'match (n:movie) where n.movie_cname = "' + str(movieName) + '" return n.' + str(classification)
    object = graph.run(cyphere)
    for item in object:
        result = item
    # print(result)
    return classification, result


## 根据问题模板回答问题
def respondQuery(movieName, classification, item):
    '''
    :param movieName: 电影名称
    :param classification: 用户意图类别
    :param item:知识图谱查询结果
    :return:none
    '''
    query = classification + 'Response'
    response = [v for k, v in responseDict.items() if k == query][0]
    item = str(item)[1:-1]
    middle_content = response.format(movieName, item)
    return middle_content
    # print(middle_content)


def main_ai(code):
    # queryText = '三十二这部电影的评分是多少？'
    queryText = code
    movieName = getMovieName(queryText)
    dict = AssignIntension(queryText)
    classification, result = SearchGraph(movieName, dict)
    if len(result) == 0:
        a = "抱歉，无法回答该问题"
        return a
    else:
        return respondQuery(movieName, classification, result)


if __name__ == '__main__':
    main_ai()
