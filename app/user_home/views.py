# user home page views

import re

from flask import render_template, request, url_for, session, redirect, flash
from flask_cors import cross_origin

from app.utils import requires_auth
from app import db
from app.database.models import User, Team, Ticket, TeamMember
from . import user_home


# user home page
@user_home.route("/user_home", methods=['GET', 'POST'])
@cross_origin(headers=["Content Type", "Authorization"])
@requires_auth
def user_home_page():
    current_user = session['profile']
    user = User.query.filter_by(email=current_user['name']).first()
    team = Team.query.filter_by(id=user.team_id).first()

    if team is not None:
        all_tickets = Ticket.query.filter_by(team_id=team.id).all()  # for search bar
    else:
        all_tickets = Ticket.query.filter_by(owner_id=user.id).all()

    # check if username, first_name or last_name is missing in DB.
    # If yes, provide screen so they can add the missing information

    if user.username is None:
        return render_template('user_home/user_profile_missing_username.html',
                               userinfo=current_user, user=user, all_tickets=all_tickets)
    elif user.first_name is None:
        return render_template('user_home/user_profile_missing_first_name.html',
                               userinfo=current_user, user=user, all_tickets=all_tickets)
    elif user.last_name is None:
        return render_template('user_home/user_profile_missing_last_name.html',
                               userinfo=current_user, user=user, all_tickets=all_tickets)

    return render_template("user_home/user_home.html", userinfo=current_user, user=user,
                           team=team, all_tickets=all_tickets)


# after initial sign-in or sign-up ask for profile information
@user_home.route("/setup_profile", methods=['GET', 'POST'])
@cross_origin(headers=["Content Type", "Authorization"])
@requires_auth
def init_profile():
    current_user = session['profile']
    user = User.query.filter_by(email=current_user['name']).first()
    team = Team.query.filter_by(id=user.team_id).first()

    if team is not None:
        all_tickets = Ticket.query.filter_by(team_id=team.id).all()  # for search bar
    else:
        all_tickets = Ticket.query.filter_by(owner_id=user.id).all()

    if user.username is not None and user.invite_status == 2 and user.role_id is None:
        return redirect(url_for('user_home.accept_invite'))
    # if account has an existing username, redirect to main profile page and avoid add form
    if user.username is not None:
        return redirect(url_for('user_home.user_home_page'))

    return render_template('user_home/user_profile_add_form.html',
                           userinfo=current_user, user=user, all_tickets=all_tickets)


# accept invite for existing accounts
@user_home.route("/accept_invite", methods=['GET', 'POST'])
@cross_origin(headers=["Content Type", "Authorization"])
@requires_auth
def accept_invite():
    current_user = session['profile']
    user = User.query.filter_by(email=current_user['name']).first()
    team = Team.query.filter_by(id=user.team_id).first()

    if team is not None:
        all_tickets = Ticket.query.filter_by(team_id=team.id).all()  # for search bar
    else:
        all_tickets = Ticket.query.filter_by(owner_id=user.id).all()

    if request.method == 'POST':
        role_id = request.form.get('role_id')

        # update role_id and invite_status on user table
        user.role_id = role_id
        db.session.commit()

        # create entry in member table
        new_member = TeamMember(user_id=user.id, role_id=user.role_id, admin_id=team.admin_id, team_name=team.team_name)
        db.session.add(new_member)
        db.session.commit()
        return redirect(url_for('user_home.user_home_page'))

    return render_template('user_home/accept_invite.html', userinfo=current_user, user=user, all_tickets=all_tickets)


