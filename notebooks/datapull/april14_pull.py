import http.client
import json
import pandas as pd
from pandas.io.json import json_normalize
import pickle

month = 4
day = 14

conn = http.client.HTTPSConnection("api.sportradar.us")

conn.request("GET",
             "/mlb/trial/v6.5/en/games/2019/{0}/{1}/boxscore."
             "json?api_key=bw84ac36vu34rdk5vkkh4psx".format(month, day))

res = conn.getresponse()
data = res.read()

baseball_data = []
baseball_data.append(data.decode("utf-8"))

baseball_json = []
baseball_json.append(json.loads(baseball_data[0]))
del baseball_json[0]['_comment']

baseball_normal = json_normalize(baseball_json)
baseball_normal = baseball_normal.drop(columns=
                                       ['league.alias', 'league.date', 'league.id', 'league.name'])

baseball_normal_14 = json_normalize(baseball_normal.iloc[0, 0])

with open('outfile_april_14_pre', 'wb') as fp:
    pickle.dump(baseball_normal_14, fp)
