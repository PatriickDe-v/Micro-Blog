import logging
from logging.handlers import SMTPHandler

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login' #uam função ou (endpoit) para exibição de login
from app import errors, models, routes

#set FLASK_APP=microblog.py

if not app.debug: 
    if app.config['MAIL_SERVER']: 
        auth = None 
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']: 
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None 
        if app.config['MAIL_USE_TLS']: 
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.loger.addHandler(mail_handler)

    