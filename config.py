import os

my_api_key = "92jge9phm7k8x746vdj39w83"
my_bucket = "kupebaseball"

local_db = 'sqlite:///sqlite.db'

conn_type = "mysql+pymysql"
user = os.environ.get("MYSQL_USER")
password = os.environ.get("MYSQL_PASSWORD")
host = os.environ.get("MYSQL_HOST")
port = os.environ.get("MYSQL_PORT")
DATABASE_NAME = 'msia423'
local_results = 'data/daily_results/results.csv'
local_csv = 'results.csv'
