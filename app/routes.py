from app import app
from app import db
from flask import render_template, redirect, flash, url_for, request
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User,OAuth
from werkzeug.urls import url_parse
from app import github_blueprint,make_github_blueprint,github
from flask_dance.consumer import oauth_authorized
from flask_dance.consumer.backend.sqla import SQLAlchemyBackend
from sqlalchemy.orm.exc import NoResultFound






@app.route('/')
@app.route('/index')
@login_required
def index():
   # user = {'username':'Jeff'}
     return render_template('index.html', title='Home')

@app.route('/login',methods=['post','get'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
       # flash('Login request for user {},remember_me={}'.format(form.username.data,form.remember_me.data))
       user = User.query.filter_by(username=form.username.data).first()
       if user is None or not user.check_password(form.password.data):
           flash('Invalid username or password')
           return redirect(url_for('login'))
       login_user(user,remember=form.remember_me.data)
       next_page=request.args.get('next')
       if not next_page or url_parse(next_page).netloc !='':
           next_page=url_for('index')
       return redirect(next_page)


       #return redirect(url_for('/index'))

    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/github')
def github_login():
    if not github.authorized:
        return redirect(url_for('github.login'))
    resp = github.get("/user")
    assert resp.ok
    return "You are @{login} on GitHub".format(login=resp.json()["login"])

github_blueprint.backend = SQLAlchemyBackend(OAuth,db.session,user=current_user)

@oauth_authorized.connected_to(github_blueprint)
def github_logged_in(blueprint,token):

    resp = blueprint.session.get('/user')

    if resp.ok:
        resp_json = resp.json()
        username = resp_json['login']

        query = User.query.filter_by(username=username)

        try:
            user = query.one()

        except NoResultFound:
            user = User(username=username)
            db.session.add(user)
            db.session.commit()

        logout_user(user)