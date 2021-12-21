from flask_restful import Resource,request
from algo import search

class Query(Resource):
    def get(self):
        keyword = request.args.get('keyword')
        participle = request.args.get('participle')
        sort = request.args.get('sort')

        result = search(keyword, participle, sort)

        return result
