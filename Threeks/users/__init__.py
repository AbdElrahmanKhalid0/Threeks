from flask import Blueprint
users = Blueprint('users', __name__)

from Threeks.users import routes