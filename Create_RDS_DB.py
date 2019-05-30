from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import boto3
import pandas as pd
import os
import config

Base = declarative_base()


class Predictions(Base):
    """This table houses daily predictions of 2019 MLB game runs.  It lives on RDS"""
    __tablename__='Predictions'
    __table_args__={'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True)
    game = Column(Integer)
    nonsense = Column(Integer)
    away = Column(String(3))
    betting_opportunity = Column(Float)
    bookie = Column(Float)
    day = Column(Integer)
    home = Column(String(3))
    month = Column(Integer)
    predicted_bookie_rank = Column(Float)
    predicted_run_rank = Column(Float)
    predicted_runs = Column(Float)
    bet = Column(String(5))
    year = Column(Integer)
    date = Column(Date)

    def __repr__(self):
        return f"Predictions('{self.away}', '{self.home}', '{self.predicted_runs}', '{self.bet}', '{self.month}', '{self.day}')"


class Reports(Base):
    """This table houses daily gambling results of 2019 MLB games.  It lives on RDS"""
    __tablename__="Reports"
    __table_args__={'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True)
    game = Column(Integer)
    away = Column(String(10))
    bet_result = Column(Integer)
    betting_opportunity = Column(Float)
    bookie = Column(Float)
    day = Column(Integer)
    game_result = Column(String(10))
    home = Column(String(10))
    month = Column(Integer)
    outcome = Column(Float)
    predicted_bookie_rank = Column(Float)
    predicted_run_rank = Column(Float)
    predicted_runs = Column(Float)
    bet = Column(String(10))
    year = Column(Integer)
    date = Column(Date)

    def __repr__(self):
        return f"(Reports('{self.away}', '{self.home}', '{self.date}')"


def create_RDS(conn_type, user, password, host, port, DATABASE_NAME, s3_results_file, local_results_file, s3_predictions_file, local_predictions_file):
    """Creates the RDS MySQL DB from scratch when run.  OK to run daily, will wipe and repopulate in 0.5 seconds."""
    s3 = boto3.resource("s3")
    s3.meta.client.download_file(config.my_bucket, s3_results_file, local_results_file)
    s3.meta.client.download_file(config.my_bucket, s3_predictions_file, local_predictions_file)
    engine_string = "{}://{}:{}@{}:{}/{}".format(conn_type, user, password, host, port, DATABASE_NAME)
    engine = create_engine(engine_string)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    session = sessionmaker()
    session.configure(bind=engine)
    s = session()

    try:
        results_df = pd.read_csv('results.csv', skiprows=1)
        results_df.columns = ['game', 'away', 'bet_result', 'betting_opportunity', 'bookie', 'day', 'game_result',
                              'home', 'month', 'outcome', 'predicted_bookie_rank', 'predicted_run_rank',
                              'predicted_runs', 'bet', 'year', 'date']
        s.bulk_insert_mappings(Reports, results_df.to_dict(orient="records"))
        s.commit()

        predictions_df = pd.read_csv('predictions.csv', skiprows=1)
        predictions_df.columns = ['game', 'nonsense', 'away', 'betting_opportunity', 'bookie', 'day', 'home', 'month',
                                  'predicted_bookie_rank', 'predicted_run_rank', 'predicted_runs', 'bet', 'year', 'date']
        s.bulk_insert_mappings(Predictions, predictions_df.to_dict(orient="records"))
        s.commit()

    except:
        s.rollback()
        print("exception occurred!")

    finally:
        s.close()
        if os.path.exists(local_results_file):
            os.remove(local_results_file)
        if os.path.exists(local_predictions_file):
            os.remove(local_predictions_file)


if __name__ == "__main__":
    s3_results_file = 'results.csv'
    local_results_file = 'results.csv'
    s3_predictions_file = 'predictions.csv'
    local_predictions_file = 'predictions.csv'
    create_RDS(config.conn_type,
               config.user,
               config.password,
               config.host,
               config.port,
               config.DATABASE_NAME,
               config.s3_results_file,
               config.local_results_file,
               config.s3_predictions_file,
               config.local_predictions_file)

