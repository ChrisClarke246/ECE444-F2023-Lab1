# from datetime import datetime
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError

app = Flask(__name__)

bootstrap = Bootstrap(app)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/')
# def user():
#     day = datetime.today().strftime('%A') 
#     month = datetime.now().strftime('%B')
#     date = datetime.now().day
#     year = datetime.now().year
#     time = datetime.now().strftime('%I:%M %p')
#     timestamp = f"{day}, {month} {date}, {year} {time}"

#     return render_template('user.html', name='Christian', timestamp=timestamp)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'unique'

bootstrap = Bootstrap(app)
moment = Moment(app)

def validate_email(form, field):
    if '@' not in field.data:
        message = f'Please include an \'@\' in the email. \'{field.data}\' is missing an \'@\'.'
        raise ValidationError(message)
class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = StringField('What is your UofT Email address?', validators=[DataRequired(), validate_email])
    submit = SubmitField('Submit')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()

    if form.validate_on_submit():
        old_name = session.get('name')
        old_email = session.get('email')

        # deal with changes
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        if old_email is not None and old_email != form.email.data:
            flash('Looks like you have changed your email!')

        # set session variables
        session['name'] = form.name.data
        session['email'] = form.email.data

        # handle non uoft email adress
        if 'utoronto' not in session.get('email'):
            session['email'] = None
            session['non_uoft'] = True
        else:
            session['non_uoft'] = False
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), email=session.get('email'), non_uoft=session.get('non_uoft'))