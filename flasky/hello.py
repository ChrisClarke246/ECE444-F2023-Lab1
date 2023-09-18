from datetime import datetime
from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)

bootstrap = Bootstrap(app)

# @app.route('/')
# def index():
#     return render_template('index.html')

@app.route('/')
def user():
    day = datetime.today().strftime('%A') 
    month = datetime.now().strftime('%B')
    date = datetime.now().day
    year = datetime.now().year
    time = datetime.now().strftime('%I:%M %p')
    timestamp = f"{day}, {month} {date}, {year} {time}"

    return render_template('user.html', name='Christian', timestamp=timestamp)