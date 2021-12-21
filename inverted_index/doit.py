import os
import re
import jieba
import math
from jieba import analyse
import pymysql
import pkuseg
pku_seg = pkuseg.pkuseg()

import jieba.analyse
host="localhost"
user="root"
password=""
database="npl"
try:
    db = pymysql.connect(host=host, user=user, password=password, database=database,charset="utf8")

    print("数据库连接成功")
except pymysql.Error as e:
    print("数据库连接失败："+str(e))
# 引入TF-IDF关键词抽取接口
tfidf = analyse.extract_tags

rootdir="./html/"
textdir="./txt/"
inverted_index = {}
totalnum=0
def read_files( file_path):
    with open(file_path, 'r', encoding='utf-8') as fin:
        text = fin.read()



    process_files(file_path, text)
def main():
    temp=0
    rootdir = "./html/"
    for root, dirs, files in os.walk(rootdir):
        for file_path in files:
            read_files(rootdir+file_path)
            temp+=1
    return temp

def process_files( id, text):#相当于对数据库的所有
    # 为每一个单词建立倒序索引（词 -> 文档id）
    text = re.sub(r'[^\w ]', ' ', text)
    text = text.lower()
    text=re.sub("的",u"",text)
    text=re.sub(u"[一了和]",u"",text)
    id = re.sub(u"./html/", u"", id)
    #words=jieba.analyse.extract_tags(text, topK=15, withWeight=False, allowPOS=())

    words = pku_seg.cut(text)
    if len(words)>=10:
        words=words[0:10]



    for word in words:
        word=word.lower()
        #print(word)
        if word not in inverted_index:#去重
            inverted_index[word] = []
        inverted_index[word].append(id)#id是filepath

def parse_text_to_words(text):#搜索的关键词
    # 使用正则表达式去除标点符号和换行符
    text = re.sub(r'[^\w ]', ' ', text)
    text=text.lower()

    seg_list = jieba.cut(text)#分词
    #print(", ".join(seg_list))


    # 过滤空值
    seg_list = filter(None, seg_list)


    # 返回单词的 set
    return set(seg_list)
totalnum=main()
print(totalnum)
temp = 0
id=[]
keyword=[]
scores=[]
titles=[]
url=[]
list=[]
err=[]
cursor = db.cursor()
sql = f'select url_id,title from url;'
ids=[]
tit=[]
try:
    # 执行sql语句
    cursor.execute(sql)
    fet = cursor.fetchall()

    # 提交到数据库执行
    db.commit()
except pymysql.Error as e:
    # 如果发生错误则回滚
    db.rollback()
    print('寄了' + str(e))

for i in range(len(fet)):
    ids.append(fet[i][0])
    tit.append(fet[i][1])
dic=dict(zip(tit,ids))

print(len(dic))
for w in inverted_index.keys():  # 建立分数索引表 非常重要 拿key也就是索引值
    if(w==" "):
        continue


    for i in range(len(inverted_index[w])):  # 每个关键词出现过的每个文本 结果是文本
        # w是字典的key 我们要的是字典的value数组
        # print(self.inverted_index[w][i])

        with open("./html/" + inverted_index[w][i], 'r', encoding='utf-8') as fin:  # 打开比一比出现多少次
            text = fin.read()
        text=text.lower()


        if (text.count(w) != 0):
            score= text.count(w)/len(parse_text_to_words(text)) * math.log( totalnum/ (len(inverted_index[w]) + 1), 10)




            title = re.sub(u"\.txt", u"", inverted_index[w][i])




            change=0
            if(title not in dic.keys()):


                err.append(title)
                continue
            else:
                temp += 1
                fet_result=dic[title]


                id.append(temp)
                scores.append(score)
                keyword.append(w)
                titles.append(title)
                url.append(fet_result)

        else:
            continue








#for i in range(len(id)):
    #print(id[i],scores[i],keyword[i],titles[i],url[i])
sql ='INSERT INTO article1 (id,keyword,score,title,url_id) VALUES (%s,%s,%s,%s,%s)'
print(sql)

for i in range(len(id)):

    try:
    # 执行sql语句
        cursor.execute(sql,(id[i],keyword[i],scores[i],titles[i],url[i]))
        print('↓↓↓')

   # 提交到数据库执行
        db.commit()
    except pymysql.Error as e:
         # 如果发生错误则回滚
        db.rollback()
        print('寄了'+str(e))

