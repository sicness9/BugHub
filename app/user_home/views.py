# user home views
import json

from flask import render_template, request, url_for, session
from flask_cors import cross_origin

from app.utils import requires_auth
from app import db
from app.database.models import User
from . import user_home


# user home page
@user_home.route("/user_home", methods=['GET', 'POST'])
@cross_origin(headers=["Content Type", "Authorization"])
@requires_auth
def user_home_page():
    return render_template('user_home.html', userinfo=session['profile'])


# work in progress
@user_home.route("/profile", methods=["GET", "POST"])
@cross_origin(headers=["Content Type", "Authorization"])
@requires_auth
def user_profile():
    user = session['profile']
    current_user = User.query.filter_by(email=user.name)
    for info in current_user:
        if User.username or User.first_name or User.last_name is None:
            render_template('user_profile_add_form.html', userinfo=session['profile'])

    return render_template("user_profile.html", userinfo=session['profile'])


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
