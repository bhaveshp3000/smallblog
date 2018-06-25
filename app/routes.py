from app import app
from app import db
from flask import render_template, redirect, flash, url_for, request
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User,S_User
from werkzeug.urls import url_parse
from oauth import OAuthSignIn





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

@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()

@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('login'))
    user = S_User.query.filter_by(social_id=social_id).first()
    if not user:
        user = S_User(social_id=social_id, nickname=username, email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('index'))
