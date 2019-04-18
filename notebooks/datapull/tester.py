from api_data_grab import daily_data
from daily_prediction import get_predicted_runs, user_input_results
import pickle
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

print("Hey, bub, need a data pull?")
answer = input("If so, type YES: ")
print()
month = input("Give the month as 4, 5, 6, 7, 8, or 9: ")
day = input("Give the day as 1, 2, ..., 29, 30, or 31: ")
print()

# Need to put decision here for user
# Are you gambling for today?
# Or are you just inputting results from the past?

if answer == "YES":

    data = daily_data(month, day)
    # with open('./daily_data/outfile_{0}_{1}_pre'.format(month, day), 'wb') as fp:
    #     pickle.dump(data, fp)
    data.to_csv('./daily_data/outfile_{0}_{1}_pre'.format(month, day), encoding='utf-8')

else:
    # with open('./daily_data/outfile_{0}_{1}_pre'.format(month, day), 'rb') as fp:
    #     data = pickle.load(fp)
    data = pd.read_csv('./daily_data/outfile_{0}_{1}_pre'.format(month, day), encoding='utf-8')

today = get_predicted_runs(data, month, day)
today = user_input_results(today)

print(today)

# with open('./daily_results/results_{0}_{1}'.format(month, day), 'wb') as fp:
#     pickle.dump(today, fp)

today.to_csv('./daily_results/results_{0}_{1}'.format(month, day), encoding='utf-8')
