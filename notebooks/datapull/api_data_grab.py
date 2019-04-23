def api_pull(month, day):

    import http.client
    import pickle

    conn = http.client.HTTPSConnection("api.sportradar.us")

    conn.request("GET",
                 "/mlb/trial/v6.5/en/games/2019/{0}/{1}/boxscore."
                 "json?api_key=bw84ac36vu34rdk5vkkh4psx".format(month, day))

    res = conn.getresponse()
    data = res.read()
    with open('daily_raw/raw_{0}_{1}'.format(month, day), 'wb') as fp:
        pickle.dump(data, fp)


def minor_processing(month, day):

    import json
    from pandas.io.json import json_normalize
    import pickle

    with open('daily_raw/raw_{0}_{1}'.format(month, day), 'rb') as fp:
        data = pickle.load(fp)

    baseball_data = []
    baseball_data.append(data.decode("utf-8"))

    baseball_json = []
    baseball_json.append(json.loads(baseball_data[0]))
    del baseball_json[0]['_comment']

    baseball_normal = json_normalize(baseball_json)
    baseball_normal = baseball_normal.drop(columns=
                                           ['league.alias', 'league.date', 'league.id', 'league.name'])

    data = json_normalize(baseball_normal.iloc[0, 0])
    data.to_csv('./daily_data/outfile_{0}_{1}_pre.csv'.format(month, day), encoding='utf-8')
