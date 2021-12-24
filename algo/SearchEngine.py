import re
import jieba
from algo.SearchEngineBase import SearchEngineBase
import math
import pymysql
import jieba.analyse
# 定义数据库变量
host="39.108.154.184"
user="root"
password="naive_search_db"
database="npl"
port=3310
class SearchEngine(SearchEngineBase):
    def __init__(self):#初始化
        super(SearchEngine, self).__init__()
        self.inverted_index = {}


    def process_files(self, participle):#相当于对数据库的所有
        # 为每一个单词建立倒序索引（词 -> 文档id）
        try:
            db = pymysql.connect(host=host, user=user,port=port, password=password, database=database, charset="utf8")

            print("数据库连接成功")
        except pymysql.Error as e:
            print("数据库连接失败：" + str(e))

        cursor = db.cursor()
        if(participle=="0"):
            sql = f"select keyword,title,score,url_id from article;"
        else:
            sql = f"select keyword,title,score,url_id from article1;"
        try:
            cursor.execute(sql)
            fet = cursor.fetchall()

        except pymysql.Error as e:
            db.rollback()
            print('寄了' + str(e))

        for i in range(len(fet)):
            word=fet[i][0]
            #print(word)
            if word not in self.inverted_index:#去重
                self.inverted_index[word] = []
            self.inverted_index[word].append(fet[i][1])#id是filepath
        return fet

    @staticmethod
    def parse_text_to_words(text):#搜索的关键词
        # 使用正则表达式去除标点符号和换行符
        text = re.sub(r'[^\w ]', ' ', text)
        text = text.lower()

        seg_list = jieba.cut_for_search(text)#分词
        #print(", ".join(seg_list))


        # 过滤空值
        seg_list = filter(None, seg_list)

        # 返回单词的 set
        return set(seg_list)

    def word2sencentence(self,query,fet):

        delete_word=[]


        query_words=self.parse_text_to_words(query)#搜索分词函数
        for query_word in query_words:#没有在倒排索引表的关键词直接跳过 逐个查询的关键词遍历
            if(query_word not in self.inverted_index):
                delete_word.append(query_word)

        if(len(query_words)==len(delete_word)):
            return []
        sr=self.txt_ranking(delete_word,query,fet)
        return sr

    def txt_ranking(self,delete_word,query,fet):#文本排行（估计只要前20个）
        # print(fet)
        print(delete_word)
        return_result={}
        results=[]
        words = self.parse_text_to_words(query)
        words = list(words)
        document=[]
        for i in range(len(delete_word)):
            if (delete_word[i] in words):
                words.remove(delete_word[i])
        #接下来要把可能的文本全部抓出来
        for word in words:
            results += self.inverted_index[word]
        results=list(set(results))#去重

        for res in results:#发现了所有可能的结果都在results里面 利用循环 给每一个结果集里的文本定分数
            res=re.sub(u"\.txt", u"", res)
            for word in words:#关键词

                for i in range(len(fet)):
                    fet_result = []#[score,url_id]


                    if fet[i][1]==res and fet[i][0]==word:

                        fet_result.append(fet[i][2])#score
                        fet_result.append(fet[i][3])#url_id
                        if res not in return_result:  # 无中生有
                            return_result[res] = fet_result
                        else:

                            return_result[res][0] += fet_result[0]  # id是filepath
        # print(return_result)
        return return_result

    def jacccard(self, query,finals):
        words = self.parse_text_to_words(query)
        words = list(words)

        temp=1
        for final in finals:
            # print(final)
            # print(final[0])
            # print(final[1])
            # print(type(final[1]))
            # print(final[1][0])
            # print(type(final[1][0]))
            ans=len(list(jieba.cut(final[0])))
            ans1=len(words)
            for word in words:
                if word in final[0]:
                    temp += 1
            score=temp/(ans+ans1)
            #
            # print(score)
            # print(type(score))
            final[1][0]=score




    def sentences_ranking(self,delete_word,query,sentences,results):

        words=self.parse_text_to_words(query)
        words=list(words)
        for i,w in delete_word:
            if(words[i]==w):
                words.remove(words[i])


        thewords = [[0 for i in range(len(results))] for j in range(len(words))]  #

        for i in range(len(words)):#词的for

            for j in range(len(results)):
                key=self.file_to_words(results[j])#文档的内容

                thewords[i][j]=(key.count(words[i])) #在做成字符串的文档中
        print(thewords)
        wordsscore=[]
        for i in range(len(words)):
            temp=0
            if(len(thewords[i])):
                for j in range(len(thewords[i])):
                    if(thewords[i][j]!=0):
                        temp+=1

                score=math.log(1+thewords[i][j],10)*math.log(len(thewords[i])/temp+1,10)

                wordsscore.append(score)
        print(wordsscore)

        sentencesscores=[]
        for i in range(len(sentences)):
            sentencesscores.append(0)
        for i in range(len(sentences)):

            for j in range(len(words)):

                if(words[j] in sentences[i]):
                    sentencesscores[i]+=wordsscore[j]
        print(sentencesscores)
        sentenceswithscores=[]
        for i in range(len(sentencesscores)):
            sentenceswithscores.append((sentences[i],sentencesscores[i]))

        def takeSecond(elem):
            return elem[1]
        sentenceswithscores.sort(key=takeSecond,reverse=True)

        return sentenceswithscores

    def sort_final_result(self,query,result,ifjaccard):
        final = sorted(result.items(), key=lambda x: x[1][0], reverse=True)
        print(final)
        if ifjaccard=="1":
            self.jacccard(query,final)
            final = sorted(result.items(), key=lambda x: x[1][0], reverse=True)
            print(final)
        final=final[0:20]
        return final

    def init_title_with_url(self, final):
        finallist = []
        try:
            db = pymysql.connect(host=host, user=user, port=port,password=password, database=database, charset="utf8")
            print("数据库连接成功")
        except pymysql.Error as e:
            print("数据库连接失败：" + str(e))
        cursor = db.cursor()

        for f in final:

            sql = f"select url from url where url_id='{f[1][1]}';"

            try:
                cursor.execute(sql)
                fet = cursor.fetchall()
                # print(fet)
            except pymysql.Error as e:
                db.rollback()
                print('寄了' + str(e))

            f1 = (f[0],) + fet
            finallist.append((f1))
        return finallist

    def file_to_words(self,res):#把具体一篇文档分词
        with open("./html/"+res, 'r',encoding = 'utf-8') as fin:
            text = fin.read()
        text = re.sub(r"\s+","", text)  # 去掉换行符
        fresult= jieba.cut_for_search(text)#分词


        # 过滤空值
        fresult = filter(None, fresult)
        fresult ="_ ".join(fresult)

        return fresult

    def get_sentences(self,index,key):
        left=0
        right=10000

        for i in range(index,-1,-1):
            if(key[i]=='，'or key[i]=='；'  or key[i]=='。'):
                left=i
                break
        for i in range(index+1,len(key)):
            if(key[i]=='，'or key[i]=='；'  or key[i]=='。'):
                right=i+1
                break
        if(left>=15):
            if(index-left<=15):
                left=index-15
        else:left=0

        if(index-left>=25):
            left = index - 20
        if(right!=10000 and right-index>=25):
            right=25



        return key[left:right]













