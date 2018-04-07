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

dummy = "mongodb://heroku_jrmxs801:d8soja6ng9gdlfskchmi51b554@ds237979.mlab.com:37979/heroku_jrmxs801"
MONGODB_URI = os.getenv('MONGODB_URI') or dummy
app.config['MONGODB_SETTINGS'] = {
    'db': 'users',
    'host': MONGODB_URI
}

db = MongoEngine(app)

from app.models import User
admin = Admin(app, 'TigerMenu Alerts')
admin.add_view(ModelView(User))

from app import routes
