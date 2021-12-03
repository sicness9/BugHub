# main page blueprint

from flask import Blueprint

main_page = Blueprint('main_page',
                      __name__,
                      template_folder='templates',
                      static_folder='static'
                      )

from . import views
