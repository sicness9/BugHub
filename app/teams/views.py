# teams and team management views

from flask import render_template, session, url_for, request, redirect, flash
from flask_cors import cross_origin

from app.utils import requires_auth, send_email
from app import db
from app.database.models import Team, User, TeamMember, Ticket
from . import teams


# teams home page
@teams.route("/team_home", methods=['GET', 'POST'])
@cross_origin(headers=["Content Type", "Authorization"])
@requires_auth
def team_home_page():
    current_user = session['profile']

    user = User.query.filter_by(email=current_user['name']).first()
    team = Team.query.filter_by(id=user.team_id).first()

    all_tickets = Ticket.query.filter_by(team_id=team.id).all()  # for search bar

    if user.is_admin is not True:
        return render_template('teams/no_team_invite.html', userinfo=current_user, all_tickets=all_tickets)

    return redirect(url_for('teams.create_team'))


# create a team
@teams.route("/team_create", methods=['GET', 'POST'])
@cross_origin(headers=["Content Type", "Authorization"])
@requires_auth
def create_team():
    current_user = session['profile']

    user = User.query.filter_by(email=current_user['name']).first()
    team = Team.query.filter_by(id=user.team_id).first()

    all_tickets = Ticket.query.filter_by(team_id=team.id).all()  # for search bar

    # create new team and send to team dashboard
    if request.method == 'POST':
        team_name = request.form.get('team_name')

        if len(team_name) > 15:
            flash("Team name is too long, must be 15 characters or less", category='error')
            return render_template('teams/create_team.html', userinfo=current_user, all_tickets=all_tickets)
        if Team.query.filter_by(team_name=team_name).first():
            flash("This team name already exists", category='error')
            return render_template('teams/create_team.html', userinfo=current_user, all_tickets=all_tickets)

        admin_id = user.id

        new_team = Team(team_name=team_name, admin_id=admin_id)

        db.session.add(new_team)
        db.session.commit()

        new_team = Team.query.filter_by(team_name=new_team.team_name).first()
        member_add = TeamMember(admin_id=user.id, role_id=5, user_id=user.id,
                                team_name=new_team.team_name)

        # update the admin to be assigned to team id
        user.team_id = new_team.id
        user.is_admin = True
        user.role_id = 5  # 5 is admin role in db

        db.session.add(member_add)
        db.session.commit()

        return redirect(url_for('dashboard.dashboard_main'))

    return render_template('teams/create_team.html', userinfo=current_user, all_tickets=all_tickets)


# invite member
@teams.route('/invite_member', methods=['GET', 'POST'])
@cross_origin(headers=["Content Type", "Authorization"])
@requires_auth
def invite_members():
    current_user = session['profile']

    user = User.query.filter_by(email=current_user['name']).first()
    team = Team.query.filter_by(id=user.team_id).first()

    all_tickets = Ticket.query.filter_by(team_id=team.id).all()  # for search bar

    existing_team_user_list = []
    invited_users = []

    if request.method == 'POST':
        members_emails = request.form.get('members_input')
        members_split = str(members_emails).strip(', ')
        # print("stripped:", members_split)
        members = members_split.split(',')
        # print("split:", members)

        for member in members[:]:
            new_email = member

            check_existing = User.query.filter_by(email=new_email).first()

            if check_existing and check_existing.team_id is not None:
                # print("Invited member has an existing team:", check_existing.email, "team:", check_existing.team)
                existing_team_user_list.append(check_existing)
                continue

            # check if entered email exists in db and does not have an existing team
            if check_existing is not None and check_existing.team_id is None:
                check_existing.invite_status = 1
                check_existing.team_id = user.team_id
                db.session.commit()

                # send email invite with SendGrid
                send_email(check_existing.email)

                invited_users.append(check_existing)
                print("Successfully invited existing account", check_existing)
                continue

            if check_existing is None:
                # switch invite status to 1 for invited and assign them to the same team as the inviting admin
                new_member = User(email=new_email, invite_status=1, team_id=user.team_id)
                invited_users.append(new_member)

                db.session.add(new_member)

                # send invite email to all invitees with Sendgrid
                send_email(new_member.email)

                print("Successfully invited", new_member)
                continue

            user = str(invited_users).strip(', ').split()
            invited_users.append(user)

            existing_team_user = str(existing_team_user_list).strip(', ').split()
            existing_team_user_list.append(existing_team_user)

        # print("existing user list:", existing_team_user_list)
        # print("Invited existing accounts:", invited_existing)

        db.session.commit()
        return render_template('teams/invite_confirm.html', userinfo=current_user,
                               existing_user_list=existing_team_user_list, new_user_list=invited_users,
                               all_tickets=all_tickets)

    # print("existing member list:", existing_team_user_list)
    return render_template('teams/invite_member_form.html', userinfo=current_user, user=user, all_tickets=all_tickets)


