"""`main` is the top level module for your Flask application."""

# Imports
import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
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


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        accessToken = request.form.get('accessToken')
        signedRequest = request.form.get('signedRequest')
        userID = request.form.get('userID')
        #session['logged_in'] = True
        return userID
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
