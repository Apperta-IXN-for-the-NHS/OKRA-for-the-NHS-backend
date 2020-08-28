"""
This is the module providing services for knowledge articles.
"""
import uuid
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from app import Article, RelatedArticles, db, KnowledgeScore, SearchHistory


def get_article_brief_info(article: Article, article_id_net_votes: dict) -> dict:
    """Get information about an article without article content.

    :param article: an Article object.
    :param article_id_net_votes: a dictionary, key is article id and value is net_votes.
    :return: a dict of the article info without content
    """
    return {'id': article.sys_id if article.sys_id else '',
            'title': article.short_description if article.short_description else '',
            'author': article.author if article.author else '',
            'created': article.published.strftime("%Y-%m-%d") if article.published else '',
            'view_count': article.sys_view_count if article.sys_view_count else 0,
            'net_votes': article_id_net_votes[article.sys_id] if article.sys_id in article_id_net_votes else 0}


def get_article_all_info(article: Article) -> dict:
    """Get information about an article with article content.

    :param article: an Article object
    :return: a dict of article info with content
    """
    def get_related_articles(article_id: str) -> list:
        """Get related articles.

        :param article_id: the id of an article
        :return: a list of article info without content
        """

        # find related articles and their similarity scores, id -> similarity score
        related_articles = RelatedArticles.query.filter_by(sys_id=article_id).order_by(RelatedArticles.score.desc())
        related_id_similarity = {related.number: related.score for related in related_articles}
        related_ids = related_id_similarity.keys()

        scores = KnowledgeScore.query.filter(KnowledgeScore.sys_id.in_(related_ids)).all()
        # find net score of these articles, id -> net score
        related_id_net_votes = {score.sys_id: score.net_votes for score in scores}
        # find trending score of these articles, id -> trending score
        related_id_trending = {score.sys_id: score.trending_score for score in scores}

        # use one query to find all the info about these articles, id -> info
        related_res = Article.query.filter(Article.sys_id.in_(related_ids)).all()
        related_id_info = {article.sys_id: get_article_brief_info(article, related_id_net_votes) for article in related_res}

        # calculate total score and sort in descending order
        related_id_total = {}
        for article_id in related_ids:
            similarity_score = 0.5 * related_id_similarity[article_id] if article_id in related_id_similarity else 0
            trending_score = 0.5 * related_id_trending[article_id] if article_id in related_id_trending else 0
            related_id_total[article_id] = similarity_score + trending_score
        sorted_ids = sorted(related_id_total.keys(), key=lambda x: x[1], reverse=True)

        # retrieve article info and output
        return [related_id_info[article_id] for article_id in sorted_ids]

    def get_net_votes(article_obj: Article) -> float:
        """Get net_votes of the article

        :param article_obj: an Article object
        :return: the net_votes of the Article object
        """
        score = KnowledgeScore.query.filter_by(sys_id=article_obj.sys_id).limit(1).first()
        return score.net_votes if score else 0

    return {'id': article.sys_id if article.sys_id else '',
            'title': article.short_description if article.short_description else '',
            'author': article.author if article.author else '',
            'created': article.published.strftime("%Y-%m-%d") if article.published else '',
            'body': article.text if article.text else '',
            'view_count': article.sys_view_count if article.sys_view_count else 0,
            'related': get_related_articles(article.sys_id),
            'net_votes': get_net_votes(article)}


def get_article_by_id(article_id: str) -> dict:
    """Get the info of the article with specified id.

    :param article_id: the id of an article
    :return: the article info with content
    """
    res = Article.query.filter_by(sys_id=article_id).limit(1).first()

    # if not exist, return empty dictionary
    if res is None:
        return {}

    # view count + 1
    # update view count after query, because
    res.sys_view_count += 1
    db.session.commit()
    return get_article_all_info(res)


def get_articles_sorted_by_trending(limit: int, start: int) -> list:
    """Get a list of articles which is sorted by trending score.

    :param limit: number of returned articles
    :param start: start index
    :return: a list of article info without content
    """

    # find the id of the top articles sorted by trending score
    res = KnowledgeScore.query.order_by(KnowledgeScore.trending_score.desc(), KnowledgeScore.published.desc(), KnowledgeScore.sys_id).offset(start).limit(limit)
    article_ids = [article.sys_id for article in res]
    # find their information according to the id
    article_objs = Article.query.filter(Article.sys_id.in_(article_ids)).all()
    # find their net scores
    scores = KnowledgeScore.query.filter(KnowledgeScore.sys_id.in_(article_ids)).all()
    # create a net score dictionary, id -> net score
    article_id_net_votes = {score.sys_id: score.net_votes for score in scores}
    # create a info dictionary, id -> info
    article_id_info = {article.sys_id: get_article_brief_info(article, article_id_net_votes) for article in article_objs}
    # return brief info
    return [article_id_info[article_id] for article_id in article_ids]


def get_articles_by_query(query: str, limit: int, start: int) -> list:
    """Get articles searched by query

    :param query: search query
    :param limit: number of returned articles
    :param start: start index
    :return: a list of article info without content
    """

    # save query
    history = SearchHistory(type="knowledge", content=query, search_date=datetime.now())
    db.session.add(history)
    db.session.commit()

    # search
    res = Article.query.filter(Article.short_description.ilike(f"%{query}%")).offset(start).limit(limit)
    article_ids = [article.sys_id for article in res]
    scores = KnowledgeScore.query.filter(KnowledgeScore.sys_id.in_(article_ids)).all()
    article_id_net_votes = {score.sys_id: score.net_votes for score in scores}

    # create a dictionary, id -> article info
    article_id_info = {article.sys_id: get_article_brief_info(article, article_id_net_votes) for article in res}
    # find the trending order
    scores = KnowledgeScore.query.filter(KnowledgeScore.sys_id.in_(article_ids)).order_by(KnowledgeScore.trending_score.desc(), KnowledgeScore.published.desc(), KnowledgeScore.sys_id).all()
    # return info according to the order
    return [article_id_info[article.sys_id] for article in scores]


def handle_vote(article_id: str, previous: int, current: int) -> bool:
    """Calculate net votes and update db.

    :param article_id: the id of an article
    :param previous: a user's previous vote
    :param current: the user's current vote
    :return: True for success, False for failure
    """

    # if the article does not exist, return false
    if Article.query.filter_by(sys_id=article_id).limit(1).first() is None:
        return False

    score = KnowledgeScore.query.filter_by(sys_id=article_id).limit(1).first()
    if score is None:
        return False

    score.net_votes += current - previous
    db.session.commit()
    return True


def add_new_article(info) -> bool:
    """Add a new article to the db.

    :param info: article info
    :return: True for success, False for failure
    """
    try:
        article = Article(sys_id=uuid.uuid4().hex,
                          number=info['number'] if 'number' in info else None,
                          short_description=info['short_description'],
                          author=info['author'],
                          kb_category=info['kb_category'] if 'kb_category' in info else None,
                          text=info['text'],
                          article_type=info['article_type'] if 'article_type' in info else None,
                          kb_knowledge_base=info['kb_knowledge_base'] if 'kb_knowledge_base' in info else None,
                          published=info['published'] if 'published' in info else None,
                          sys_tags=info['sys_tags'] if 'sys_tags' in info else None,
                          sys_view_count=info['sys_view_count'] if 'sys_view_count' in info else None
                          )
        db.session.add(article)
        db.session.commit()
        return True
    except IntegrityError:
        return False
