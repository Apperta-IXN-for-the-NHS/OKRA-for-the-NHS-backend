from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:%40EMIS123@162.62.53.126:5432/emis_ml_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.Model.metadata.reflect(db.engine)

class Article(db.Model):
    __table__ = db.Model.metadata.tables['kb_knowledge']


from app.views import api
app.register_blueprint(api)
