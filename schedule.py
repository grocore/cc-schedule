USERNAME = 'sa'
PASSWORD = 'passworD0'
SERVER = 'localhost'
DATABASE = 'oktell_settings'
DRIVER = 'ODBC+DRIVER+17+for+SQL+Server'

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from datetime import date, datetime


database_uri = (
    'mssql+pyodbc://{}:{}@{}/{}?driver={}'.format(
        USERNAME, PASSWORD, SERVER, DATABASE, DRIVER
        )
    )

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

oktell_users = db.Table('A_Users', db.metadata, autoload=True, autoload_with=db.engine)

class Schedule(db.Model):
    __tablename__ = 'A_Schedule'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), nullable=False)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Integer)

    def __repr__(self):
        return '<User %r>' % self.user_id

@app.route("/")
def homepage():
    return '<h1>Hi</h1>'

@app.route("/schedule/<user_id>", methods=['GET'])
def user_page(user_id):
    user = db.session.query(oktell_users).filter_by(ID=user_id).first()
    user_name = user.Name
    print(type(user_id))
    current_time = datetime.now()
    return "<p>Works</p>"
