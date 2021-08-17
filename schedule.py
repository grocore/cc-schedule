USERNAME = 'sa'
PASSWORD = 'passworD0'
SERVER = 'localhost'
DATABASE = 'oktell_settings'
DRIVER = 'ODBC+DRIVER+17+for+SQL+Server'

import re
from flask import Flask, render_template, redirect, request, session
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from random import randint


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
    return '<h1>Hi</h1>'


@app.route("/list/<user_id>", methods=['GET', 'POST'])
def list(user_id):
    print(request.method)
    if user_id == 'test':
        user_id = '15a05eb8-2cd9-4af6-bd93-6960bf50e5ae'
    session['operator'] = user_id
    if request.method == 'POST':
        if request.form['action'] == 'Отменить':
            print('1')
            record_id = request.form.get('record_id')
            record = Schedule.query.get(record_id)
            record.status = 3
            print(request.form.get('action'))
            print(request.form.get('record_id'))
            print(type(record_id))
            db.session.commit()
        elif request.form['action'] == 'Добавить':
            print('2')
            start = datetime.strptime(' '.join([request.form.get('Date'), request.form.get('Start')]), '%Y-%m-%d %H:%M')
            end = datetime.strptime(' '.join([request.form.get('Date'), request.form.get('End')]), '%Y-%m-%d %H:%M')
            record = Schedule(user_id=user_id, start=start, end=end, status=1)
            db.session.add(record)
            db.session.commit()
            #end = datetime.strptime(request.form.get('End'), '%H:%M')
            #print(type(start))
            #shift_start = datetime.combine(date, start)
            #print(shift_start)
            #print(start, end, date)
            print(start)
    user = db.session.query(oktell_users).filter_by(ID=user_id).first()
    records = Schedule.query.order_by(Schedule.start.desc()).all()
    return render_template('schedule2.html', records=records, user_name=user.Name, operator=session['operator'])

@app.route("/add/", methods=['POST'])
def add():
    print(session['operator'])
    print(request.method)
    user_id = session['operator']
    if request.method == 'POST':
        if request.form['action'] == 'Отменить':
            print('1')
            record_id = request.form.get('record_id')
            record = Schedule.query.get(record_id)
            record.status = 3
            print(request.form.get('action'))
            print(request.form.get('record_id'))
            print(type(record_id))
            db.session.commit()
        elif request.form['action'] == 'Добавить':
            print('2')
            start = datetime.strptime(' '.join([request.form.get('Date'), request.form.get('Start')]), '%Y-%m-%d %H:%M')
            end = datetime.strptime(' '.join([request.form.get('Date'), request.form.get('End')]), '%Y-%m-%d %H:%M')
            record = Schedule(user_id=user_id, start=start, end=end, status=1)
            db.session.add(record)
            db.session.commit()
            #end = datetime.strptime(request.form.get('End'), '%H:%M')
            #print(type(start))
            #shift_start = datetime.combine(date, start)
            #print(shift_start)
            #print(start, end, date)
            print(start)
    return redirect(url_for('list', user_id=user_id))


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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
