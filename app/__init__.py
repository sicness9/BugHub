import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
BH_DB_USER = os.getenv('BH_DB_USER')
BH_DB_PASSWORD = os.getenv('BH_DB_PASSWORD')
BH_DB_HOST = os.getenv('BH_DB_HOST')
BH_DB = os.getenv('BH_DB')

DB_URL = f'postgresql://{BH_DB_USER}:{BH_DB_PASSWORD}@{BH_DB_HOST}/{BH_DB}'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hbxirqsh:PDWwLidXZb8oo5xfDbvY5_FzHlo0OhdA@castor.db' \
                                            '.elephantsql.com/hbxirqsh'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .auth import auth
    from .main_page import main_page
    from .dashboard import dashboard
    from .user_home import user_home
    from .teams import teams
    from .bugs_board import bugs_board

    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(main_page, url_prefix='/')
    app.register_blueprint(dashboard, url_prefix='/dashboard')
    app.register_blueprint(user_home, url_prefix='/users')
    app.register_blueprint(teams, url_prefix='/teams')
    app.register_blueprint(bugs_board, url_prefix='/bugs')

    from app.database.models import User, Ticket, Team

    create_database(app)

    return app


def create_database(app):
    db.create_all(app=app)
