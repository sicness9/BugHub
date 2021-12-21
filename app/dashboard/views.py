# dashboard views

from flask import render_template, session
from flask_cors import cross_origin

from app.utils import requires_auth
from app.database.models import User, Ticket
from . import dashboard


# dashboard
@dashboard.route('/')
@cross_origin(headers=["Content Type", "Authorization"])
@requires_auth
def dashboard():
    current_user = session['profile']

    user = User.query.filter_by(email=current_user['name']).first()

    if user.team_id is None:
        return render_template('dashboard/dashboard_no_team_available.html', userinfo=current_user, user=user)

    # grab the total number of tickets in each category
    in_progress_tickets = len(Ticket.query.filter_by(status='In Progress').all())
    pending_triage_tickets = len(Ticket.query.filter_by(status='Pending Triage').all())
    closed_tickets = len(Ticket.query.filter_by(status='Closed').all())
    todo_tickets = len(Ticket.query.filter_by(status='To Do').all())

    # get the total number of tickets that are not closed
    open_tickets = (in_progress_tickets + pending_triage_tickets + todo_tickets)

    # Statistics for Dev role
    dev_team = User.query.filter_by(team_id=1).all()
    num_of_devs = len(dev_team)

    dev_tickets = 0
    for devs in dev_team:
        dev_tickets = dev_tickets + devs.tickets

    # Statistics for QA role
    qa_team = User.query.filter_by(team_id=2).all()
    num_of_qa = len(qa_team)

    qa_tickets = 0
    for member in qa_team:
        qa_tickets = qa_tickets + member.tickets

    # Statistics for Support role
    support_team = User.query.filter_by(team_id=3).all()
    num_of_support = len(support_team)

    support_tickets = 0
    for member in support_team:
        support_tickets = support_tickets + member.tickets

    # Statistics for engineers role
    engineer_team = User.query.filter_by(team_id=4).all()
    num_of_engineer = len(engineer_team)

    eng_tickets = 0
    for member in engineer_team:
        eng_tickets = eng_tickets + member.tickets

    return render_template('dashboard/dashboard_main.html', userinfo=current_user, open_tickets=open_tickets,
                           closed_tickets=closed_tickets, dev_team=dev_team, qa_team=qa_team, support_team=support_team,
                           engineer_team=engineer_team, num_of_devs=num_of_devs, dev_tickets=dev_tickets,
                           num_of_qa=num_of_qa, qa_tickets=qa_tickets, num_of_engineer=num_of_engineer,
                           eng_tickets=eng_tickets, num_of_support=num_of_support, support_tickets=support_tickets)
