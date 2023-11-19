## 相关模块导入
import pandas as pd
from py2neo import Graph, Node, Relationship

## 连接图形库，配置neo4j
graph = Graph("http://localhost:7474//browser/", auth=('neo4j', '123456'))
# 清空全部数据
graph.delete_all()
# 开启一个新的事务
graph.begin()

## csv源数据读取
storageData = pd.read_csv('./movie.csv', encoding='utf-8')
# 获取所有列标签
columnLst = storageData.columns.tolist()
# 获取数据数量
num = len(storageData['movie_cname'])

#print(num)

# KnowledgeGraph知识图谱构建(以电影为主体构建的知识图谱)
for i in range(num):
    # 为每部电影构建属性字典
    dict = {}
    for column in columnLst:
        dict[column] = str(storageData[column][i])


    #print(dict)
    node1 = Node('movie', name=storageData['movie_cname'][i], **dict)
    graph.merge(node1, 'movie', 'name')

    ## 上述代码已经成功构建所有电影的主节点，下面构建所有的分结点以及他们之间的联系
    # 去除所有的title结点
    dict.pop('movie_cname')
    ## 分界点以及关系
    for key, value in dict.items():
        ## 建立分结点
        node2 = Node(key, name=value)
        graph.merge(node2, key, 'name')
        ## 创建关系
        rel = Relationship(node1, key, node2)
        graph.merge(rel)
