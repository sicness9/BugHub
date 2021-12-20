# database models
import datetime

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
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    created_at = db.Column(TIMESTAMP(timezone=True), server_default=func.now())

    team = db.relationship("Team", foreign_keys=[team_id], backref="users")
    # ticket = db.relationship("Ticket", foreign_keys=[tickets], backref="users")

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
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    time_created = db.Column(DateTime(timezone=True), server_default=func.now())
    time_updated = db.Column(DateTime(timezone=True), onupdate=func.now())

    # owner_id = relationship("User", backref="tickets")

    def __repr__(self):
        return f"{self.status} - {self.bucket} - {self.title} - {self.ticket_description} - {self.owner_id}"


'''
team models
'''


class Team(db.Model):
    __tablename__ = "teams"

    id = db.Column(db.Integer, primary_key=True, index=True)
    team_name = db.Column(db.String, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # user_id = relationship("User", backref="teams")

    def __repr__(self):
        return f"{self.team_name} - {self.user_id}"
