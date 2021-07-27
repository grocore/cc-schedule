USERNAME = 'sa'
PASSWORD = 'passworD0'
SERVER = 'localhost'
DATABASE = 'oktell_settings'
DRIVER = 'ODBC+DRIVER+17+for+SQL+Server'

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy

app = Flask(__name__)

engine_stmt = (
    'mssql+pyodbc://{}:{}@{}/{}?driver={}'.format(
        USERNAME, PASSWORD, SERVER, DATABASE, DRIVER
        )
    )


app.config['SQLALCHEMY_DATABASE_URI'] = engine_stmt
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

oktell_users = db.Table('A_Users', db.metadata, autoload=True, autoload_with=db.engine)

@app.route("/schedule/<user_id>", methods=['GET'])
def user_page(user_id):
    user = db.session.query(oktell_users).filter_by(ID=user_id).first()
    print(user.ID)
    return "<p>Works</p>"