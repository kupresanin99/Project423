import traceback
from flask import render_template, request, redirect, url_for
import logging.config
from flask import Flask
# from src.add_songs import Tracks
from Create_RDS_DB import Predictions, Reports
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask application
app = Flask(__name__)

# Configure flask app from flask_config.py
app.config.from_pyfile('config_flask.py')

# Define LOGGING_CONFIG in flask_config.py - path to config file for setting
# up the logger (e.g. config/logging/local.conf)
logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger("baseball")
logger.debug('Test log')

# Initialize the database
db = SQLAlchemy(app)


@app.route('/')
def index():

    try:
        dates_avail = db.session.query(Predictions.date).distinct().order_by("date").all()
        predictions = db.session.query(Predictions).filter(Predictions.day == 30).filter(Predictions.month == 5).all()
        logger.debug("Index page accessed.")
        return render_template('index.html', predictions=predictions, dates_avail=dates_avail)
    except:
        traceback.print_exc()
        logger.warning("Error page accessed.")
        return render_template('error.html')





app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])



