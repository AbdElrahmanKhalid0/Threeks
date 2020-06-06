from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = '4bcde902803e55ae1211f9ba7f3ab7c1'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Threeks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

from Threeks import routes
