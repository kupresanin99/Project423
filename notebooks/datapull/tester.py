from api_data_grab import daily_data
from daily_scrub import clean_todays_data
import pickle
import pandas as pd
import pickle
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import math

month = 4
day = 15
daycount = 105

#data = daily_data(month, day)
#clean_todays_data(data, month, day)

with open('daily_data/outfile_{0}_{1}_pre'.format(month, day), 'rb') as fp:
    model_predict_today = pickle.load(fp)

with open('model_data', 'rb') as fp:
    model_data = pickle.load(fp)  # Load up the 2018 modeling data

today = pd.DataFrame()
today['away'] = model_predict_today['game.away.abbr']
today['home'] = model_predict_today['game.home.abbr']
today['day'] = daycount

model_data = pd.get_dummies(model_data)
model_predict_today = pd.get_dummies(model_predict_today)

# Make sure all columns match

feature_list_2018 = set(list(model_data.columns))
feature_list_today = set(list(model_predict_today.columns))

dropable_columns = list(feature_list_2018.difference(feature_list_today))

model_data = model_data.drop(dropable_columns, axis=1)

feature_list_2018 = set(list(model_data.columns))
feature_list_today = set(list(model_predict_today.columns))

dropable_columns = list(feature_list_today.difference(feature_list_2018))

model_predict_today = model_predict_today.drop(dropable_columns, axis=1)

labels = np.array(model_data['total.runs'])
features = model_data.drop('total.runs', axis=1)
feature_list = list(features.columns)
features = np.array(features)

forest_final = RandomForestRegressor(n_estimators=1600, random_state=99,
                                     bootstrap=True, max_depth=10,
                                     max_features='sqrt', min_samples_leaf=4,
                                     min_samples_split=2)

forest_final.fit(features, labels)

predictions = forest_final.predict(features)

predict_features = model_predict_today.drop('total.runs', axis=1)
predictions_today = forest_final.predict(predict_features)

today['predicted.runs'] = predictions_today
today['bookie'] = [7.5, 7.5, 7, 9, 8]
today['outcome'] = [10, 5, 4, 8, 12]
today['predicted.run.rank'] = today['predicted.runs'].rank()
today['predicted.bookie.rank'] = today['bookie'].rank()
today['the.bet'] = np.where(today['predicted.run.rank'] - today['predicted.bookie.rank'] >= 0, 'OVER', 'UNDER')
today['betting.opportunity'] = abs(today['predicted.run.rank'] - today['predicted.bookie.rank'])
today['game.result'] = np.where(today['outcome'] > today['bookie'], 'OVER', 'UNDER')
today['game.result'] = np.where(today['outcome'] == today['bookie'], 'PUSH', today['game.result'])
today['bet.result'] = np.where(today['the.bet'] == today['game.result'], 100, -100)
today['bet.result'] = np.where(today['game.result'] == 'PUSH', 0, today['bet.result'])
today.sort_values('betting.opportunity', ascending=False)
print(today)

with open('./daily_results/results_{0}_{1}'.format(month, day), 'wb') as fp:
    pickle.dump(today, fp)
