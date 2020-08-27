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
    __table__ = db.Model.metadata.tables['kb_knowledge']


class RelatedArticles(db.Model):
    __table__ = db.Model.metadata.tables['related_knowledge']


class KnowledgeScore(db.Model):
    __table__ = db.Model.metadata.tables['kb_knowledge_score']


class TestKnowledgeScore(db.Model):
    __table__ = db.Model.metadata.tables['test_related']


from app.controller import api
app.register_blueprint(api)

