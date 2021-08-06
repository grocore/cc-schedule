USERNAME = 'sa'
PASSWORD = 'passworD0'
SERVER = 'localhost'
DATABASE = 'oktell_settings'
DRIVER = 'ODBC+DRIVER+17+for+SQL+Server'

from flask import Flask, render_template, redirect, request
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta


database_uri = (
    'mssql+pyodbc://{}:{}@{}/{}?driver={}'.format(
        USERNAME, PASSWORD, SERVER, DATABASE, DRIVER
        )
    )

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db.create_all()

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


@app.route("/list/<user_id>", methods=['GET', 'POST'])
def list(user_id):
    if request.method == 'POST':
        record_id = request.values['record_id']
        record = Schedule.query.get(record_id)
        record.status = 3
        print(request.date)
        print(request.get_data())
        db.session.commit()
    user = db.session.query(oktell_users).filter_by(ID=user_id).first()
    records = Schedule.query.all()
    return render_template('schedule2.html', records=records, user_name=user.Name)

@app.route("/deactivate/<record_id>")
def deactivate(record_id):
    
    return redirect(url_for('list'))

@app.route("/schedule/<user_id>", methods=['GET'])
def user_page(user_id):
    user = db.session.query(oktell_users).filter_by(ID=user_id).first()
    user_name = user.Name
    print(type(user_id))
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    test_time = (datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M")
    record = Schedule(user_id=user_id, start=current_time, end=test_time, status=1)
    '''
    Status:
    1 - newly added
    2 - deactivated
    '''
    db.session.add(record)
    db.session.commit()
    return "<p>Works</p>"
