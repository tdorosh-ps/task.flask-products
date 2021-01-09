from flask import Flask

from config import DATABASE_CONNECTION_URI
from models import db
from schemas import ma
from caches import cache
from api import api


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_CONNECTION_URI

db.init_app(app)
ma.init_app(app)
cache.init_app(app)

app.register_blueprint(api, url_prefix='/api/v1')


if __name__ == '__main__':
    app.run(debug=True)
