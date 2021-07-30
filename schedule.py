USERNAME = 'sa'
PASSWORD = 'passworD0'
SERVER = 'localhost'
DATABASE = 'oktell_settings'
DRIVER = 'ODBC+DRIVER+17+for+SQL+Server'

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy


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

@app.route("/")
def homepage():
    return '<h1>Hi</h1>'

@app.route("/schedule/<user_id>", methods=['GET'])
def user_page(user_id):
    user = db.session.query(oktell_users).filter_by(ID=user_id).first()
    user_name = user.Name
    print(user_name)
    return "<p>Works</p>"
