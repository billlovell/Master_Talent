from flask import Blueprint

bp = Blueprint('Auth', __name__)

from app.Auth import routes