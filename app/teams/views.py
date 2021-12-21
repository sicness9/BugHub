# teams and team management views

from flask import render_template, session, url_for, request, redirect
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

    user = User.query.filter_by(email=current_user['name']).first()

    if user.is_admin is not True:
        return render_template('teams/no_team_invite.html', userinfo=current_user)

    '''
    # Check number of members for developer team
    # query for dev team in table
    dev_team = Team.query.filter_by(team_name='Developer').first()
    # check number of members
    dev_members = 0 + len(User.query.filter_by(team_id=dev_team.id).all())

    # Check for number of QA members
    # query for qa team in table
    qa_team = Team.query.filter_by(team_name='Quality Assurance').first()
    # check number of members
    qa_members = 0 + len(User.query.filter_by(team_id=qa_team.id).all())

    # Check for number of Support members
    # query for support team in table
    support_team = Team.query.filter_by(team_name='Support').first()
    # check number of members
    support_members = 0 + len(User.query.filter_by(team_id=support_team.id).all())

    # Check for number of Engineer members
    # query for support team in table
    eng_team = Team.query.filter_by(team_name='Engineer').first()
    # check number of members
    eng_members = 0 + len(User.query.filter_by(team_id=eng_team.id).all())'''

    return redirect(url_for('teams.create_team'))


# create a team
@teams.route("/team_create", methods=['GET', 'POST'])
@cross_origin(headers=["Content Type", "Authorization"])
@requires_auth
def create_team():
    current_user = session['profile']

    user = User.query.filter_by(email=current_user['name']).first()

    # create new team and send to team dashboard
    if request.method == 'POST':
        team_name = request.form.get('team_name')
        admin_id = user.id

        new_team = Team(team_name=team_name, admin_id=admin_id)
        db.session.add(new_team)
        db.session.commit()

        new_team = Team.query.filter_by(team_name=new_team.team_name).first()

        # update the admin to be assigned to team id
        user.team_id = new_team.id
        db.session.commit()

        return redirect(url_for('dashboard.dashboard'))

    return render_template('teams/create_team.html', userinfo=current_user)


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

    # grab current team to pass to the next template
    current_team = Team.query.filter_by(id=user.team_id).first()

    return render_template('teams/team_join_confirmed.html', userinfo=current_user, current_team=current_team)


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

    # grab current team to pass to the next template
    current_team = Team.query.filter_by(id=user.team_id).first()

    return render_template('teams/team_join_confirmed.html', userinfo=current_user, current_team=current_team)


# support team page
@teams.route("/support_join", methods=['GET', 'POST'])
@cross_origin(headers=["Content Type", "Authorization"])
@requires_auth
def support_join():
    current_user = session['profile']

    user = User.query.filter_by(email=current_user['name']).first()
    support_team = Team.query.filter_by(team_name='Support').first()

    user.team_id = support_team.id
    db.session.commit()

    # grab current team to pass to the next template
    current_team = Team.query.filter_by(id=user.team_id).first()

    return render_template('teams/team_join_confirmed.html', userinfo=current_user, current_team=current_team)


# engineer team page
@teams.route("/engineer_join", methods=['GET', 'POST'])
@cross_origin(headers=["Content Type", "Authorization"])
@requires_auth
def engineer_join():
    current_user = session['profile']

    user = User.query.filter_by(email=current_user['name']).first()
    support_team = Team.query.filter_by(team_name='Engineer').first()

    user.team_id = support_team.id
    db.session.commit()

    # grab current team to pass to the next template
    current_team = Team.query.filter_by(id=user.team_id).first()

    return render_template('teams/team_join_confirmed.html', userinfo=current_user, current_team=current_team)
