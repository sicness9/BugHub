# dashboard views

import json

from flask import render_template, session

from app.utils import requires_auth
from . import dashboard


# dashboard
@dashboard.route('/dashboard')
@requires_auth
def dashboard():
    return render_template('dashboard.html', userinfo=session['profile'],
                           userinfo_pretty=json.dumps(session['jwt_payload'], indent=4))
