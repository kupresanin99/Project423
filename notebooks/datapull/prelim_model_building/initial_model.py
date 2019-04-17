import pickle
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

with open('model_data', 'rb') as fp:
    model_data = pickle.load(fp)  # Load up the 2018 modeling data

model_data = pd.get_dummies(model_data)

labels = np.array(model_data['total.runs'])
features = model_data.drop('total.runs', axis=1)
feature_list = list(features.columns)
features = np.array(features)

train_features, test_features, train_labels, test_labels = \
    train_test_split(features, labels, test_size=0.25, random_state=99)

forest = RandomForestRegressor(n_estimators=1000, random_state=99)

forest.fit(train_features, train_labels)

predictions = forest.predict(test_features)

errors = abs(predictions - test_labels)

print('Mean Absolute Error:', round(np.mean(errors), 2), 'runs.')

mape = 100 * (errors / test_labels)
accuracy = 100 - np.mean(mape)
print('Accuracy:', round(accuracy, 2), '%.')

