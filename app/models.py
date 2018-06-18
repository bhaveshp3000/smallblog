from app import db,login,github_blueprint
from werkzeug.security import check_password_hash,generate_password_hash
from flask_login import UserMixin
from flask_dance.consumer.backend.sqla import OAuthConsumerMixin,SQLAlchemyBackend


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(84),index=True,unique=True)
    email = db.Column(db.String(120),index=True,unique=True)
    password_hash = db.Column(db.String(120))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash, password)


class OAuth(OAuthConsumerMixin, db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)



@login.user_loader
def load_user(id):
    return User.query.get(int(id))