# leave team
@teams.route('/leave_team', methods=['GET', 'POST', 'DELETE'])
@cross_origin(headers=["Content Type", "Authorization"])
@requires_auth
def leave_team():
    current_user = session['profile']
    user = User.query.filter_by(email=current_user['name']).first()
    member = TeamMember.query.filter_by(user_id=user.id).first()

    # remove team id and reset invite status
    user.team_id = None
    user.invite_status = 0
    user.role_id = None

    # clear from the members table
    db.session.delete(member)
    db.session.commit()

    return redirect(url_for('main_page.main'))


# delete a team
@teams.route('/delete_team', methods=['GET', 'POST', 'DELETE'])
@cross_origin(headers=["Content Type", "Authorization"])
@requires_auth
def delete_team():
    current_user = session['profile']
    user = User.query.filter_by(email=current_user['name']).first()
    member = TeamMember.query.filter_by(user_id=user.id).first()
    team = Team.query.filter_by(id=user.team_id).first()

    team_name = request.form.get('delete_team')
    print("team_name:", team_name, "team.team_name:", team.team_name)
    if team_name != team.team_name:
        flash("Entered team name does not match", category='error')
        return redirect(url_for('user_home.my_team'))
    if request.form.get('delete_team') is None:
        flash("Team name field was empty", category='error')
        return redirect(url_for('user_home.my_team'))
    else:
        # remove team id and reset invite status
        user.team_id = None
        user.invite_status = 0
        user.role_id = None

        # clear from the members table
        db.session.delete(member)

        # delete team from db
        db.session.delete(team)

        db.session.commit()

    return redirect(url_for('main_page.main'))


# transfer ownership
@teams.route('/transfer_team', methods=['GET', 'POST', 'DELETE'])
@cross_origin(headers=["Content Type", "Authorization"])
@requires_auth
def transfer_team_ownership():
    current_user = session['profile']

    user = User.query.filter_by(email=current_user['name']).first()
    team = Team.query.filter_by(id=user.team_id).first()
    member_table_entry = TeamMember.query.filter_by(user_id=user.id).first()

    # remove the admin from the team and member table
    user.role_id = None
    user.team_id = None
    db.session.delete(member_table_entry)

    # new owner comes in as ID format from the form
    new_owner_input = request.form.get('new_owner')
    new_owner = User.query.filter_by(id=new_owner_input).first()
    member_table = TeamMember.query.filter_by(team_name=team.team_name).first()

    # update the member table and team ables
    member_table.admin_id = new_owner.id
    team.admin_id = new_owner.id
    new_owner.role_id = 5  # set user to admin role
    new_owner.is_admin = True

    db.session.commit()

    return redirect(url_for('main_page.main'))


# update team role
@teams.route('/change_role', methods=['GET', 'POST'])
@cross_origin(headers=["Content Type", "Authorization"])
@requires_auth
def change_role():
    current_user = session['profile']
    user = User.query.filter_by(email=current_user['name']).first()
    member = TeamMember.query.filter_by(user_id=user.id).first()

    new_role = request.form.get('role')
    print("new role", new_role)

    user.role_id = new_role  # update role on user table
    member.role_id = new_role  # update role on member table
    db.session.commit()

    return redirect(url_for('user_home.my_team'))