# add user profile information to User db
@user_home.route("/profile_added", methods=['GET', 'POST', 'PATCH'])
@cross_origin(headers=["Content Type", "Authorization"])
@requires_auth
def add_profile():
    current_user = session['profile']
    form_data = request.form

    user = User.query.filter_by(email=current_user['name']).first()
    team = Team.query.filter_by(id=user.team_id).first()

    if team is not None:
        all_tickets = Ticket.query.filter_by(team_id=team.id).all()  # for search bar
    else:
        all_tickets = Ticket.query.filter_by(owner_id=user.id).all()

    current_team = user.team

    if request.method == 'POST':
        '''Validate username'''
        entered_username = request.form.get('username')

        # some validation for username and add username
        if User.query.filter_by(username=entered_username).first():
            flash("Username already exists", category='error')
            return render_template('user_home/user_profile_add_form.html', userinfo=current_user)
        if entered_username is None:
            flash("Username can not be blank", category='error')
            return render_template('user_home/user_profile_add_form.html', userinfo=current_user)
        if len(entered_username) < 3:
            flash("Username must be 4 characters or greater", category='error')
            return render_template('user_home/user_profile_add_form.html', userinfo=current_user)
        if len(entered_username) > 15:
            flash("Username is too long", category='error')
            return render_template('user_home/user_profile_add_form.html', userinfo=current_user)
        else:
            user.username = entered_username

        '''Validate first name'''
        entered_firstname = request.form.get('first_name')
        # validate first name to contain only letters
        fn_val = re.compile(r"[A-za-z]+")

        # validate first name and add to db
        if entered_firstname is None:
            flash("First name can not be blank", category='error')
            return render_template('user_home/user_profile_add_form.html', userinfo=current_user)
        if bool(re.fullmatch(fn_val, entered_firstname)) is False:
            flash("First name must contain letters only", category='error')
            return render_template('user_home/user_profile_add_form.html', userinfo=current_user)
        if len(entered_firstname) < 3:
            flash("First name must be 3 characters or greater", category='error')
            return render_template('user_home/user_profile_add_form.html', userinfo=current_user)
        if len(entered_firstname) > 12:
            flash("First name is too long", category='error')
            return render_template('user_home/user_profile_add_form.html', userinfo=current_user)
        else:
            user.first_name = request.form.get('first_name')

        '''Validate the last name'''
        entered_lastname = request.form.get('last_name')
        # validate last name to contain only letters
        ln_val = re.compile(r"[A-za-z]+")

        # validate last name and add to db
        if entered_lastname is None:
            flash("Last name can not be blank", category='error')
            return render_template('user_home/user_profile_add_form.html', userinfo=current_user)
        if bool(re.fullmatch(ln_val, entered_lastname)) is False:
            flash("Last name must contain letters only", category='error')
            return render_template('user_home/user_profile_add_form.html', userinfo=current_user)
        if len(entered_lastname) < 3:
            flash("Last name must be 3 characters or greater", category='error')
            return render_template('user_home/user_profile_add_form.html', userinfo=current_user)
        if len(entered_lastname) > 12:
            flash("Last name is too long", category='error')
            return render_template('user_home/user_profile_add_form.html', userinfo=current_user)
        else:
            user.last_name = request.form.get('last_name')

        role_id = request.form.get('role')

        # update user table
        user.role_id = role_id

        # add to team_members table
        if current_team is not None:
            member_add = TeamMember(team_name=current_team.team_name, admin_id=current_team.admin_id, role_id=role_id,
                                    user_id=user.id)
            db.session.add(member_add)
        else:
            pass

        '''if is_admin:
            user.is_admin = True'''

        db.session.commit()
    return render_template('user_home/profile_added.html', userinfo=current_user, form_data=form_data,
                           all_tickets=all_tickets)


# update username
@user_home.route("/username_updated", methods=['GET', 'POST', 'PATCH'])
@cross_origin(headers=["Content Type", "Authorization"])
@requires_auth
def update_username():
    current_user = session['profile']

    user = User.query.filter_by(email=current_user['name']).first()
    team = Team.query.filter_by(id=user.team_id).first()

    if team is not None:
        all_tickets = Ticket.query.filter_by(team_id=team.id).all()  # for search bar
    else:
        all_tickets = Ticket.query.filter_by(owner_id=user.id).all()

    if request.method == 'POST':

        # existing_usernames = User.query.all()
        entered_username = request.form.get('username')

        # some validation for username
        if User.query.filter_by(username=entered_username).first():
            flash("Username already exists", category='error')
            return render_template('user_home/update_username.html', userinfo=current_user)
        if entered_username is None:
            flash("Username can not be blank", category='error')
            return render_template('user_home/update_username.html', userinfo=current_user)
        if len(entered_username) < 3:
            flash("Username must be 4 characters or greater", category='error')
            return render_template('user_home/update_username.html', userinfo=current_user)
        if len(entered_username) > 12:
            flash("Username is too long", category='error')
            return render_template('user_home/update_username.html', userinfo=current_user)
        else:
            user.username = request.form.get('username')
            db.session.commit()
            return redirect(url_for('user_home.user_home_page'))

    return render_template('user_home/update_username.html', userinfo=current_user, user=user, all_tickets=all_tickets)


