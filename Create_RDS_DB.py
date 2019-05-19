from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import boto3
import pandas as pd
import os
import config

Base = declarative_base()


# class Predictions(Base):
#     __tablename__='Predictions'
#     __table_args__={'sqlite_autoincrement': True}
#     id = Column(Integer, primary_key=True)
#     game = Column(Integer)
#     away = Column(String(3))
#     home = Column(String(3))
#     month = Column(Integer)
#     day = Column(Integer)
#     predicted_runs = Column(Float)
#     bookie = Column(Float)
#     predicted_run_rank = Column(Float)
#     predicted_bookie_rank = Column(Float)
#     bet = Column(String(5))
#     betting_opportunity = Column(Float)
#
#     def __repr__(self):
#         return f"Predictions('{self.away}', '{self.home}', '{self.predicted_runs}', '{self.bet}', '{self.month}', '{self.day}')"
#
#
# class Results(Base):
#     __tablename__='Results'
#     __table_args__={'sqlite_autoincrement': True}
#     id = Column(Integer, primary_key=True)
#     game = Column(Integer)
#     away = Column(String(3))
#     home = Column(String(3))
#     month = Column(Integer)
#     day = Column(Integer)
#     predicted_runs = Column(Float)
#     bookie = Column(Float)
#     predicted_run_rank = Column(Float)
#     predicted_bookie_rank = Column(Float)
#     bet = Column(String(5))
#     betting_opportunity = Column(Float)
#     outcome = Column(Float)
#     game_result = Column(String(5))
#     bet_result = Column(Integer)
#
#     def __repr__(self):
#         return f"(Results('{self.away}', '{self.home}', '{self.predicted_runs}', '{self.bet}', '{self.month}', '{self.day}', '{self.bet_result}')"


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
    date = Column(Date)

    def __repr__(self):
        return f"(Reports('{self.away}', '{self.home}', '{self.date}')"


def create_RDS(conn_type):
    s3 = boto3.resource("s3")
    s3.meta.client.download_file(config.my_bucket, local_results, local_csv)
    #conn_type = "mysql+pymysql"
    user = os.environ.get("MYSQL_USER")
    password = os.environ.get("MYSQL_PASSWORD")
    host = os.environ.get("MYSQL_HOST")
    port = os.environ.get("MYSQL_PORT")
    DATABASE_NAME = 'msia423'
    engine_string = "{}://{}:{}@{}:{}/{}".format(conn_type, user, password, host, port, DATABASE_NAME)
    engine = create_engine(engine_string)
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
        if os.path.exists(local_csv):
            os.remove(local_csv)


if __name__ == "__main__":
    local_results = 'data/daily_results/results.csv'
    local_csv = 'results.csv'
    create_RDS(config.conn_type)

