import os

from dotenv import load_dotenv

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

db = SQLAlchemy()
DB_USER = os.getenv('BH_DB_USER')
DB_PASSWORD = os.getenv('BH_DB_PASSWORD')
DB_HOST = os.getenv('BH_DB_HOST')
DB = os.getenv('BH_DB')

DB_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB}'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from flask_migrate import Migrate
    migrate = Migrate(app, db)

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

    from app.database.models import User, Ticket, Team, Role, TeamMember

    create_database(app)

    return app


def create_database(app):
    db.create_all(app=app)
