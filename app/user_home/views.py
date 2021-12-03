# user home views
import json

from flask import render_template, request, url_for, session
from flask_cors import cross_origin

from app.utils import requires_auth
from app import db
from . import user_home


# user home page
@user_home.route("/", methods=['GET'])
@cross_origin(headers=["Content Type", "Authorization"])
@requires_auth
def user_home_page():
    return render_template('user_home.html', userinfo=session['profile'],
                           userinfo_pretty=json.dumps(session['jwt_payload'], indent=4))


# start add username process with this form
@user_home.route("/add_username/form", methods=['GET', 'POST'])
@requires_auth
def add_username_form():
    if request.method == 'POST':
        return render_template(url_for('user_home.username_add'))
    return render_template("add_username_form.html")


# add username to db function
@user_home.route("/add_username", methods=['GET', 'POST'])
@requires_auth
def add_username():
    username = request.form.get('username')
    db.session.add(username)
    db.session.commit()
    return render_template(url_for('user_home.user_home'))


# update username


# delete or unlink account


# join a team
