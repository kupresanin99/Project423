def api_pull(month, day, bucket, key):

    import http.client
    import pickle
    import boto3
    import os

    conn = http.client.HTTPSConnection("api.sportradar.us")

    conn.request("GET",
                 "/mlb/trial/v6.5/en/games/2019/{0}/{1}/boxscore."
                 "json?api_key={2}".format(month, day, key))

    res = conn.getresponse()
    data = res.read() 

    with open('data/daily_raw/raw_{0}_{1}'.format(month, day), 'wb') as fp:
        pickle.dump(data, fp)

    s3 = boto3.resource("s3")
    s3.meta.client.upload_file("data/daily_raw/raw_{0}_{1}".format(month, day), bucket, "data/daily_raw/raw_{0}_{1}".format(month,day))

    if os.path.exists("data/daily_raw/raw_{0}_{1}".format(month, day)):
        os.remove("data/daily_raw/raw_{0}_{1}".format(month, day))


def minor_processing(month, day):

    import json
    from pandas.io.json import json_normalize
    import pickle
    import boto3
    import os
    import config

    s3 = boto3.resource("s3")
    s3.meta.client.download_file(config.my_bucket, 'data/daily_raw/raw_{0}_{1}'.format(month, day), 'data/daily_raw/raw_{0}_{1}'.format(month, day))

    with open('data/daily_raw/raw_{0}_{1}'.format(month, day), 'rb') as fp:
        data = pickle.load(fp)

    if os.path.exists("data/daily_raw/raw_{0}_{1}".format(month, day)):
        os.remove("data/daily_raw/raw_{0}_{1}".format(month, day))

    baseball_data = []
    baseball_data.append(data.decode("utf-8"))

    baseball_json = []
    baseball_json.append(json.loads(baseball_data[0]))
    del baseball_json[0]['_comment']

    baseball_normal = json_normalize(baseball_json)
    baseball_normal = baseball_normal.drop(columns=
                                           ['league.alias', 'league.date', 'league.id', 'league.name'])

    data = json_normalize(baseball_normal.iloc[0, 0])
    data.to_csv('data/daily_data/outfile_{0}_{1}_pre.csv'.format(month, day), encoding='utf-8')

    s3.meta.client.upload_file("data/daily_data/outfile_{0}_{1}_pre.csv".format(month, day), config.my_bucket, "data/daily_data/outfile_{0}_{1}_pre.csv".format(month, day))

    if os.path.exists("data/daily_data/outfile_{0}_{1}_pre.csv".format(month, day)):
        os.remove("data/daily_data/outfile_{0}_{1}_pre.csv".format(month, day))

