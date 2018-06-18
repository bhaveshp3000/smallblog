from flask import Flask,redirect,url_for
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_dance.contrib.github import make_github_blueprint,github

app = Flask(__name__)

app.config.from_object(Config)
login = LoginManager(app)
login.login_view = 'login'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

github_blueprint = make_github_blueprint(
    client_id="4496269045dadef27392",
    client_secret="c6f7e53b86f9296fd022cdec5e3e0fbc89dea1ed",
)

app.register_blueprint(github_blueprint,url_prefix='/github_login')



from app import routes, models

