from api_data_grab import daily_data
from daily_prediction import get_predicted_runs
import pickle
import numpy as np
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

month = input("Give the month as 4, 5, 6, 7, 8, or 9: ")
day = input("Give the day as 1, 2, ..., 29, 30, or 31: ")
print()

with open('./daily_results/results_{0}_{1}'.format(month, day), 'rb') as fp:
    data = pickle.load(fp)

print(data)
