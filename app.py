import traceback
from flask import render_template, request, redirect, url_for
import logging.config
from flask import Flask
from Create_RDS_DB import Predictions, Reports
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

app = Flask(__name__)
app.config.from_pyfile('config_flask.py')
logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger("baseball")
logger.debug('Test log')
db = SQLAlchemy(app)
today = datetime.today() - timedelta(days=1)
today = today.strftime('%Y-%m-%d')


@app.route('/')
def index():

    try:
        dates_avail = db.session.query(Predictions.date).distinct().order_by("date").all()
        predictions = db.session.query(Predictions).filter(Predictions.date == today).all()
        logger.debug("Index page accessed.")
        return render_template('index.html', predictions=predictions, dates_avail=dates_avail)
    except:
        traceback.print_exc()
        logger.warning("Error page accessed.")
        return render_template('error.html')


@app.route('/results', methods=['POST'])
def get_date():

    try:
        dates_avail = db.session.query(Predictions.date).distinct().order_by("date").all()
        date1 = request.form['dates2']
        logger.debug(date1)
        predictions = db.session.query(Predictions).filter(Predictions.date == date1).all()
        return redirect('index.html', predictions=predictions, dates_avail=dates_avail)
    except:
        return render_template('error.html')


app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])