# update first_name
@user_home.route("/first_name_updated", methods=['GET', 'POST', 'PATCH'])
@cross_origin(headers=["Content Type", "Authorization"])
@requires_auth
def update_first_name():
    current_user = session['profile']
    form_data = request.form

    user = User.query.filter_by(email=current_user['name']).first()
    team = Team.query.filter_by(id=user.team_id).first()

    if team is not None:
        all_tickets = Ticket.query.filter_by(team_id=team.id).all()  # for search bar
    else:
        all_tickets = Ticket.query.filter_by(owner_id=user.id).all()

    if request.method == 'POST':
        entered_firstname = request.form.get('first_name')

        # validate first name to contain only letters
        val = re.compile(r"[A-za-z]+")

        # validate first name and add to db
        if entered_firstname is None:
            flash("First name can not be blank", category='error')
            return render_template('user_home/update_first_name.html', userinfo=current_user)
        if bool(re.fullmatch(val, entered_firstname)) is False:
            flash("First name must contain letters only", category='error')
            return render_template('user_home/update_first_name.html', userinfo=current_user)
        if len(entered_firstname) < 3:
            flash("First name must be 3 characters or greater", category='error')
            return render_template('user_home/update_first_name.html', userinfo=current_user)
        if len(entered_firstname) > 12:
            flash("First name is too long", category='error')
            return render_template('user_home/update_first_name.html', userinfo=current_user)
        else:
            user.first_name = request.form.get('first_name')
            db.session.commit()
            return redirect(url_for('user_home.user_home_page'))

    return render_template('user_home/update_first_name.html', userinfo=current_user, form_data=form_data, user=user,
                           all_tickets=all_tickets)


# update last_name
@user_home.route("/last_name_updated", methods=['GET', 'POST', 'PATCH'])
@cross_origin(headers=["Content Type", "Authorization"])
@requires_auth
def update_last_name():
    current_user = session['profile']
    form_data = request.form

    user = User.query.filter_by(email=current_user['name']).first()
    team = Team.query.filter_by(id=user.team_id).first()

    if team is not None:
        all_tickets = Ticket.query.filter_by(team_id=team.id).all()  # for search bar
    else:
        all_tickets = Ticket.query.filter_by(owner_id=user.id).all()

    if request.method == 'POST':
        entered_lastname = request.form.get('last_name')
        # validate last name to contain only letters
        ln_val = re.compile(r"[A-za-z]+")

        # validate last name and add to db
        if entered_lastname is None:
            flash("Last name can not be blank", category='error')
            return render_template('user_home/update_last_name.html', userinfo=current_user)
        if bool(re.fullmatch(ln_val, entered_lastname)) is False:
            flash("Last name must contain letters only", category='error')
            return render_template('user_home/update_last_name.html', userinfo=current_user)
        if len(entered_lastname) < 3:
            flash("Last name must be 3 characters or greater", category='error')
            return render_template('user_home/update_last_name.html', userinfo=current_user)
        if len(entered_lastname) > 12:
            flash("Last name is too long", category='error')
            return render_template('user_home/update_last_name.html', userinfo=current_user)
        else:
            user.last_name = request.form.get('last_name')
            db.session.commit()
            return redirect(url_for('user_home.user_home_page'))

    return render_template('user_home/update_last_name.html', userinfo=current_user, form_data=form_data, user=user,
                           all_tickets=all_tickets)


# team view page
@user_home.route("/my_team", methods=['GET', 'POST'])
@cross_origin(headers=["Content Type", "Authorization"])
@requires_auth
def my_team():
    current_user = session['profile']

    user = User.query.filter_by(email=current_user['name']).first()
    members = User.query.filter_by(team_id=user.team_id).all()
    team = Team.query.filter_by(id=user.team_id).first()
    # print(members)

    if team is not None:
        all_tickets = Ticket.query.filter_by(team_id=team.id).all()  # for search bar
    else:
        all_tickets = Ticket.query.filter_by(owner_id=user.id).all()

    # if no team joined yet, have the user join one first
    if user.team_id is None:
        return render_template('user_home/join_team.html', userinfo=current_user, user=user, all_tickets=all_tickets)

    return render_template('user_home/my_team.html', members=members, userinfo=current_user, user=user, team=team)


# User ticket view
@user_home.route("/my_tickets", methods=['GET', 'POST'])
@cross_origin(headers=["Content Type", "Authorization"])
@requires_auth
def my_tickets():
    current_user = session['profile']

    user = User.query.filter_by(email=current_user['name']).first()
    tickets = Ticket.query.filter_by(owner_id=user.id).all()
    team = Team.query.filter_by(id=user.team_id).first()

    if team is not None:
        all_tickets = Ticket.query.filter_by(team_id=team.id).all()  # for search bar
    else:
        all_tickets = Ticket.query.filter_by(owner_id=user.id).all()

    return render_template('user_home/my_tickets.html', userinfo=current_user, tickets=tickets, all_tickets=all_tickets)
