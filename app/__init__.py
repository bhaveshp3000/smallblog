from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)

app.config.from_object(Config)
login = LoginManager(app)
login.login_view = 'login'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.config['OAUTH_CREDENTIALS'] = {
    'facebook': {
        'id': '2066031190332012',
        'secret': '63f2a58a5285fe1e59a96e99c19bbf0c'
    },
    'twitter': {
        'id': 'j7y8rKsd6yvQ49keY1xemtgLj',
        'secret': '15y5Z5zON1NXWLkmsnoQBgZJNB2wPYBuCJgEJIi4gxQsEhAkEd'
    }
}

from app import routes, models
