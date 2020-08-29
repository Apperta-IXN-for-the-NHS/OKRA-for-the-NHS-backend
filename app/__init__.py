"""
This module contains the Flask configuration and Flask-SQLAlchemy configuration.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:%40EMIS123@162.62.53.126:5432/emis_ml_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.Model.metadata.reflect(db.engine)


Base = automap_base()
Base.prepare(db.engine, reflect=True)
knowledge_score_table = Base.classes.kb_knowledge_score
related_article = Base.classes.related_knowledge


# get table schema
class Article(db.Model):
    """This is the class represents the kb_knowledge table in db.

    This class has the following attribute:
    - sys_id: article id
    - short_description: article title
    - author: article author
    - published: the published date of article
    - text: article body
    - sys_view_count: view count of article
    """
    __table__ = db.Model.metadata.tables['kb_knowledge']


class RelatedArticles(db.Model):
    """This is the class represents the related_knowledge table in db.

    This class has the following attribute:
    - id: auto-generated primary key
    - sys_id: article id
    - number: related article id
    - score: similarity score
    """
    __table__ = db.Model.metadata.tables['related_knowledge']


class KnowledgeScore(db.Model):
    """This is the class represents the kb_knowledge_score table in db.

    This class has the following attribute:
    - sys_id: article id
    - trending_score: trending score of article
    - net_votes: vote score of article
    - published: the published date of article
    """
    __table__ = db.Model.metadata.tables['kb_knowledge_score']


class Case(db.Model):
    """This is the class represents the case table in db.

    This class has the following attribute:
    - sys_id: case id
    - short_description: case title
    - content: case content
    - priority: case priority
    - submitted: submitted date of case
    """
    __table__ = db.Model.metadata.tables['case']


class SearchHistory(db.Model):
    """This is the class represents the search_history table in db.

    This class has the following attribute:
    - id: auto-generated primary key
    - type: knowledge or case
    - content: query content
    - search_date: the date and time of search
    """
    __table__ = db.Model.metadata.tables['search_history']


class TestKnowledgeScore(db.Model):
    __table__ = db.Model.metadata.tables['test_related']


from app.controller import api
app.register_blueprint(api)
