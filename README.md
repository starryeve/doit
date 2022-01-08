# DOIT —— 计算机学习搜索引擎

## 项目简介

本项目是由三名同学分工完成的NLP期末大作业——一个简单的文章搜索引擎，使用了本学期课上所学习的基本算法理论。
通过收集CSDN网站上的技术文档、博客的数据，调用python提供的jieba、pkuseg分词包，
进行文章分词，构建倒排索引数据库。使用了tf-idf和jaccard算法，对搜索结果进行了一定的排序优化。

## 技术栈

- 算法：jieba，pkuseg，tf-idf，jaccard
- 爬虫：requests
- 前端：html，css，javascript
- 后端：flask，flask-restful，mysql

## 项目目录

``` markdown
.
├── README.md
├── algo // 核心搜索算法
│   ├── SearchEngine.py
│   ├── SearchEngineBase.py
│   ├── __init__.py
├── api
│   ├── __init__.py
│   ├── query  // 搜索接口
│   │   ├── __init__.py
│   └── routers.py // 路由注册
├── app.py // 项目启动文件
├── inverted_index // 倒排索引构建代码
│   └── doit.py
├── requirements.txt // 所用到的python依赖
├── sql // 数据库文件
│   ├── npl_article.sql
│   ├── npl_article1.sql
│   ├── npl_url.sql
├── spider // 爬虫相关
│   └── spider.py
└── templates  // 前端界面
    └── index.html // 搜索主页
5 directories, 10 files
```

## 运行步骤

1. 打开pycharm，配置好pyth3.8虚拟环境
2. 命令行运行` pip3 install -r ./requirements.txt`安装项目所需的依赖包
3. 导入三个sql数据库文件
4. 修改SearchEngine.py下的数据库配置项为本地数据库
5. 运行app.py，启动项目
   ![image-20211218184827950](https://gitee.com/zeng-fanhao/figure-bed/raw/master/images/202112181848993.png)
6. 使用chrome或其他浏览器打开http://localhost:5000
   ![image-20211218184504207](https://gitee.com/zeng-fanhao/figure-bed/raw/master/images/202112181845263.png)



