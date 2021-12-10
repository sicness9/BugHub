# main page views

from flask import render_template, redirect, url_for, session
from . import main_page


# main page
@main_page.route('/main')
def main():
    return render_template('main_page.html', userinfo=session['profile'])


# main page but redirect to log in first
@main_page.route('/')
def main_redirect():
    return redirect(url_for('auth.login'))
