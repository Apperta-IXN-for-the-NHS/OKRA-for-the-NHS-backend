from flask import Blueprint, request, jsonify
from app.knowledge_service import get_article_by_id, get_articles_sorted_by_date

api = Blueprint('api', __name__)


@api.route('/articles/<id>', methods=['GET'])
def get_article(id):
    d = get_article_by_id(id)
    # if not found, return 404
    return jsonify(d), 200 if d else 404


@api.route('/articles', methods=['GET'])
def get_recent_articles():
    limit = request.args.get('limit')
    if limit is None:
         limit = 5
    start = request.args.get('start')
    if start is None:
        start = 0
    article_list = get_articles_sorted_by_date(limit, start)

    return jsonify(article_list), 200 if article_list else 404
