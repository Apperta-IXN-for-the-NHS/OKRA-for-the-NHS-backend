"""
This is the controller of the back-end application.

It provides REST APIs, handles requests and returns responses.
"""
from flask import Blueprint, request, jsonify
from app.service.case_service import get_cases_sorted_by_date_and_priority, get_case_by_id, add_new_case
from app.service.knowledge_service import get_article_by_id, get_articles_sorted_by_trending, get_articles_by_query, \
    handle_vote, add_new_article
from app.service.trending_service import update_trending, update_related

api = Blueprint('api', __name__)


@api.route('/articles/<article_id>', methods=['GET'])
def get_article(article_id: str) -> (str, int):
    """Return the info of the article with the article id.

    Returned JSON has the following keys:
    - id: string, article id
    - title: string, article title
    - author: string, article author
    - created: string, the created date of article
    - body: string, article content
    - view_count: integer, view count of article
    - net_votes: float, vote score of article
    - related: a list of JSON with keys: id, title, author, created, view_count, net_votes

    :param article_id: the id of an article
    :return: JSON format of article info and status code
    """

    # {
    #     "id": "string",
    #     "title": "string",
    #     "author": "string",
    #     "created": "string",
    #     "body": "string",
    #     "view_count": 0,
    #     "net_votes": 0,
    #     "related": [
    #         {
    #             "id": "string",
    #             "title": "string",
    #             "author": "string",
    #             "created": "string",
    #             "view_count": 0,
    #             "net_votes": 0
    #         }
    #     ]
    # }

    article = get_article_by_id(article_id)
    # if not found, return 404
    return jsonify(article), 200 if article else 404


@api.route('/articles', methods=['GET'])
def get_articles() -> (str, int):
    """Get a list of articles according to the given parameters.

    Returned JSON has the following keys:
    - id: string, article id
    - title: string, article title
    - author: string, article author
    - created: string, the created date of article
    - view_count: integer, view count of article
    - net_votes: float, vote score of article

    :return: JSON format of an article info list and status code
    """

    # [
    #     {
    #         "id": "string",
    #         "title": "string",
    #         "author": "string",
    #         "created": "string: 2020-08-01",
    #         "view_count": 0,
    #         "net_votes": 0
    #     }
    # ]

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


@api.route('/articles', methods=['POST'])
def add_article() -> (str, int):
    """Add a new article.

    Accept JSON format requests with the following keys:
    - short_description: string, article title
    - author: string, article author
    - text: string, article content

    There could be other optional keys: number, kb_category, article_type,
    kb_knowledge_base, published, sys_tags, sys_view_count

    :return: messages and status code
    """
    req = request.get_json()
    if not {'short_description', 'author', 'text'}.issubset(req):
        return 'require short_description, author and text', 400

    if add_new_article(req):
        return '', 200
    else:
        return 'cannot add into db', 400


@api.route('/articles/<article_id>/vote', methods=['POST'])
def vote(article_id: str) -> (str, int):
    """Vote a knowledge article.

    Accept a POST JSON request with the following keys:
    - previous: -1/0/1, users' previous vote
    - current: -1/0/1, users' current vote

    :param article_id: the id of an article
    :return: error messages and status code
    """

    # {
    #     "previous": -1/0/1,
    #     "current": -1/0/1
    # }

    req = request.get_json()
    if not {'previous', 'current'}.issubset(req):
        return 'missing previous or current', 400

    previous = req['previous']
    current = req['current']

    if previous not in [-1, 0, 1] or current not in [-1, 0, 1]:
        return 'wrong value for previous or current', 400

    if handle_vote(article_id, previous, current):
        return '', 200
    else:
        return 'cannot find the knowledge article', 400


@api.route('/cases/<case_id>', methods=['GET'])
def get_case(case_id: str) -> (str, int):
    """Get a case with the specified id.

    Returned JSON has the following keys:
    - id: string, case id
    - title: string, case title
    - body: string, case body
    - priority: integer, the priority of case
    - date: string, submitted date of case

    :param case_id: the id of a case
    :return: JSON format case info and status code
    """

    # {
    #     "id": "string",
    #     "title": "string",
    #     "body": "string",
    #     "priority": 1 - 4,
    #     "date": "string"
    # }

    case = get_case_by_id(case_id)
    # if not found, return 404
    return jsonify(case), 200 if case else 404


@api.route('/cases', methods=['GET'])
def get_cases() -> (str, int):
    """Get a list of cases.

    Returned JSON has the following keys:
    - id: string, case id
    - title: string, case title
    - body: string, case body
    - priority: integer, the priority of case
    - date: string, submitted date of case

    :return: a list of JSON format case info and status code
    """

    # [
    #     {
    #         "id": "string",
    #         "title": "string",
    #         "body": "string",
    #         "priority": 1 - 4,
    #         "date": "string"
    #     }
    # ]

    limit = request.args.get('limit')
    if limit is None:
        limit = 5

    start = request.args.get('start')
    if start is None:
        start = 0

    query = request.args.get('query')

    case_list = get_cases_sorted_by_date_and_priority(query, limit, start)

    return jsonify(case_list), 200 if case_list else 404


@api.route('/cases', methods=['POST'])
def add_case() -> (str, int):
    """Add a case into db.

    Accept JSON request with the following keys:
    - title: string, case title
    - body: string, case body
    - priority: integer, the priority of case

    :return: empty string and status code
    """

    # {
    #     "title": "string",
    #     "body": "string",
    #     "priority": 1-4
    # }
    req = request.get_json()
    if not {'title', 'body', 'priority'}.issubset(req):
        return 'missing title, body or priority', 400

    short_description = req['title']
    content = req['body']
    priority = req['priority']

    if add_new_case(short_description, content, priority):
        return '', 200
    else:
        return 'cannot add to db', 400


# @api.route('/update/trending', methods=['GET'])
# def update_trending_score() -> (str, int):
#     """this is used for testing purpose, to be able to test without trigger the scheduler"""
#     d = update_trending()
#     # if not found, return 404
#     if d:
#         return "success", 200
#     else:
#         return "fail", 404


# @api.route('/update/related', methods=['GET'])
# def update_related_score() -> (str, int):
#     """this is used for testing purpose, to be able to test without trigger the scheduler"""
#     d = update_related()
#     # if not found, return 404
#     if d:
#         return "success", 200
#     else:
#         return "fail", 404
