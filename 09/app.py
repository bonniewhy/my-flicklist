from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True # Displays runtime errors in the browser, too.
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flicklist:mynewpass@localhost:8889/flicklist'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)