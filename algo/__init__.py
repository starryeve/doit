from algo.SearchEngine import SearchEngine

def main(search_engine, str, participle, ifjaccard):
    fet=search_engine.process_files(participle)

    rresults=search_engine.word2sencentence(str,fet)
    print(len(rresults))

    if (len(rresults)==0):
        return {}

    final=search_engine.sort_final_result(str,rresults,ifjaccard)

    finallist=search_engine.init_title_with_url(final)
    # print(finallist)
        #算法想法 把所有句子rresults 先用query即所有关键词来比对，如果有 append list
        #没有就下一步 每个句子匹配多少个关键词 算TF值等来确定哪个关键词优先级高
        #优先级高的 词多的优先append list
        #优先级低的再append
        #最后剩下来的就再加上来

    return finallist

# 搜索接口调用该方法，传入三个参数，分别为关键词，搜索算法和排序算法
def search(keyword, participle, ifjaccard):
    search_engine = SearchEngine()
    print(1)
    print(participle)
    print(ifjaccard)
    print(1)
    return main(search_engine, keyword, participle, ifjaccard)
