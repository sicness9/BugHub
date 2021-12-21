# database models
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import DateTime, TIMESTAMP, event

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
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'))

    team = db.relationship("Team", foreign_keys=[team_id], backref="users")
    ticket = db.relationship("Ticket", foreign_keys=[ticket_id], backref='users')

    def __repr__(self):
        return f"{self.username} - {self.first_name} - {self.last_name} - {self.email}"


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
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    owner = relationship("User", foreign_keys=[owner_id])

    def __repr__(self):
        return f"{self.status} - {self.bucket} - {self.title} - {self.ticket_description} - {self.owner_id}"


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
        return f"{self.team_name} - {self.user_id}"


'''
team models
'''


class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True, index=True)
    role_name = db.Column(db.String, index=True)

    def __repr__(self):
        return f"{self.role_name} - {self.user_id}"



