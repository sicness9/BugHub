# teams blueprint

from flask import Blueprint

teams = Blueprint('teams',
                  __name__,
                  template_folder='templates',
                  static_folder='static'
                  )

from . import views
