"""
This is the module providing services for trending
"""
from app import recommendation
from app import db
from app import knowledge_score_table, related_article
from app.service import knowledge_service
from app import KnowledgeScore, TestKnowledgeScore


def write_trending_to_db():
    """this method initialise the kb_knowledge_score table with articles with date and dummy data.

    :return: a string after code is being executed
    """
    article_list = knowledge_service.get_articles_date()
    for article in article_list:
        new_article = knowledge_score_table(sys_id=article['id'], published=article['date'], trending_score=0, net_votes=0)
        db.session.add(new_article)
    db.session.commit()
    return 'success'


# this method is used to update the trending_score in kb_knowledge_score
def update_trending():
    """this method is used to update the trending_score in kb_knowledge_score,
    where it obtained the list article with trending score from knowledge_services, get_trending_score_list

    :return: a string after code is being executed
    """
    knowledge_trending_score = knowledge_service.get_trending_score_list()
    for knowledge in knowledge_trending_score:
        edited_knowledge = KnowledgeScore.query.get(knowledge)
        edited_knowledge.trending_score = knowledge_trending_score[knowledge]
    db.session.commit()
    return "success"


def update_related():
    """this method is used to update the related articles in related_article table

    it firstly use the method in recommendation engine to obtain the articles with similarity score of all articles,
    then only takes the top 10 similarity scored article from the list and store them in the database.

    :return: list of articles with similarity score of all articles sorted by similarity.
    """
    all_article = knowledge_service.get_all_article_similarity()
    all_article_sorted_by_similarity = recommendation.update_related(all_article)
    TestKnowledgeScore.query.delete()
    db.session.execute('TRUNCATE TABLE related_knowledge')
    for article in all_article_sorted_by_similarity:
        rank = 0
        for article_score in all_article_sorted_by_similarity[article]:
            rank += 1
            if rank <= 10:
                new_related_article = related_article(sys_id=article, number=article_score[0], score=article_score[1])
                db.session.add(new_related_article)
    db.session.commit()
    return all_article_sorted_by_similarity
