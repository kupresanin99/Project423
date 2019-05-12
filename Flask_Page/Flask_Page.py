from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///joe.db'
db = SQLAlchemy(app)


class Predictions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game = db.Column(db.Integer)
    away = db.Column(db.String(3))
    home = db.Column(db.String(3))
    month = db.Column(db.Integer)
    day = db.Column(db.Integer)
    predicted_runs = db.Column(db.Float)
    bookie = db.Column(db.Float)
    predicted_run_rank = db.Column(db.Float)
    predicted_bookie_rank = db.Column(db.Float)
    bet = db.Column(db.String(5))
    betting_opportunity = db.Column(db.Float)

    def __repr__(self):
        return f"Predictions('{self.away}', '{self.home}', '{self.predicted_runs}', '{self.bet}', '{self.month}', '{self.day}')"


class Results(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game = db.Column(db.Integer)
    away = db.Column(db.String(3))
    home = db.Column(db.String(3))
    month = db.Column(db.Integer)
    day = db.Column(db.Integer)
    predicted_runs = db.Column(db.Float)
    bookie = db.Column(db.Float)
    predicted_run_rank = db.Column(db.Float)
    predicted_bookie_rank = db.Column(db.Float)
    bet = db.Column(db.String(5))
    betting_opportunity = db.Column(db.Float)
    outcome = db.Column(db.Float)
    game_result = db.Column(db.String(5))
    bet_result = db.Column(db.Integer)

    def __repr__(self):
        return f"(Results('{self.away}', '{self.home}', '{self.predicted_runs}', '{self.bet}', '{self.month}', '{self.day}', '{self.bet_result}')"


class Reports(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game = db.Column(db.Integer)
    away = db.Column(db.String(3))
    bet_result = db.Column(db.Integer)
    betting_opportunity = db.Column(db.Float)
    bookie = db.Column(db.Float)
    game_result = db.Column(db.String(5))
    home = db.Column(db.String(3))
    outcome = db.Column(db.Float)
    predicted_runs = db.Column(db.Float)
    bet = db.Column(db.String(5))
    date = db.Column(db.Date)

    def __repr__(self):
        return f"(Reports('{self.away}', '{self.home}', '{self.date}')"


