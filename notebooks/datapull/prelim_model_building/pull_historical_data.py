import http.client
import time
import pickle


def pull_historical_data(month, day):
    """
    Each run calls SportRadar API and returns one day of baseball data

    month = {4, 5, 6, 7, 8, 9}
    day = {1, 2, ..., 30, 31}

    Returns json object which includes multiple baseball variables
    """

    conn = http.client.HTTPSConnection("api.sportradar.us")

    conn.request("GET",
                 "/mlb/trial/v6.5/en/games/2018/{0}/{1}/boxscore."
                 "json?api_key=bw84ac36vu34rdk5vkkh4psx".format(month, day))

    res = conn.getresponse()
    data = res.read()

    return data


baseball_data = []

# Pull all data from 2018 baseball season
for month in range(4, 10):
    for day in range(1, 32):
        baseball_data.append(pull_historical_data(month, day).decode("utf-8"))
        time.sleep(3)

# Save data in pickle
with open('baseball2018', 'wb') as fp:
    pickle.dump(baseball_data, fp)
