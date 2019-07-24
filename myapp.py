from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask import Flask, render_template, request
import RPi.GPIO as GPIO

app = Flask(__name__)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

led1 = 13
led2= 19
buzzer= 26

led1Sts = 0
if led1Sts:
    print("Off")
else:
    print("On");
led2Sts = 0
buzzer1 = 0

GPIO.setup(led1, GPIO.OUT)
GPIO.setup(led2,GPIO.OUT)
GPIO.setup(buzzer, GPIO.OUT)

GPIO.output(led1, GPIO.LOW)
GPIO.output(led2, GPIO.LOW)
GPIO.output(buzzer, GPIO.LOW)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'Thisisgroup3secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/pi/Desktop/Pi-JED/database.db'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        return '<h1>Invalid username or password</h1>'
        return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return '<h1>New user has been created!</h1>'
        return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html', form=form)




@app.route('/dashboard')
@login_required
def dashboard():
        led1Sts = GPIO.input(led1)
        led2Sts = GPIO.input(led2)
        buzzer1 = GPIO.input(buzzer)
   
        templateData = { 'led1' : led1Sts,
        'led2' : led2Sts,
        'buzzer' : buzzer1 }
   
        return render_template('dashboard.html', **templateData)
        return render_template('dashboard.html', name=current_user.username)

@app.route('/<deviceName>/<action>')
def do(deviceName, action):
    if deviceName == "led1":
        actuator = led1
    if deviceName == "led2":
        actuator = led2
    if deviceName == "buzzer":
        actuator = buzzer

    if action == "on":
        GPIO.output(actuator, GPIO.HIGH)
    if action == "off":
        GPIO.output(actuator, GPIO.LOW)

    f_led = GPIO.input(led1)
    s_led = GPIO.input(led2)
    buzz = GPIO.input(buzzer)
   
    templateData = { 'led1' : f_led,
    'led2' : s_led, 'buzzer': buzz}

    return render_template('dashboard.html', **templateData )

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
