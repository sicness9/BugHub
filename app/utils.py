# utility functions

import os
import json
from functools import wraps
from six.moves.urllib_request import urlopen
from dotenv import load_dotenv

from flask import session, redirect, request, _request_ctx_stack
from jose import jwt
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from app.database.models import User, Team

load_dotenv()

AUTH0_DOMAIN = os.getenv('DOMAIN')
API_AUDIENCE = os.getenv('API_AUDIENCE')
ALGORITHMS = os.getenv('ALGORITHMS')
SENDGRID_SENDER_EMAIL = os.getenv('SENDGRID_SENDER_EMAIL')
TEMPLATE_ID = os.getenv('TEMPLATE_ID')


# wrapper to require auth for endpoints
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'profile' not in session:
            # redirect to login page
            return redirect('/')
        return f(*args, **kwargs)

    return decorated


# api wrapper
def api_requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()
        jsonurl = urlopen("https://" + AUTH0_DOMAIN + "/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
            if rsa_key:
                try:
                    payload = jwt.decode(
                        token,
                        rsa_key,
                        algorithms=ALGORITHMS,
                        audience=API_AUDIENCE,
                        issuer="https://" + AUTH0_DOMAIN + "/"
                    )

                except jwt.ExpiredSignatureError:
                    raise AuthError({"code": "token_expired",
                                     "description": "token is expired"}, 401)
                except jwt.JWTClaimsError:
                    raise AuthError({"code": "invalid_claims",
                                     "description":
                                         "incorrect claims,"
                                         "please check the audience and issuer"}, 401)
                except Exception:
                    raise AuthError({"code": "invalid_header",
                                     "description":
                                         "Unable to parse authentication"
                                         " token."}, 401)

                _request_ctx_stack.top.current_user = payload
                return f(*args, **kwargs)
            raise AuthError({"code": "invalid_header",
                             "description": "Unable to find appropriate key"}, 401)
        return decorated


# error handler
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# format error response and append status code
def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                         "description":
                             "Authorization header is expected"}, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header",
                         "description":
                             "Authorization header must start with"
                             " Bearer"}, 401)
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                         "description": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                         "description":
                             "Authorization header must be"
                             " Bearer token"}, 401)

    token = parts[1]
    return token


# check for auth0 scope to access certain endpoints
def requires_scope(required_scope):
    """Determines if the required scope is present in the Access Token
    Args:
        required_scope (str): The scope required to access the resource
    """
    token = get_token_auth_header()
    unverified_claims = jwt.get_unverified_claims(token)
    if unverified_claims.get("scope"):
        token_scopes = unverified_claims["scope"].split()
        for token_scope in token_scopes:
            if token_scope == required_scope:
                return True
    return False


# send invite emails
def send_email(invitee):
    message = Mail(
        from_email=SENDGRID_SENDER_EMAIL,
        to_emails=invitee,
        subject='Sending with Twilio SendGrid is Fun',
        html_content='<strong>and easy to do anywhere, even with Python</strong>')
    message.template_id = TEMPLATE_ID
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)
