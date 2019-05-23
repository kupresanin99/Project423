def api_pull(month, day, bucket, key):
    """Takes date, AWS bucket from user, calls API and saves raw data to S3"""
    import http.client
    import pickle
    import boto3
    import os

    conn = http.client.HTTPSConnection("api.sportradar.us")
    local_raw = 'raw_{0}_{1}'
    conn.request("GET",
                 "/mlb/trial/v6.5/en/games/2019/{0}/{1}/boxscore."
                 "json?api_key={2}".format(month, day, key))

    res = conn.getresponse()
    data = res.read() 

    with open(local_raw.format(month, day), 'wb') as fp:
        pickle.dump(data, fp)

    s3 = boto3.resource("s3")
    s3.meta.client.upload_file(local_raw.format(month, day), bucket, local_raw.format(month, day))

    if os.path.exists(local_raw.format(month, day)):
        os.remove(local_raw.format(month, day))


def minor_processing(month, day, bucket):
    """Calls S3 to get raw daily data, jsonifies it, cleans it slightly, pops it back to S3"""
    import json
    from pandas.io.json import json_normalize
    import pickle
    import boto3
    import os

    s3 = boto3.resource("s3")
    local_raw = 'raw_{0}_{1}'
    local_data = 'outfile_{0}_{1}_pre.csv'
    s3.meta.client.download_file(bucket, local_raw.format(month, day), local_raw.format(month, day))

    with open(local_raw.format(month, day), 'rb') as fp:
        data = pickle.load(fp)

    if os.path.exists(local_raw.format(month, day)):
        os.remove(local_raw.format(month, day))

    baseball_data = []
    baseball_data.append(data.decode("utf-8"))

    baseball_json = []
    baseball_json.append(json.loads(baseball_data[0]))
    del baseball_json[0]['_comment']

    baseball_normal = json_normalize(baseball_json)
    baseball_normal = baseball_normal.drop(columns=
                                           ['league.alias', 'league.date', 'league.id', 'league.name'])

    data = json_normalize(baseball_normal.iloc[0, 0])
    data.to_csv(local_data.format(month, day), encoding='utf-8')

    s3.meta.client.upload_file(local_data.format(month, day), bucket, local_data.format(month, day))

    if os.path.exists(local_data.format(month, day)):
        os.remove(local_data.format(month, day))

