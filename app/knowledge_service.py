from app import Article


# {
#   id: string,
#   title: string,
#   author: string,
#   created: string,
#   body: string,
#   related: string[] //related articles IDs
# }
def get_article_by_id(id):
    dict = {}
    article = Article.query.filter_by(sys_id=id).first()

    # if exists
    if article is not None:
        dict['id'] = article.sys_id
        dict['title'] = article.short_description
        dict['author'] = article.author
        dict['created'] = article.published.strftime("%Y-%m-%d")
        dict['body'] = article.text
        dict['related'] = None
    return dict


# sorted by date
# {
#   id: string,
#   title: string,
#   author: string,
#   created: string // "2020-08-01"
# }
def get_articles_sorted_by_date(limit, start):
    articleObjs =  Article.query.filter(Article.published.isnot(None)).order_by(Article.published.desc()).offset(start).limit(limit)
    articles = []

    for article in articleObjs:
        dict = {}
        dict['id'] = article.sys_id
        dict['title'] = article.short_description
        dict['author'] = article.author
        dict['created'] = article.published.strftime("%Y-%m-%d")
        articles.append(dict)

    return articles
