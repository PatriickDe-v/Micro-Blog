from flask import Flask

#set FLASK_APP=microblog.py
app = Flask(__name__)

from app import routes
