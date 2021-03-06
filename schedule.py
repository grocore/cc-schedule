from sqlalchemy.engine import create_engine
from sqlalchemy.sql.schema import MetaData, Table
from flask import Flask, render_template, redirect, request, session
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, timedelta
import settings


app = Flask(__name__)
app.config.from_object(settings.ProductionConfig())

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], convert_unicode=True)
metadata = MetaData(bind=engine)

db = SQLAlchemy(app)

oktell_users = Table(app.config['SOURCE_TABLE'], metadata, autoload=True, autoload_with=engine)

class Schedule(db.Model):
    __tablename__ = 'A_Schedule'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), nullable=False)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Integer)


@app.route("/")
def homepage():
    return redirect(url_for('schedule', user_id='15a05eb8-2cd9-4af6-bd93-6960bf50e5ae'))


@app.route("/schedule/<user_id>", methods=['GET'])
def schedule(user_id):
    session['operator'] = user_id
    today = date.today().strftime('%Y-%m-%d')
    #user = db.session.query(oktell_users).filter_by(ID=user_id).first()
    records = Schedule.query.filter_by(user_id=user_id).order_by(Schedule.start.desc()).all() # .order_by(Schedule.start.desc())
    return render_template('schedule_operator.html', records=records, today=today)


@app.route("/add/", methods=['POST'])
def add():
    user_id = session['operator']
    if request.form.get('Date') and request.form.get('Start') and request.form.get('End') and (request.form.get('Start') < request.form.get('End')):
        start = datetime.strptime(' '.join([request.form.get('Date'), request.form.get('Start')]), '%Y-%m-%d %H:%M')
        end = datetime.strptime(' '.join([request.form.get('Date'), request.form.get('End')]), '%Y-%m-%d %H:%M')
        record = Schedule(user_id=user_id, start=start, end=end, status=1)
        db.session.add(record)
        db.session.commit()
    return redirect(url_for('schedule', user_id=user_id))


@app.route("/cancel/", methods=['POST'])
def cancel():
    user_id = session['operator']
    record_id = request.form.get('record_id')
    record = Schedule.query.get(record_id)
    record.status = 3
    db.session.commit()
    return redirect(url_for('schedule', user_id=user_id))

@app.route("/sv_cancel/", methods=['POST'])
def sv_cancel():
    user_id = session['operator']
    record_id = request.form.get('record_id')
    record = Schedule.query.get(record_id)
    record.status = 4
    db.session.commit()
    return redirect(url_for('admin', user_id=user_id))

@app.route("/sv_aprove/", methods=['POST'])
def sv_aprove():
    user_id = session['operator']
    record_id = request.form.get('record_id')
    record = Schedule.query.get(record_id)
    record.status = 2
    db.session.commit()
    return redirect(url_for('admin', user_id=user_id))

@app.route("/admin/<user_id>", methods=['GET', 'POST'])
def admin(user_id):
    if not session.get('sv_id'):
        session['sv_id'] = user_id
    allusers = db.session.query(oktell_users).all()
    if request.method == 'POST' and request.form.get('operator'):
        name = request.form.get('operator')
        user = db.session.query(oktell_users).filter_by(Name=name).first()
        session['operator'] = user.ID
        return redirect(url_for('admin', user_id=user.ID))
    records = Schedule.query.filter_by(user_id=user_id).order_by(Schedule.start.desc()).all()

    print(user_id)
    return render_template('test.html', users=allusers, records=records)
    

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
