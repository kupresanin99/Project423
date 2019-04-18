from api_data_grab import daily_data
from daily_prediction import get_predicted_runs, \
    user_input_lines_and_results, user_input_lines
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

print("Hey, bub, need an API data pull?")
answer = input("If so, type YES: ")
print()
month = input("Give the month as 4, 5, 6, 7, 8, or 9: ")
day = input("Give the day as 1, 2, ..., 29, 30, or 31: ")
print()

print("Do you need gambling picks for today or recording past results?")
print()
print("Recording past results?  Enter 1")
print("Gambling picks for today?  Enter 2")
task = int(input("1 or 2: "))

if answer == "YES":
    data = daily_data(month, day)
    data.to_csv('./daily_data/outfile_{0}_{1}_pre'.format(month, day), encoding='utf-8')

else:
    data = pd.read_csv('./daily_data/outfile_{0}_{1}_pre'.format(month, day), encoding='utf-8')

if task == 1:
    today = get_predicted_runs(data, month, day)
    today = user_input_lines_and_results(today)
    print(today)
    today.to_csv('./daily_results/results_{0}_{1}'.format(month, day), encoding='utf-8')

elif task == 2:
    today = get_predicted_runs(data, month, day)
    today = user_input_lines(today)
    print(today)
