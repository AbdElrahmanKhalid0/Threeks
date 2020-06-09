from flask import Blueprint
errors = Blueprint('errors',__name__)

from Threeks.errors import handlers