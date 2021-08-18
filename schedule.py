USERNAME = 'sa'
PASSWORD = 'passworD0'
SERVER = 'localhost'
DATABASE = 'oktell_settings'
DRIVER = 'ODBC+DRIVER+17+for+SQL+Server'

from flask import Flask, render_template, redirect, request, session
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, timedelta



database_uri = (
    'mssql+pyodbc://{}:{}@{}/{}?driver={}'.format(
        USERNAME, PASSWORD, SERVER, DATABASE, DRIVER
        )
    )

app = Flask(__name__)

app.config['SECRET_KEY'] = "zP0B8YTzRy9vcGMqVEKFFMqoT4kzn7IU"
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


@app.route("/")
def homepage():
    return redirect(url_for('list', user_id='15a05eb8-2cd9-4af6-bd93-6960bf50e5ae'))


@app.route("/list/<user_id>", methods=['GET'])
def list(user_id):
    session['operator'] = user_id
    today = date.today().strftime('%Y-%m-%d')
    #user = db.session.query(oktell_users).filter_by(ID=user_id).first()
    records = Schedule.query.order_by(Schedule.start.desc()).all()
    return render_template('schedule2.html', records=records, today=today)


@app.route("/add/", methods=['POST'])
def add():
    user_id = session['operator']
    if request.form.get('Date') and request.form.get('Start') and request.form.get('End'):
        start = datetime.strptime(' '.join([request.form.get('Date'), request.form.get('Start')]), '%Y-%m-%d %H:%M')
        end = datetime.strptime(' '.join([request.form.get('Date'), request.form.get('End')]), '%Y-%m-%d %H:%M')
        record = Schedule(user_id=user_id, start=start, end=end, status=1)
        db.session.add(record)
        db.session.commit()
    return redirect(url_for('list', user_id=user_id))


@app.route("/cancel/", methods=['POST'])
def cancel():
    user_id = session['operator']
    record_id = request.form.get('record_id')
    record = Schedule.query.get(record_id)
    record.status = 3
    db.session.commit()
    return redirect(url_for('list', user_id=user_id))

@app.route("/generate", methods=['GET'])
def generate():
    user_id = '15a05eb8-2cd9-4af6-bd93-6960bf50e5ae'
    user = db.session.query(oktell_users).filter_by(ID=user_id).first()
    user_name = user.Name
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    test_time = (datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M")
    record = Schedule(user_id=user_id, start=current_time, end=test_time, status=1)
    db.session.add(record)
    db.session.commit()
    return "<p>OK</p>"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
