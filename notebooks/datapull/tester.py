from api_data_grab import daily_data
from daily_prediction import get_predicted_runs
import pickle
import numpy as np
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

month = input("Give the month as 4, 5, 6, 7, 8, or 9, OK? ")
day = input("Give the day as 1, 2, ..., 29, 30, or 31, OK? ")

# data = daily_data(month, day)
#
# with open('./daily_data/outfile_{0}_{1}_pre'.format(month, day), 'wb') as fp:
#     pickle.dump(data, fp)

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
today['game.result'] = np.where(today['outcome'] > today['bookie'], 'OVER', 'UNDER')
today['game.result'] = np.where(today['outcome'] == today['bookie'], 'PUSH', today['game.result'])
today['bet.result'] = np.where(today['the.bet'] == today['game.result'], 100, -100)
today['bet.result'] = np.where(today['game.result'] == 'PUSH', 0, today['bet.result'])
today = today.sort_values('betting.opportunity', ascending=False)
print(today)

with open('./daily_results/results_{0}_{1}'.format(month, day), 'wb') as fp:
    pickle.dump(today, fp)
