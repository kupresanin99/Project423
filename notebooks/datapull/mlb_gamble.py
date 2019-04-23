from api_data_grab import daily_data
from daily_prediction import get_predicted_runs, \
    user_input_lines_and_results, user_input_lines
from reports import run_reports
import pandas as pd
from time import sleep

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


def print_main_menu():
    print()
    print("Baseball Gambling Tool Main Menu")
    print()
    print("Enter 1 for Admin Mode")
    print("Enter 2 for User Mode")
    print("Enter 3 to Quit")
    print()


def print_admin_menu():
    print()
    print("Enter 1 for API Pull")
    print("Enter 2 to Input Today's Betting Lines")
    print("Enter 3 to Input Past Game Results")
    print("Enter 4 to Return to Main Menu")
    print("Enter 5 to Quit Program")
    print()


def print_user_menu():
    print()
    print("Enter 1 for Today's Picks")
    print("Enter 2 for Profit Reports")
    print("Enter 3 to Return to Main Menu")
    print("Enter 4 to Quit Program")
    print()


run_main_menu = True

while run_main_menu:
    run_admin_menu = True
    run_user_menu = True
    print_main_menu()
    main_menu_choice = int(input("Choice: "))

    if main_menu_choice == 1:
        while run_admin_menu:
            print_admin_menu()
            admin_menu_choice = int(input("Choice: "))

            if admin_menu_choice == 1:
                print()
                print("Run API Data Pull:")
                print()
                month = int(input("Give the month as 4, 5, 6, 7, 8, or 9: "))
                print()
                day = int(input("Give the day as 1, 2, ..., 29, 30, or 31: "))
                print()

                if month in [4, 5, 6, 7, 8, 9]:
                    if day in list(range(1, 32)):
                        if day == 31 and month in [4, 6, 9]:
                            print("Invalid Date!")
                            sleep(2)
                        else:
                            data = daily_data(month, day)
                            data.to_csv('./daily_data/outfile_{0}_{1}_pre.csv'.format(month, day), encoding='utf-8')
                            print("Attempted API Pull")
                            sleep(2)
                    else:
                        print("Jesus, learn how to enter months and dates, OK?")
                        sleep(2)

                else:
                    print("Jesus, learn how to enter months and dates, OK?")
                    sleep(2)

            elif admin_menu_choice == 2:
                print()
                print("This will be the entering of the daily lines commands")
                sleep(2)

            elif admin_menu_choice == 3:
                print()
                print("This will be the entering of yesterday's scores commands")
                sleep(2)

            elif admin_menu_choice == 4:
                print()
                print("Back to Main Menu")
                sleep(2)
                run_admin_menu = False

            else:
                print()
                print("Quitting Program")
                sleep(2)
                run_admin_menu = False
                run_main_menu = False

    elif main_menu_choice == 2:
        while run_user_menu:
            print_user_menu()
            user_menu_choice = int(input("Choice: "))

            if user_menu_choice == 1:
                print()
                print("This will show today's picks for the user")
                sleep(2)

            elif user_menu_choice == 2:
                run_reports()

            elif user_menu_choice == 3:
                print()
                print("Back to Main Menu")
                sleep(2)
                run_user_menu = False

            else:
                print()
                print("Quitting Program")
                sleep(2)
                run_user_menu = False
                run_main_menu = False

    elif main_menu_choice == 3:
        print("Quitting Program")
        run_main_menu = False

    else:
        print()
        print("How about a valid menu choice, douche bag?")
        sleep(2)

    # elif task == 1 or task == 2:
    #     print()
    #     print("Hey, bub, need an API data pull?")
    #     answer = input("If so, type YES: ")
    #
    #
    #     if answer == "YES":
    #
    #
    #     else:
    #         data = pd.read_csv('./daily_data/outfile_{0}_{1}_pre.csv'.format(month, day), encoding='utf-8')
    #
    #     if task == 1:
    #         today = get_predicted_runs(data, month, day)
    #         today = user_input_lines_and_results(today)
    #         print(today)
    #         today.to_csv('./daily_results/results_{0}_{1}.csv'.format(month, day), encoding='utf-8')
    #
    #     elif task == 2:
    #         today = get_predicted_runs(data, month, day)
    #         today = user_input_lines(today)
    #         print(today)
    #

