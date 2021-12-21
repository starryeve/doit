# 注册路由
from flask_restful import Api

from api.query import Query
api = Api()

# 搜索模块
api.add_resource(Query, "/query")

