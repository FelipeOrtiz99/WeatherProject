from flask import Blueprint


#Creamos los blueprint 
auth_bp = Blueprint('auth', __name__)
station_bp = Blueprint('station', __name__)

from . import auth
from . import station