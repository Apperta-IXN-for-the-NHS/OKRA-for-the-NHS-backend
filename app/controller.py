from flask import Blueprint, request, jsonify
from app.knowledge_service import get_article_by_id, get_articles_sorted_by_date, get_articles_by_query

api = Blueprint('api', __name__)


# get an article with a specified id
# the structure of JSON return
# {
# 	"id": "string",
# 	"title": "string",
# 	"author": "string",
# 	"created": "string",
# 	"body": "string",
# 	"related": [
# 		{
# 			"id": "string",
# 			"title": "string",
# 			"author": "string",
# 			"created": "string"
#           "view_count": 0
# 		}
# 	]
# }
@api.route('/articles/<article_id>', methods=['GET'])
def get_article(article_id):
    article = get_article_by_id(article_id)
    # if not found, return 404
    return jsonify(article), 200 if article else 404


# get articles
# the structure of JSON return:
# [
#   {
#     "id": "string",
#     "title": "string",
#     "author": "string",
#     "created": "string: 2020-08-01"
#   }
# ]
@api.route('/articles', methods=['GET'])
def get_articles():
    limit = request.args.get('limit')
    if limit is None:
        limit = 5

    start = request.args.get('start')
    if start is None:
        start = 0

    query = request.args.get('query')
    if query is None:
        article_list = get_articles_sorted_by_date(limit, start)
    else:
        article_list = get_articles_by_query(query, limit, start)

    return jsonify(article_list), 200 if article_list else 404
