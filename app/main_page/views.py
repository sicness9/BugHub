# main page views

from flask import render_template, redirect, url_for, session
from flask_cors import cross_origin

from . import main_page
from app.utils import requires_auth
from app.database.models import Ticket, User, Team


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
    current_user = session['profile']
    user = User.query.filter_by(email=current_user['name']).first()
    team = Team.query.filter_by(id=user.team_id).first()

    if team is not None:
        all_tickets = Ticket.query.filter_by(team_id=team.id).all()  # for search bar
    else:
        all_tickets = Ticket.query.filter_by(owner_id=user.id).all()

    return render_template('main_page/main_page.html', userinfo=session['profile'], all_tickets=all_tickets)
