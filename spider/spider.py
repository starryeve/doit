import requests
import parsel # 数据解析模块 第三方模块 pip install parsel
import os # 文件操作模块
import re # 正则表达式模块
def change_title(name):
    mode = re.compile(r'[\\\/\:\*\?\"\<\>\|]')
    new_name = re.sub(mode, '_', name)
    return new_name

filename = 'pdf\\' # 文件名字
filename_1 = 'html\\'
if not os.path.exists(filename): #如果没有这个文件夹的话
    os.mkdir(filename) # 自动创建一下这个文件夹

if not os.path.exists(filename_1): #如果没有这个文件夹的话
    os.mkdir(filename_1) # 自动创建一下这个文件夹


for page in range(1, 51):
    print(f'=================正在爬取第{page}页数据内容=================')
    #url = f'https://blog.csdn.net/qdPython/article/list/{page}'
    #url = f'https://blog.csdn.net/m0_54355125/article/list/{page}'
    #url = f'https://blog.csdn.net/qq_33709582/article/list/{page}'
    #url = f'https://pythonjx.blog.csdn.net/article/list/{page}'
    #url = f'https://blog.csdn.net/csdnopensource/article/list/{page}'
    #url = f'https://blog.csdn.net/super111t/article/list/{page}'
    #url = f'https://blog.csdn.net/csdngeeknews/article/list/{page}'
    #url = f'https://feige.blog.csdn.net/article/list/{page}'
    #url = f'https://blog.csdn.net/m0_64353693/article/list/{page}'
    #url = f'https://blog.csdn.net/ZuoYueLiang/article/list/{page}'
    #url = f'https://blog.csdn.net/qq_41809113/article/list/{page}'
    #url = f'https://blog.csdn.net/jakpopc/article/list/{page}'
    #url = f'https://blog.csdn.net/pp13164892/article/list/{page}'
    url = f'https://blog.csdn.net/siren0203/article/list/{page}'
    #url = f'https://blog.csdn.net/m0_55452176/article/list/{page}'
    #url = f'https://blog.csdn.net/Byeweiyang/article/list/{page}'
    #url = f'https://blog.csdn.net/weixin_52040868/article/list/{page}'
    #url = f'https://blog.csdn.net/JACK_SUJAVA/article/list/{page}'
    #url = f'https://haiyong.blog.csdn.net/article/list/{page}'
    #url = f'https://yuhaidong.blog.csdn.net/article/list/{page}'

    # python代码对于服务器发送请求 >>> 服务器接收之后(如果没有伪装)被识别出来, 是爬虫程序, >>> 不会给你返回数据
    # 客户端(浏览器) 对于 服务器发送请求 >>> 服务器接收到请求之后 >>> 浏览器返回一个response响应数据
    # headers 请求头 就是把python代码伪装成浏览器进行请求
    # headers参数字段 是可以在开发者工具里面进行查询 复制
    # 并不是所有的参数字段都是需要的
    # user-agent: 浏览器的基本信息 (相当于披着羊皮的狼, 这样可以混进羊群里面)
    # cookie: 用户信息 检测是否登录账号 (某些网站 是需要登录之后才能看到数据, B站一些数据内容)
    # referer: 防盗链 请求你的网址 是从哪里跳转过来的 (B站视频内容 / 妹子图图片下载 / 唯品会商品数据)
    # 根据不同的网站内容 具体情况 具体分析
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
    }
    # 请求方式: get请求 post请求 通过开发者工具可以查看url请求方式是什么样的
    # 搜索 / 登录 /查询 这样是post请求
    response = requests.get(url=url, headers=headers)
# 需要把获取到的html字符串数据转成 selector 解析对象
    selector = parsel.Selector(response.text)
    # getall 返回的是列表
    href = selector.css('.article-list a::attr(href)').getall()
    html_str = """
    <!DOCTYPE HTML>
    <html lang="en">
    <head>
        <title>{title}</title><meta charset="utf-8">
    </head>
    <body>
    {article}
    </body >
    </html >"""
    for index in href:
        # 发送请求 对于文章详情页url地址发送请求
        response_1 = requests.get(url=index, headers=headers)
        selector_1 = parsel.Selector(response_1.text)
        title = selector_1.css('#articleContentId::text').get()
        keywords = selector_1.css('meta[name="description"]').get()
        keywords = re.sub("^.*content=[\"\']", "", keywords)
        keywords = re.sub("[\"\']>", "", keywords)
        new_title = change_title(title)
        content_views = selector_1.css('#content_views').get()
        html_content = html_str.format(title=title,article=content_views)
        html_path = filename_1 + new_title + '.html'
        pdf_path = filename + new_title + '.pdf'
        with open(filename_1 + new_title+".txt", mode='w', encoding='utf-8') as f:
            f.write(keywords)
            print('正在保存: ', title)
        with open(filename_1+"url.txt", mode='a', encoding='utf-8') as f:
            f.write(f'INSERT INTO `url`(`url`, `title`) VALUES ("{index}","{new_title}");\n')

