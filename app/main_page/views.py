# main page views

from flask import render_template, redirect, url_for, session
from flask_cors import cross_origin

from . import main_page
from app.utils import requires_auth
from app.database.models import Ticket


# main page but redirect to log in first
@main_page.route('/', methods=['GET', 'POST'])
def main_redirect():

    return redirect(url_for('auth.login'))


# main page
@main_page.route('/main', methods=['GET', 'POST'])
@main_page.route('/main/', methods=['GET', 'POST'])
@cross_origin(headers=["Content Type", "Authorization"])
@requires_auth
def main():
    all_tickets = Ticket.query.all()  # all tickets available for search function

    return render_template('main_page/main_page.html', userinfo=session['profile'], all_tickets=all_tickets)
