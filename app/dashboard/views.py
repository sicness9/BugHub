# dashboard views

from flask import render_template, session, redirect, url_for
from flask_cors import cross_origin

from app.utils import requires_auth
from app.database.models import User, Ticket, Team
from . import dashboard


# dashboard
@dashboard.route('/', methods=['GET', 'POST'])
@cross_origin(headers=["Content Type", "Authorization"])
@requires_auth
def dashboard_main():
    current_user = session['profile']

    user = User.query.filter_by(email=current_user['name']).first()
    team = Team.query.filter_by(id=user.team_id).first()
    # print(user.team)

    if team is not None:
        all_tickets = Ticket.query.filter_by(team_id=team.id).all()  # for search bar
    else:
        all_tickets = Ticket.query.filter_by(owner_id=user.id).all()

    if user.team_id is None:
        return render_template('dashboard/dashboard_no_team_available.html', userinfo=current_user, user=user)
    if user.role_id != 5:
        return redirect(url_for('bugs_board.bugs_main'))

    # grab the total number of tickets in each category
    '''in_progress_tickets = len(Ticket.query.filter_by(status='In Progress', team_id=team.id).all())
    pending_triage_tickets = len(Ticket.query.filter_by(status='Pending Triage', team_id=team.id).all())
    closed_tickets = len(Ticket.query.filter_by(status='Closed', team_id=team.id).all())
    todo_tickets = len(Ticket.query.filter_by(status='To Do', team_id=team.id).all())'''

    # test
    all_tickets = Ticket.query.all()

    in_progress_tickets = []
    for ticket in all_tickets:
        if ticket.status == 'In Progress' and ticket.team_id == team.id:
            in_progress_tickets.append(ticket)

    pending_triage_tickets = []
    for ticket in all_tickets:
        if ticket.status == 'Pending Triage' and ticket.team_id == team.id:
            pending_triage_tickets.append(ticket)

    closed_tickets_list = []
    for ticket in all_tickets:
        if ticket.status == 'Closed' and ticket.team_id == team.id:
            closed_tickets_list.append(ticket)

    todo_tickets = []
    for ticket in all_tickets:
        if ticket.status == 'To Do' and ticket.team_id == team.id:
            todo_tickets.append(ticket)

    open_tickets = (len(in_progress_tickets) + len(pending_triage_tickets) + len(todo_tickets))
    closed_tickets = len(closed_tickets_list)

    # Statistics for Dev role
    dev_team = User.query.filter_by(role_id=1, team_id=team.id).all()
    num_of_devs = len(dev_team)

    dev_tickets = 0
    for devs in dev_team:
        dev_tickets = dev_tickets + devs.tickets

    # Statistics for QA role
    qa_team = User.query.filter_by(role_id=2, team_id=team.id).all()
    num_of_qa = len(qa_team)

    qa_tickets = 0
    for member in qa_team:
        qa_tickets = qa_tickets + member.tickets

    # Statistics for Support role
    support_team = User.query.filter_by(role_id=3, team_id=team.id).all()
    num_of_support = len(support_team)

    support_tickets = 0
    for member in support_team:
        support_tickets = support_tickets + member.tickets

    # Statistics for engineers role
    engineer_team = User.query.filter_by(role_id=4, team_id=team.id).all()
    num_of_engineer = len(engineer_team)

    eng_tickets = 0
    for member in engineer_team:
        eng_tickets = eng_tickets + member.tickets

    return render_template('dashboard/dashboard_main.html', userinfo=current_user, open_tickets=open_tickets,
                           closed_tickets=closed_tickets, dev_team=dev_team, qa_team=qa_team, support_team=support_team,
                           engineer_team=engineer_team, num_of_devs=num_of_devs, dev_tickets=dev_tickets,
                           num_of_qa=num_of_qa, qa_tickets=qa_tickets, num_of_engineer=num_of_engineer,
                           eng_tickets=eng_tickets, num_of_support=num_of_support, support_tickets=support_tickets,
                           user=user, team=team, all_tickets=all_tickets)


