# database models

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import DateTime, TIMESTAMP

from .. import db

'''
user models
'''


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String, unique=True, nullable=True)
    first_name = db.Column(db.String, nullable=True)
    last_name = db.Column(db.String, nullable=True)
    email = db.Column(db.String, unique=True, index=True)
    tickets = db.Column(db.Integer, default=0)
    created_at = db.Column(TIMESTAMP(timezone=True), server_default=func.now())
    is_admin = db.Column(db.Boolean, default=False)
    invite_status = db.Column(db.Integer, default=0, nullable=True)

    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'))
    member_id = db.Column(db.Integer, db.ForeignKey('team_members.id'))

    team = db.relationship("Team", foreign_keys=[team_id], backref="users")
    ticket = db.relationship("Ticket", foreign_keys=[ticket_id], backref='users')
    role = db.relationship("Role", foreign_keys=[role_id])
    team_members = db.relationship("TeamMember", foreign_keys=[member_id], backref='users')

    def __repr__(self):
        return f"{self.username} - {self.first_name} {self.last_name} - {self.email}"


'''
ticket models
'''


class Ticket(db.Model):
    __tablename__ = "tickets"

    id = db.Column(db.Integer, primary_key=True, index=True)
    status = db.Column(db.String)
    bucket = db.Column(db.String)
    title = db.Column(db.String, index=True)
    ticket_description = db.Column(db.String, nullable=True)
    time_created = db.Column(DateTime(timezone=True), server_default=func.now())
    time_updated = db.Column(DateTime(timezone=True), onupdate=func.now())
    team_id = db.Column(db.Integer)

    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    owner = relationship("User", foreign_keys=[owner_id])

    def __repr__(self):
        return f"{self.id}- {self.status} - {self.bucket} - {self.title} - {self.ticket_description} - {self.owner_id}"


'''
team models
'''


class Team(db.Model):
    __tablename__ = "teams"

    id = db.Column(db.Integer, primary_key=True, index=True)
    team_name = db.Column(db.String, unique=True, index=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    admin = relationship("User", foreign_keys=[admin_id])

    def __repr__(self):
        return f"{self.team_name}"


'''
team member models
'''


class TeamMember(db.Model):
    __tablename__ = "team_members"

    id = db.Column(db.Integer, primary_key=True, index=True)
    admin_id = db.Column(db.Integer)

    team_name = db.Column(db.String, db.ForeignKey('teams.team_name'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    member = relationship("User", foreign_keys=[user_id])
    team = relationship("Team", foreign_keys=[team_name])

    '''member = relationship("User", foreign_keys=[user_id],
                          primaryjoin="and_(User.id == TeamMember.user_id,"
                                      "User.is_admin == 'False')")'''

    def __repr__(self):
        return f"{self.id} - {self.team_name} - {self.role_id}"


'''
role models
'''


class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True, index=True)
    role_name = db.Column(db.String, index=True, unique=True)

    def __repr__(self):
        return f"{self.role_name}"
