"""`main` is the top level module for your Flask application."""

# Imports
import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from google.appengine.ext import ndb
from datetime import datetime
app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
    SECRET_KEY='development key',
    DATA_BACKEND='datastore',
    PROJECT_ID='wink-dating',
    DEBUG=True
))
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

import flask_login
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class User(ndb.Model, flask_login.UserMixin):
    """Models a user"""
    #userID = ndb.KeyProperty(kind='userID') #Facebook user ID
    fullName = ndb.StringProperty()
    firstName = ndb.StringProperty()
    lastName = ndb.StringProperty()
    gender = ndb.StringProperty()
    #picture = ndb.StringProperty() #This is an edge, not sure how to work w/ them yet
    birthday = ndb.DateTimeProperty()
    email = ndb.StringProperty()
    link = ndb.StringProperty()
    relationshipStatus = ndb.StringProperty()
    timezoneOffset = ndb.FloatProperty() #Offset from UTC
    createdDate = ndb.DateTimeProperty(auto_now_add=True)
    modifiedDate = ndb.DateTimeProperty(auto_now=True)

    @classmethod
    def query_user(cls, userID):
        return cls.get_by_id(userID)

@login_manager.user_loader
def load_user(userID):
    return User.query_user(userID)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Login and validate the user.
        # user should be an instance of your `User` class
        userID = request.headers.get('x-userID')
        # If user does not exist, create
        user = User.query_user(userID)
        if not user:
            # Interpret birthday
            if request.form.get('birthday').count('/') == 2:
                birthday = datetime.strptime(request.form.get('birthday'),'%m/%d/%Y')
            elif request.form.get('birthday').count('/') == 1:
                birthday = datetime.strptime(request.form.get('birthday'),'%m/%d')
            elif request.form.get('birthday').count('/') == 0:
                birthday = datetime.strptime(request.form.get('birthday'),'%Y')

            # Create user
            user = User(
                id=userID,
                fullName=request.form.get('name'),
                firstName=request.form.get('first_name'),
                lastName=request.form.get('last_name'),
                gender=request.form.get('gender'),
                birthday=birthday,
                email=request.form.get('email'),
                link=request.form.get('link'),
                relationshipStatus=request.form.get('relationship_status'),
                timezoneOffset=float(request.form.get('timezone'))
            )
            user.put()
        # Login user
        user.id = userID
        flask_login.login_user(user)

        flash('Logged in successfully.')

        next = request.args.get('next')
        if not next_is_valid(next):
            return abort(400)

        return redirect(next or url_for('index'))
    return render_template('login.html')

@app.route("/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for('index'))

def next_is_valid(next):
    # next_is_valid should check if the user has valid
    # permission to access the `next` url
    return True

@app.route('/')
def home():
    return render_template('home.html')
"""
# TODO: Remove code, this is pre- flask-login
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        #I think this is all stored in the browser cookie automatically (by the JS SDK)
        #accessToken = request.form.get('accessToken')
        #signedRequest = request.form.get('signedRequest')
        userID = request.headers.get('x-userID')
        # Interpret birthday
        if request.form.get('birthday').count('/') == 2:
            birthday = datetime.strptime(request.form.get('birthday'),'%m/%d/%Y')
        elif request.form.get('birthday').count('/') == 1:
            birthday = datetime.strptime(request.form.get('birthday'),'%m/%d')
        elif request.form.get('birthday').count('/') == 0:
            birthday = datetime.strptime(request.form.get('birthday'),'%Y')
        #If user does not exist, create
        user = User.query_user(userID)
        if not user:
            user = User(
                id=userID,
                fullName=request.form.get('name'),
                firstName=request.form.get('first_name'),
                lastName=request.form.get('last_name'),
                gender=request.form.get('gender'),
                birthday=birthday,
                email=request.form.get('email'),
                link=request.form.get('link'),
                relationshipStatus=request.form.get('relationship_status'),
                timezoneOffset=float(request.form.get('timezone'))
            )
            user.put()
        return True
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))
"""
@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
