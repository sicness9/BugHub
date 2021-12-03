# user home blueprint

from flask import Blueprint

user_home = Blueprint('user_home',
                      __name__,
                      template_folder='templates',
                      static_folder='static'
                      )

from . import views
