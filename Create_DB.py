from numpy import genfromtxt
from time import time
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import boto3
import pandas as pd

Base = declarative_base()


#app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///joe.db'
#db = SQLAlchemy(app)


class Predictions(Base):
    __tablename__='Predictions'
    __table_args__={'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True)
    game = Column(Integer)
    away = Column(String(3))
    home = Column(String(3))
    month = Column(Integer)
    day = Column(Integer)
    predicted_runs = Column(Float)
    bookie = Column(Float)
    predicted_run_rank = Column(Float)
    predicted_bookie_rank = Column(Float)
    bet = Column(String(5))
    betting_opportunity = Column(Float)

    def __repr__(self):
        return f"Predictions('{self.away}', '{self.home}', '{self.predicted_runs}', '{self.bet}', '{self.month}', '{self.day}')"


class Results(Base):
    __tablename__='Results'
    __table_args__={'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True)
    game = Column(Integer)
    away = Column(String(3))
    home = Column(String(3))
    month = Column(Integer)
    day = Column(Integer)
    predicted_runs = Column(Float)
    bookie = Column(Float)
    predicted_run_rank = Column(Float)
    predicted_bookie_rank = Column(Float)
    bet = Column(String(5))
    betting_opportunity = Column(Float)
    outcome = Column(Float)
    game_result = Column(String(5))
    bet_result = Column(Integer)

    def __repr__(self):
        return f"(Results('{self.away}', '{self.home}', '{self.predicted_runs}', '{self.bet}', '{self.month}', '{self.day}', '{self.bet_result}')"


class Reports(Base):
    __tablename__="Reports"
    __table_args__={'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True)
    game = Column(Integer)
    away = Column(String(10))
    bet_result = Column(Integer)
    betting_opportunity = Column(Float)
    bookie = Column(Float)
    game_result = Column(String(10))
    home = Column(String(10))
    outcome = Column(Float)
    predicted_runs = Column(Float)
    bet = Column(String(10))
    date = Column(String(20))

    def __repr__(self):
        return f"(Reports('{self.away}', '{self.home}', '{self.date}')"


if __name__ == "__main__":
    # s3 = boto3.resource("s3")
    # s3.meta.client.download_file('kupebaseball', 'data/daily_results/results.csv', 'results.csv')

    t = time()

    engine = create_engine('sqlite:///joe_test.db')
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    session = sessionmaker()
    session.configure(bind=engine)
    s = session()

    try:
        results_df = pd.read_csv('results.csv', skiprows=1)
        results_df.columns = ['game', 'away', 'bet_result', 'betting_opportunity', 'bookie', 'game_result', 'home',
                              'outcome', 'predicted_runs', 'bet', 'date']

        s.bulk_insert_mappings(Reports, results_df.to_dict(orient="records"))
        s.commit()

    except:
        s.rollback()
        print("exception occurred!")

    finally:
        s.close()

    print("Time elapsed: " + str(time() - t) + " seconds.")
