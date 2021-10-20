from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextField
from wtforms.fields.html5 import DateField, TimeField, SearchField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from hashlib import md5
from datetime import datetime, date, timedelta
from settings import DevelopmentConfig

from datetime import datetime, timedelta

app = Flask(__name__)
app.config.from_object(DevelopmentConfig())
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_message = u"Для доступа к системе необходима авторизация."

class User(db.Model, UserMixin):
    __tablename__ = app.config['SOURCE_TABLE']
    id = db.Column('ID', db.String(40), primary_key=True)
    name = db.Column('Name', db.String(120))
    login = db.Column('Login', db.String(120))
    password = db.Column('Password', db.String(60))
    parentgroupid = db.Column('ParentGroupID', db.String(60))

    def __repr__(self):
        return f"User('{self.id}', '{self.name}', '{self.login}')"

class Shift(db.Model):
    __tablename__ = 'A_Shifts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), nullable=False)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Integer)

    def __repr__(self):
        return f"Shift('{self.user_id}', '{self.start}', '{self.end}')"

def generate_shift():
    user_id = current_user.id
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    test_time = (datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M")
    shift = Shift(user_id=user_id, start=current_time, end=test_time, status=1)
    db.session.add(shift)
    db.session.commit()

def check_pwd(hash, password):
    return md5(password.encode('utf-8')).hexdigest().upper() == hash.upper()

class LoginForm(FlaskForm):
    name = StringField('Имя пользователя',
                        validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class ShiftForm(FlaskForm):
    date = TextField('Дата', render_kw={'readonly': True})
    start_time = TextField('Время начала смены', render_kw={'readonly': True})
    end_time = TextField('Время окончания смены', render_kw={'readonly': True})
    submit = SubmitField('Добавить') 

    def validate_date(self, field):
        if field.data:
            try:
                datetime.strptime(field.data, "%d.%m.%Y")
            except:
                raise ValidationError('Дата не соответствует формату "ДД.ММ.ГГГГ"')
        else:
            raise ValidationError('Не выбрана дата')

    def validate_start_time(self, field):
        if not field.data:
            raise ValidationError('Не выбрано время начала смены')


    def validate_end_time(self, field):
        if field.data:
            if field.data <= self.start_time.data:
                raise ValidationError('Время начала смены должно предшествовать времени окончания')
        else:
            raise ValidationError('Не выбрано время окончания смены')

class SelectOperatorForm(FlaskForm):
    #department = SearchField('Отдел')
    language = SelectField(u'Programming Language', choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])
    submit = SubmitField('Найти')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(str(user_id))

@app.route("/")
@app.route("/home")
@login_required
def home():
    shifts = Shift.query.filter_by(user_id=current_user.id).order_by(Shift.start.desc()).all()
    return render_template('schedule.html', shifts=shifts)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.name.data).first()
        if user and check_pwd(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('С возвращением, {}'.format(user.name), 'info')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Неверное имя пользователя или пароль.', 'danger')
    return render_template('login.html', title='Вход', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/shift/new", methods=['GET', 'POST'])
@login_required
def new_shift():
    form = ShiftForm()
    if form.validate_on_submit():
        print(form.date.data, type(form.date.data))
        date_obj = datetime.strptime(form.date.data, "%d.%m.%Y")

        print(date_obj.date())

        start_obj = datetime.strptime(form.start_time.data, '%H:%M').time()
        end_obj = datetime.strptime(form.end_time.data, '%H:%M').time()
        start = datetime.combine(date_obj, start_obj)
        end = datetime.combine(date_obj, end_obj)

        
        shift = Shift(user_id=current_user.id, start=start, end=end, status=1)
        this_user_shifts = Shift.query.filter_by(user_id=current_user.id).all()
        for a_shift in this_user_shifts:
            print(a_shift.start)
        #print(this_user_shifts)

        db.session.add(shift)
        db.session.commit()
        flash('Ваша смена была успешно добавлена.', 'success')
        return redirect(url_for('home'))
    today = date.today().strftime('%Y-%m-%d')
    return render_template('create_shift.html', today=today, title='Добавление смены', form=form, legend='Добавление новой смены')

@app.route("/shift/<int:shift_id>/delete", methods=['POST'])
@login_required
def cancel_shift(shift_id):
    shift = Shift.query.get_or_404(shift_id)
    shift.status = 3
    db.session.commit()
    flash('Смена была отменена.', 'success')
    return redirect(url_for('home'))

@app.route("/sv", methods=['GET', 'POST'])
@login_required
def sv():
    form = SelectOperatorForm()
    if form.validate_on_submit():
        print(form.language.data)
        print(type(form.language.data))
    return render_template('schedule_sv.html', form=form)

@app.route("/generate", methods=['GET', 'POST'])
def generate():
    generate_shift()
    return 'OK'

if __name__ == '__main__':
    app.run(debug=True)
