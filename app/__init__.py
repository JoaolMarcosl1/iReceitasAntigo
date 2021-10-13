from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://joaomarcos123:OHMAIGODIUAU123l@joaomarcos123.mysql.pythonanywhere-services.com/joaomarcos123$joaoireceitas"
app.config['SECRET_KEY'] = '123456'

login_manager = LoginManager(app)
db = SQLAlchemy(app)