from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://joaomarcos123:OHMAIGODIUAU123l@joaomarcos123.mysql.pythonanywhere-services.com/joaomarcos123$joaoireceitas"
app.config['SECRET_KEY'] = '123456'

login_manager = LoginManager(app)
db = SQLAlchemy(app)

app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME '] = "joaobastos716@gmail.com"
app.config['MAIL_PASSWORD'] = "123"
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
