from app import db,login
from werkzeug.security import check_password_hash,generate_password_hash
from flask_login import UserMixin

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(84),index=True,unique=True)
    email = db.Column(db.String(120),index=True,unique=True)
    password_hash = db.Column(db.String(120))
    social_id = db.Column(db.String(64), nullable=True, unique=True)
    nickname = db.Column(db.String(64), nullable=True)


    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash, password)

# class S_User(UserMixin, db.Model):
#    __tablename__ = 's_users'
#    id = db.Column(db.Integer, primary_key=True)
#    social_id = db.Column(db.String(64), nullable=False, unique=True)
#    nickname = db.Column(db.String(64), nullable=False)
#    email = db.Column(db.String(64), nullable=True)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
