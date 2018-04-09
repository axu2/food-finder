import os
from flask import Flask
from flask_cas import CAS
from flask_admin import Admin
from flask_bootstrap import Bootstrap
from flask_mongoengine import MongoEngine
from flask_admin.contrib.mongoengine import ModelView

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or 'you-will-never-guess'
app.config['CAS_SERVER'] = 'https://fed.princeton.edu/cas'
app.config['CAS_AFTER_LOGIN'] = '/'
cas = CAS(app)
bootstrap = Bootstrap(app)

dummy = "mongodb://heroku_cqcm2pgv:nd8cpu61p161k9ltshhpopu5oe@ds237989.mlab.com:37989/heroku_cqcm2pgv"
MONGODB_URI = os.getenv('MONGODB_URI') or dummy
app.config['MONGODB_SETTINGS'] = {
    'db': 'users',
    'host': MONGODB_URI
}

db = MongoEngine(app)

from app.models import User
admin = Admin(app, 'TigerMenu Alerts')
if not os.getenv('TZ'):
    admin.add_view(ModelView(User))
    #admin panel only on local dev

from app import routes
