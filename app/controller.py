from flask import Blueprint, request, jsonify
from app.service.case_service import get_cases_sorted_by_priority, get_case_by_id, add_case_into_db
from app.service.knowledge_service import get_article_by_id, get_articles_sorted_by_trending, get_articles_by_query, handle_vote
import uuid
from datetime import date

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
        article_list = get_articles_sorted_by_trending(limit, start)
    else:
        article_list = get_articles_by_query(query, limit, start)

    return jsonify(article_list), 200 if article_list else 404


# vote a knowledge article
# accept a POST request with JSON
#{
#   "direction": -1/0/1
#}
@api.route('/articles/<article_id>/vote', methods=['POST'])
def vote(article_id):
    req = request.get_json()
    if not {'clientId', 'direction'}.issubset(req):
        return '', 400

    client_id = req['clientId']
    direction = req['direction']

    if direction not in [-1, 0, 1]:
        return '', 400

    return '', 200 if handle_vote(article_id, client_id, direction) else 400



# get a case by id
# return JSON
# {
# 	"id": "string",
# 	"title": "string",
# 	"body": "string",
# 	"priority": 1-4,
# 	"date": "string"
# }
@api.route('/cases/<case_id>', methods=['GET'])
def get_case(case_id):
    case = get_case_by_id(case_id)
    # if not found, return 404
    return jsonify(case), 200 if case else 404


# get cases
# return JSON
# [{
# 	"id": "string",
# 	"title": "string",
# 	"body": "string",
# 	"priority": 1-4,
# 	"date": "string"
# }]
@api.route('/cases', methods=['GET'])
def get_cases():
    limit = request.args.get('limit')
    if limit is None:
        limit = 5

    start = request.args.get('start')
    if start is None:
        start = 0

    query = request.args.get('query')

    case_list = get_cases_sorted_by_priority(query, limit, start)

    return jsonify(case_list), 200 if case_list else 404


# add a case into the db
# accept JSON
# {
# 	"title": "string",
# 	"body": "string",
# 	"priority": 1-4
# }
@api.route('/cases', methods=['POST'])
def add_case():
    req = request.get_json()
    if not {'title', 'body', 'priority'}.issubset(req):
        return 'missing title, body or priority', 400

    short_description = req['title']
    content = req['body']
    priority = req['priority']
    sys_id = uuid.uuid4().hex
    opened = date.today()

    add_case_into_db(sys_id, short_description, content, priority, opened)
    return '', 200
