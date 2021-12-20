# bug board blueprint

from flask import Blueprint

bugs_board = Blueprint('bugs_board',
                       __name__,
                       template_folder='templates',
                       static_folder='static'
                       )

from . import views
