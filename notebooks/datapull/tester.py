from api_data_grab import daily_data
from daily_prediction import get_predicted_runs
import pickle
import numpy as np
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

print("Hey, bub, need a data pull?")
answer = input("If so, type YES: ")
print()
month = input("Give the month as 4, 5, 6, 7, 8, or 9: ")
day = input("Give the day as 1, 2, ..., 29, 30, or 31: ")
print()

if answer == "YES":

    data = daily_data(month, day)
    with open('./daily_data/outfile_{0}_{1}_pre'.format(month, day), 'wb') as fp:
        pickle.dump(data, fp)

else:
    with open('./daily_data/outfile_{0}_{1}_pre'.format(month, day), 'rb') as fp:
        data = pickle.load(fp)

today = get_predicted_runs(data, month, day)
bookie = []
outcome = []
print(today)
for game in range(today.shape[0]):
    print()
    q = "Enter bookie line for " + today.iloc[game, 0] + " vs " + today.iloc[game, 1] + ": "
    bookie.append(input(q))
    a = "Enter runs scored for " + today.iloc[game, 0] + " vs " + today.iloc[game, 1] + ": "
    outcome.append(input(a))

today['bookie'] = bookie
today['outcome'] = outcome
today['predicted.run.rank'] = today['predicted.runs'].rank()
today['predicted.bookie.rank'] = today['bookie'].rank()
today['the.bet'] = np.where(today['predicted.run.rank'] - today['predicted.bookie.rank'] >= 0, 'OVER', 'UNDER')
today['betting.opportunity'] = abs(today['predicted.run.rank'] - today['predicted.bookie.rank'])

condition_list = [today["outcome"] > today["bookie"],
                  today["outcome"] < today["bookie"],
                  today["outcome"] == today["bookie"]]
choice_list = ["OVER", "UNDER", "PUSH"]
today['game.result'] = np.select(condition_list, choice_list)

condition_list2 = [today["the.bet"] == today["game.result"],
                   (today["the.bet"] != today["game.result"]) & (today["game.result"] != "PUSH"),
                   today["game.result"] == "PUSH"]
choice_list2 = [100, -100, 0]

today['bet.result'] = np.select(condition_list2, choice_list2)
today.sort_values(by=['betting.opportunity'], ascending=False, inplace=True)
print(today)

with open('./daily_results/results_{0}_{1}'.format(month, day), 'wb') as fp:
    pickle.dump(today, fp)
