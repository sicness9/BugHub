# teams and team management views

from flask import render_template, request, url_for, session, redirect, flash
from flask_cors import cross_origin

from app.utils import requires_auth
from app import db
from app.database.models import Team, User
from .import teams


# teams home page
@teams.route("/team_home", methods=['GET', 'POST'])
@cross_origin(headers=["Content Type", "Authorization"])
@requires_auth
def team_home_page():
    current_user = session['profile']
    all_teams = Team.query.all()

    '''Check number of members for developer team'''
    # query for dev team in table
    dev_team = Team.query.filter_by(team_name='Developer').first()
    # check number of members
    dev_members = 0 + len(User.query.filter_by(team_id=dev_team.id).all())

    '''Check for number of QA members'''
    # query for qa team in table
    qa_team = Team.query.filter_by(team_name='Quality Assurance').first()
    # check number of members
    qa_members = 0 + len(User.query.filter_by(team_id=qa_team.id).all())

    '''Check for number of Support members'''
    # query for support team in table
    support_team = Team.query.filter_by(team_name='Support').first()
    # check number of members
    support_members = 0 + len(User.query.filter_by(team_id=support_team.id).all())

    '''Check for number of Engineer members'''
    # query for support team in table
    eng_team = Team.query.filter_by(team_name='Engineer').first()
    # check number of members
    eng_members = 0 + len(User.query.filter_by(team_id=eng_team.id).all())

    return render_template('teams/team_home_page.html',
                           userinfo=current_user, all_teams=all_teams,
                           dev_members=dev_members, qa_members=qa_members, support_members=support_members,
                           eng_members=eng_members)


# developer team page
@teams.route("/developer_join", methods=['GET', 'POST'])
@cross_origin(headers=["Content Type", "Authorization"])
@requires_auth
def developer_join():
    current_user = session['profile']

    user = User.query.filter_by(email=current_user['name']).first()
    dev_team = Team.query.filter_by(team_name='Developer').first()

    user.team_id = dev_team.id
    db.session.commit()

    return render_template('teams/developer_join_confirm.html', userinfo=current_user)


# QA team page
@teams.route("/QA_join", methods=['GET', 'POST'])
@cross_origin(headers=["Content Type", "Authorization"])
@requires_auth
def qa_join():
    current_user = session['profile']

    user = User.query.filter_by(email=current_user['name']).first()
    dev_team = Team.query.filter_by(team_name='Quality Assurance').first()

    user.team_id = dev_team.id
    db.session.commit()

    return render_template('teams/qa_join_confirm.html', userinfo=current_user)
