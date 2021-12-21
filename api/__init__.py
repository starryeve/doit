from flask import Flask
from api.routers import api


def create_app():
    app = Flask(__name__, template_folder="../templates")

    # 返回数据中response为中文
    app.config['JSON_AS_ASCII'] = False
    app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))


    # 初始化路由
    api.init_app(app)

    return app
