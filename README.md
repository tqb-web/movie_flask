# Python爬取豆瓣电影 使用flask框架可视化数据

## 项目技术栈：`Flask框架、Echarts、WordCloud、SQLite`

## 环境设置 确保安装 Python 3.x，并且已安装以下依赖（见 `requirements.txt` 文件）。

## 目录结构说明

│ app.py ----- flask框架文件  

│ ... .py ----- 其他功能文件 

│ database ----数据  
&emsp;&emsp; ----cloud.db  
&emsp;&emsp; ----feedback.db  
&emsp;&emsp; ----pythonMovie.db  
&emsp;&emsp; ----userInfo.db  
&emsp;&emsp; ----sentiment.db

│ README.md

│ requirements.txt ----- 依赖包环境版本

├─static ----- 静态页面

├─templates ----- HTML页面

└─venv ----- 虚拟环境

## 运行方式

运行以下命令启动 Flask 服务器：

```bash
python3 app.py
```

**项目托管于以下地址，点击访问：<a href="http://47.236.122.152:5000">47.236.122.152:5000</a>**

**由于github限制，电影数据无法完整上传，部分功能可能无法正常使用，想要完整数据的请联系。**

目前仅上传了可视化代码，爬虫代码有时间再整理上传，后续将持续更新...

有任何问题请联系**QQ1797834904**

## 页面展示

![index](./static/assets/img/page/index.png)
![movie](./static/assets/img/page/movie.png)
![chart](./static/assets/img/page/chart.png)
![wordcloud](./static/assets/img/page/wordcloud.png)
![askQuestion](./static/assets/img/page/askQuestion.png)
![compare](./static/assets/img/page/compare.png)
![info](./static\assets\img\page\info.png)
![sentiment](./static/assets/img/page/sentiment.png)
