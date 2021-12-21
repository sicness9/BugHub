# auth views and functions
# primarily handled by auth0

import os
import datetime
from dotenv import load_dotenv

from flask import session, redirect, url_for, jsonify
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode

from main import app
from app import db
from . import auth
from ..utils import AuthError
from app.database.models import User

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
API_BASE_URL = os.getenv('API_BASE_URL')
ACCESS_TOKEN_URL = os.getenv('ACCESS_TOKEN_URL')
AUTHORIZE_URL = os.getenv('AUTHORIZE_URL')
API_AUDIENCE = os.getenv('API_AUDIENCE')


oauth = OAuth(app)


# initialize authlib
auth0 = oauth.register(
    'auth0',
    client_id=f'{CLIENT_ID}',
    client_secret=f'{CLIENT_SECRET}',
    api_base_url=f'{API_BASE_URL}',
    access_token_url=f'{ACCESS_TOKEN_URL}',
    authorize_url=f'{AUTHORIZE_URL}',
    client_kwargs={
        'scope': 'openid profile email',
    },
)


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


# handle callback
@auth.route('/callback', methods=['GET', 'POST'])
def callback_handling():
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    # store user info in flask session
    session['jwt_payload'] = userinfo
    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }

    # check if email exists in db
    user = User.query.filter_by(email=userinfo['name']).first()
    # if email does not exist, add to User table
    if user is None:
        new_user = User(email=userinfo['name'], created_at=datetime.datetime.now())
        db.session.add(new_user)
        db.session.commit()

    return redirect(url_for('user_home.init_profile'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    return auth0.authorize_redirect(redirect_uri=url_for('auth.callback_handling', _external=True),
                                    audience=f'{API_AUDIENCE}')


@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    # clear the session stored data
    session.clear()
    # redirect to logout endpoint
    params = {'returnTo': url_for('main_page.main_redirect', _external=True), 'client_id': f'{CLIENT_ID}'}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))
