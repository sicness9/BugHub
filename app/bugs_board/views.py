# bugs board views

from flask import render_template, request, url_for, session, redirect, flash
from flask_cors import cross_origin

from app.utils import requires_auth
from app import db
from app.database.models import User, Team, Ticket
from . import bugs_board


# bugs board main view
@bugs_board.route('/', methods=['GET', 'POST'])
@cross_origin(headers=["Content Type", "Authorization"])
@requires_auth
def bugs_main():
    current_user = session['profile']
    user = User.query.filter_by(email=current_user['name']).first()
    team = Team.query.filter_by(id=user.team_id).first()

    in_progress_tickets = Ticket.query.filter_by(status='In Progress', team_id=team.id).all()

    '''in_progress_tickets = []
    for ticket in in_progress:
        owner = ticket.owner
        if team.id != owner.team_id:
            continue

        in_progress_tickets.append(ticket)'''

    pending_triage_tickets = Ticket.query.filter_by(status='Pending Triage', team_id=team.id).all()

    '''pending_triage_tickets = []
    for ticket in pending_triage:
        owner = ticket.owner
        if team.id != owner.team_id:
            continue

        pending_triage.append(ticket)'''

    closed_tickets = Ticket.query.filter_by(status='Closed', team_id=team.id).all()

    '''closed_tickets = []
    for ticket in closed_tickets_query:
        owner = ticket.owner
        if team.id != owner.team_id:
            continue

        closed_tickets.append(ticket)'''

    todo_tickets = Ticket.query.filter_by(status='To Do', team_id=team.id).all()

    '''todo_tickets = []
    for ticket in todo_tickets_query:
        owner = ticket.owner
        if team.id != owner.team_id:
            continue

        todo_tickets.append(ticket)'''

    all_tickets = Ticket.query.filter_by(team_id=team.id).all()  # for search bar

    '''all_tickets = []
    for ticket in all_tickets_query:
        owner = ticket.owner
        if team.id != owner.team_id:
            continue

        all_tickets.append(ticket)'''

    return render_template('bugs_board/bugs_main.html', userinfo=current_user,
                           in_progress_tickets=in_progress_tickets, pending_triage_tickets=pending_triage_tickets,
                           closed_tickets=closed_tickets, todo_tickets=todo_tickets, all_tickets=all_tickets, user=user,
                           team=team)


# ticket creation form
@bugs_board.route('/create_ticket', methods=['GET', 'POST'])
@cross_origin(headers=["Content Type", "Authorization"])
@requires_auth
def create_ticket():
    current_user = session['profile']
    user = User.query.filter_by(email=current_user['name']).first()
    team = Team.query.filter_by(id=user.team_id).first()
    all_tickets = Ticket.query.filter_by(team_id=team.id).all()  # for search bar

    if request.method == 'POST':
        title = request.form.get('title')
        ticket_description = request.form.get('ticket_description')
        bucket = request.form.get('bucket')
        status = request.form.get('status')
        owner_id = user.id
        team_id = user.team_id

        if len(title) < 1:
            flash("Title can not empty", category='error')
        elif len(ticket_description) < 1:
            flash("Description can not be blank", category='error')
        elif bucket == 'Choose...':
            flash("Ticket must have a ticket type", category='error')
        elif status == 'Choose...':
            flash("Ticket must have a status", category='error')
        else:
            new_ticket = Ticket(title=title, ticket_description=ticket_description, bucket=bucket, status=status,
                                owner_id=owner_id, team_id=team_id)
            user.tickets += 1
            db.session.add(new_ticket)
            db.session.commit()

            return redirect(url_for('bugs_board.bugs_main'))

    return render_template('bugs_board/create_ticket.html', userinfo=current_user, user=user, all_tickets=all_tickets)


# make a view for ticket information based on ticket number
@bugs_board.route('/browse/<id>', methods=['GET', 'POST'])
@cross_origin(headers=["Content Type", "Authorization"])
@requires_auth
def view_ticket(id):
    current_user = session['profile']
    user = User.query.filter_by(email=current_user['name']).first()
    team = Team.query.filter_by(id=user.team_id).first()
    all_tickets = Ticket.query.filter_by(team_id=team.id).all()  # for search bar

    # take the input from the search and split it to grab the ID value only
    form_search = request.form.get('id')
    form_split = form_search.split()

    id = form_split[0]

    # query for ticket by the id and its owner
    ticket = Ticket.query.filter_by(id=id).first()
    ticket_owner = User.query.filter_by(id=ticket.owner_id).first()

    # Query for all users on the same team to allow for ticket assignment
    active_team_users = User.query.filter_by(team_id=team.id).all()

    return render_template('bugs_board/ticket.html', userinfo=current_user, ticket=ticket, id=id,
                           ticket_owner=ticket_owner, active_team_users=active_team_users,
                           all_tickets=all_tickets, user=user)


# make updates to the ticket
@bugs_board.route('/update/<id>', methods=['GET', 'POST'])
@cross_origin(headers=["Content Type", "Authorization"])
@requires_auth
def update_ticket(id):
    current_user = session['profile']

    user = User.query.filter_by(email=current_user['name']).first()
    ticket = Ticket.query.filter_by(id=id).first()
    ticket_owner = User.query.filter_by(id=ticket.owner_id).first()
    team = Team.query.filter_by(id=user.team_id).first()

    all_tickets = Ticket.query.filter_by(team_id=team.id).all()  # for search bar

    # update ticket information
    if request.method == 'POST':

        ticket.title = request.form.get('title')
        ticket.ticket_description = request.form.get('ticket_description')
        ticket.bucket = request.form.get('bucket')
        ticket.status = request.form.get('status')

        # grab new owner from data list
        owner_select = request.form.get('owner_id')
        # print("owner select:", owner_select)

        if owner_select is None:
            ticket.owner_id = ticket.owner_id
        else:
            try:
                # split the input
                select_split = owner_select.split()
                # print("split:", select_split)

                # grab first element for the ID
                owner_id = select_split[0]
                # print("owner_id:", owner_id)

                # query for the new owner and assign into new_owner variable
                new_owner = User.query.filter_by(id=owner_id).first()

                ticket.owner_id = new_owner.id
            except:
                pass

        flash("Changes saved", category="success")
        db.session.commit()

    return render_template('bugs_board/ticket.html', userinfo=current_user, id=ticket.id, ticket=ticket,
                           ticket_owner=ticket_owner, all_tickets=all_tickets, user=user)


# delete a ticket
@bugs_board.route('/delete/<id>', methods=['GET', 'POST', 'DELETE'])
@cross_origin(headers=["Content Type", "Authorization"])
@requires_auth
def delete_ticket(id):
    id = request.form.get('id')
    ticket = Ticket.query.filter_by(id=id).first()

    # delete ticket
    db.session.delete(ticket)
    db.session.commit()

    return redirect(url_for('bugs_board.bugs_main'))
