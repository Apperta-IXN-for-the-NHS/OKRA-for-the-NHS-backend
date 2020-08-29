from app import recommendation
from app import db
from app import knowledge_score_table, related_article
from app.service import knowledge_service
from app import KnowledgeScore, TestKnowledgeScore


# this method initialise the kb_knowledge_score table using published date by ranking.
def write_trending_to_db():
    article_list = knowledge_service.get_articles_date()
    for article in article_list:
        new_article = knowledge_score_table(sys_id=article['id'], published=article['date'], trending_score=0, net_votes=0)
        db.session.add(new_article)
    db.session.commit()
    return 'success'


# this method is used to update the trending_score in kb_knowledge_score
def update_trending():
    knowledge_trending_score = knowledge_service.get_trending_score_list()
    for knowledge in knowledge_trending_score:
        edited_knowledge = KnowledgeScore.query.get(knowledge)
        edited_knowledge.trending_score = knowledge_trending_score[knowledge]
    db.session.commit()
    return "success"


def update_related():
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
