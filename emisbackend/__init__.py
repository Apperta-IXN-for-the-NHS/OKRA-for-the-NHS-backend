from flask import Flask
from emisbackend.views import api


app = Flask(__name__)
app.register_blueprint(api)

if __name__ == '__main__':
    app.run()
