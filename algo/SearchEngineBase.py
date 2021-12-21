class SearchEngineBase(object):
    def __init__(self):
        print('进入父类初始化函数')
        pass

    # 加载文件内容，将文件id(这里简单用文件名代替)，和文件内容送给处理函数 process_files
    def read_files(self, file_path):
        with open(file_path, 'r',encoding = 'utf-8') as fin:
            text = fin.read()


        self.process_files(file_path, text)

    # 内容处理函数
    def process_files(self, id, text):
        raise Exception('process_files has not implemented.')

    # 检索函数，处理检索请求并返回结果
    def search_files(self,query):
        raise Exception('search_files has not implemented.')


