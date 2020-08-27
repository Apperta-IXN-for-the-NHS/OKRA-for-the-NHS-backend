
from app import Article
from app import recommendation
from app import db
from app import KnowledgeScore
from app import RelatedArticles


# this function computes the trending score for each of the articles
def get_trending_score_list():
    # get article list with view sorted by published date
    article_view = Article.query.filter(Article.published.isnot(None)).order_by(Article.published.desc()).with_entities(Article.sys_id, Article.sys_view_count)
    articleSortedByViewList = []
    articleSortedByNetVotes=[]
    for article in article_view:
        dict={}
        dict['sys_id']=article.sys_id
        dict['view_count'] = article.sys_view_count
        articleSortedByViewList.append(dict)

    # get article list with net_votes sorted by published date
    article_favorite = KnowledgeScore.query.filter(KnowledgeScore.published.isnot(None)).order_by(KnowledgeScore.published.desc()).with_entities(
        KnowledgeScore.sys_id, KnowledgeScore.net_votes)
    for article in article_favorite:
        dict={}
        dict['sys_id'] = article.sys_id
        dict['net_votes'] = article.net_votes
        articleSortedByNetVotes.append(dict)
    trendingScoreList = recommendation.return_trending_score(articleSortedByNetVotes,articleSortedByViewList)
    return trendingScoreList


# this function query all article's information used for similarity computation
def get_all_article_similarity():
    all_article = Article.query.all()
    all_article_list = []
    i = 0
    for article in all_article:
        i += 1
        dict = {}
        dict['sys_id'] = article.sys_id
        dict['short_description'] = article.short_description
        dict['body'] = article.text
        all_article_list.append(dict)
    return all_article_list


# this method return date-sorted article with sortable date in db
def get_articles_date():
    articleObjs = Article.query.filter(Article.published.isnot(None)).order_by(Article.published.desc())
    articles = []
    for article in articleObjs:
        dict={}
        dict['id'] = article.sys_id
        dict['date'] = article.published
        articles.append(dict)
    return articles


# return brief info on articles
def get_article_brief_info(article):
    return {'id': article.sys_id if article.sys_id else '',
            'title': article.short_description if article.short_description else '',
            'author': article.author if article.author else '',
            'created': article.published.strftime("%Y-%m-%d") if article.published else ''}


def get_article_all_info(res):
    # return required info about related articles
    def get_related_article_info(article):
        return {'id': article.sys_id if article.sys_id else '',
                'title': article.short_description if article.short_description else '',
                'author': article.author if article.author else '',
                'created': article.published.strftime("%Y-%m-%d") if article.published else '',
                'view_count': article.sys_view_count if article.sys_view_count else 0}

    # return info about the related articles
    def get_related_articles(related_id):
        score_res = RelatedArticles.query.filter_by(sys_id=related_id).order_by(RelatedArticles.score.desc())

        # find related articles' id
        related_ids = [score.number for score in score_res]

        # use one query to find all the info about these articles
        # store info in a dictionary because its lookup complexity is O(1)
        article_res = Article.query.filter(Article.sys_id.in_(related_ids)).all()
        article_id_info = {article.sys_id: get_related_article_info(article) for article in article_res}

        # retrieve article info and output
        return [article_id_info[related_id] for related_id in related_ids]

    return {'id': res.sys_id if res.sys_id else '',
            'title': res.short_description if res.short_description else '',
            'author': res.author if res.author else '',
            'created': res.published.strftime("%Y-%m-%d") if res.published else '',
            'body': res.text if res.text else '',
            'related': get_related_articles(res.sys_id)}


# return article info with a specified id
def get_article_by_id(article_id):
    res = Article.query.filter_by(sys_id=article_id).first()

    # if not exist, return empty dictionary
    if res is None:
        return {}

    # view count + 1
    res.sys_view_count += 1
    db.session.commit()
    return get_article_all_info(res)


# return most recent articles
# sorted by id to make sure the articles are always in the same order
def get_articles_sorted_by_date(limit, start):
    res = Article.query.filter(Article.published.isnot(None)).order_by(Article.published.desc(), Article.sys_id).offset(start).limit(limit)

    return [get_article_brief_info(article) for article in res]


# return articles searched by query
# sorted by date and id to make sure the articles are always in the same order
def get_articles_by_query(query, limit, start):
    res = Article.query.filter(Article.short_description.ilike(f"%{query}%")).order_by(Article.published.desc(), Article.sys_id).offset(start).limit(limit)

    return [get_article_brief_info(article) for article in res]

