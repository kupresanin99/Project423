import os

my_api_key = "92jge9phm7k8x746vdj39w83"
my_bucket = "kupebaseball"

DEST_BUCKET = "kupebaseball"
DEST_KEY_1 = "model_data"
DEST_KEY_2 = "predictions.csv"
DEST_KEY_3 = "results.csv"

local_db = 'sqlite:///sqlite.db'

conn_type = "mysql+pymysql"
user = os.environ.get("MYSQL_USER")
password = os.environ.get("MYSQL_PASSWORD")
host = os.environ.get("MYSQL_HOST")
port = os.environ.get("MYSQL_PORT")
DATABASE_NAME = 'msia423'

s3_results_file = 'results.csv'
local_results_file = 'results.csv'
s3_predictions_file = 'predictions.csv'
local_predictions_file = 'predictions.csv'
