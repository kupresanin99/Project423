import sqlalchemy as db

engine = db.create_engine('sqlite:///joe_test.db')
connection = engine.connect()
metadata = db.MetaData()
reports = db.Table('Reports', metadata, autoload=True, autoload_with=engine)

query = db.select([reports])
ResultProxy = connection.execute(query)
ResultSet = ResultProxy.fetchall()
print(ResultSet[:11])

