from datetime import datetime

from app import Article, RelatedArticles, db, KnowledgeScore, SearchHistory


# return required info about articles
def get_article_brief_info(article, article_id_net_votes):
    return {'id': article.sys_id if article.sys_id else '',
            'title': article.short_description if article.short_description else '',
            'author': article.author if article.author else '',
            'created': article.published.strftime("%Y-%m-%d") if article.published else '',
            'view_count': article.sys_view_count if article.sys_view_count else 0,
            'net_votes': article_id_net_votes[article.sys_id] if article.sys_id in article_id_net_votes else 0}


def get_article_all_info(res):
    # return info about the related articles
    def get_related_articles(related_id):
        # find related articles and their similarity scores, id -> similarity score
        related_articles = RelatedArticles.query.filter_by(sys_id=related_id).order_by(RelatedArticles.score.desc())
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
        for related_id in related_ids:
            similarity_score = 0.5 * related_id_similarity[related_id] if related_id in related_id_similarity else 0
            trending_score = 0.5 * related_id_trending[related_id] if related_id in related_id_trending else 0
            related_id_total[related_id] = similarity_score + trending_score
        sorted_ids = sorted(related_id_total.keys(), key=lambda x: x[1], reverse=True)

        # retrieve article info and output
        return [related_id_info[article_id] for article_id in sorted_ids]

    def get_net_votes(article):
        score = KnowledgeScore.query.filter_by(sys_id=article.sys_id).first()
        return score.net_votes if score else 0

    return {'id': res.sys_id if res.sys_id else '',
            'title': res.short_description if res.short_description else '',
            'author': res.author if res.author else '',
            'created': res.published.strftime("%Y-%m-%d") if res.published else '',
            'body': res.text if res.text else '',
            'view_count': res.sys_view_count if res.sys_view_count else 0,
            'related': get_related_articles(res.sys_id),
            'net_votes': get_net_votes(res)}


# return article info with a specified id
def get_article_by_id(article_id):
    res = Article.query.filter_by(sys_id=article_id).first()

    # if not exist, return empty dictionary
    if res is None:
        return {}

    # view count + 1
    # update view count after query, because
    res.sys_view_count += 1
    db.session.commit()
    return get_article_all_info(res)


# return articles sorted by trending score
def get_articles_sorted_by_trending(limit, start):
    # find the id of the top 10 article sorted by trending score
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


# return articles searched by query
def get_articles_by_query(query, limit, start):
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


def handle_vote(article_id, previous, current):
    # if the article does not exist, return false
    if Article.query.filter_by(sys_id=article_id).first() is None:
        return False

    score = KnowledgeScore.query.filter_by(sys_id=article_id).first()
    if score is None:
        return False

    score.net_votes += current - previous
    db.session.commit()
    return True
