from api_data_grab import api_pull, minor_processing
from daily_prediction import get_predicted_runs, \
    admin_input_results, admin_input_lines
from reports import run_yearly_reports, display_gambling_picks, run_daily_report
import pandas as pd
from time import sleep
from datetime import datetime

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

##### Text input on main menu fucking things up


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
    print("Enter 1 for API Pull (Only Do This Once Per Day)")
    print("Enter 2 to Input Today's Betting Lines (And Runs Random Forest)")
    print("Enter 3 to Input Past Game Results (Presumes Model Already Built Yesterday)")
    print("Enter 4 to Return to Main Menu")
    print("Enter 5 to Quit Program")
    print()


def print_user_menu():
    print()
    print("Enter 1 for Today's Picks")
    print("Enter 2 for 2019 Profit Reports")
    print("Enter 3 for Daily Report")
    print("Enter 4 to Return to Main Menu")
    print("Enter 5 to Quit Program")
    print()


def print_choice_menu():
    month1 = input("Give the month as 4, 5, 6, 7, 8, or 9: ")
    print()
    day1 = input("Give the day as 1, 2, ..., 29, 30, or 31: ")
    print()

    try:
        month1 = int(month1)
        day1 = int(day1)

        if month1 in [4, 5, 6, 7, 8, 9]:
            if day1 in list(range(1, 32)):
                if day1 == 31 and month1 in [4, 6, 9]:
                    print("Invalid Date!")
                    sleep(2)
                elif month1 > datetime.now().month or (month1 == datetime.now().month and day1 > datetime.now().day):
                    print("Date out of bounds")
                    sleep(2)
                    return 0, 0
                else:
                    sleep(2)
                    return month1, day1
            else:
                print("Date out of bounds")
                sleep(2)
                return 0, 0
        else:
            print("Date out of bounds")
            sleep(2)
            return 0, 0

    except ValueError:
        print("Jesus, learn how to enter months and dates, OK?")
        sleep(2)
        return 0, 0


run_main_menu = True

while run_main_menu:
    while True:
        try:
            run_admin_menu = True
            run_user_menu = True
            print_main_menu()
            main_menu_choice = int(input("Choice: "))

            if main_menu_choice == 1:
                while True:
                    try:
                        while run_admin_menu:
                            print_admin_menu()
                            admin_menu_choice = int(input("Choice: "))

                            if admin_menu_choice == 1:
                                print()
                                month, day = print_choice_menu()
                                if month == 0:
                                    pass
                                else:
                                    api_pull(month, day)
                                    print("Attempted API Pull")
                                    sleep(2)
                                    minor_processing(month, day)
                                    print("Performed minor processing")
                                    sleep(2)

                            elif admin_menu_choice == 2:
                                print()
                                print("Run today's model and enter betting lines:")
                                print()
                                month, day = print_choice_menu()
                                if month == 0:
                                    pass
                                else:
                                    data = pd.read_csv('./daily_data/outfile_{0}_{1}_pre.csv'.format(month, day), encoding='utf-8')
                                    today = get_predicted_runs(data, month, day)
                                    today = admin_input_lines(today)
                                    today.to_csv('./daily_predictions/predictions_{0}_{1}.csv'.format(month, day), encoding='utf-8')
                                    print(today)

                            elif admin_menu_choice == 3:
                                print()
                                print("Enter past results:")
                                print()
                                month, day = print_choice_menu()
                                if month == 0:
                                    pass
                                else:
                                    print("Enter game results for ", month, "/", day, sep="")
                                    today = pd.read_csv('./daily_predictions/predictions_{0}_{1}.csv'.format(month, day))
                                    today = admin_input_results(today)
                                    today.to_csv('./daily_results/results_{0}_{1}.csv'.format(month, day), encoding='utf-8')
                                    print("Daily results for ", month, "/", day, sep="")
                                    print(today.drop(['month', 'day', 'predicted.runs', 'predicted.run.rank',
                                                      'predicted.bookie.rank', 'betting.opportunity'], axis=1))

                            elif admin_menu_choice == 4:
                                print()
                                print("Back to Main Menu")
                                sleep(2)
                                run_admin_menu = False

                            elif admin_menu_choice == 5:
                                print()
                                print("Quitting Program")
                                sleep(2)
                                run_admin_menu = False
                                run_main_menu = False

                            else:
                                pass

                    except ValueError:
                        print()
                        print("Bad Value Admin Menu")
                        continue
                    else:
                        break

            elif main_menu_choice == 2:
                while True:
                    try:
                        while run_user_menu:
                            print_user_menu()
                            user_menu_choice = int(input("Choice: "))

                            if user_menu_choice == 1:
                                print()
                                print("View Gambling Picks:")
                                print()
                                month, day = print_choice_menu()
                                if month == 0:
                                    pass
                                else:
                                    display_gambling_picks(month, day)
                                    sleep(2)

                            elif user_menu_choice == 2:
                                run_yearly_reports()
                                sleep(2)

                            elif user_menu_choice == 3:
                                print()
                                print("Run Daily Report:")
                                print()
                                month, day = print_choice_menu()
                                if month == 0:
                                    pass
                                else:
                                    run_daily_report(month, day)
                                    sleep(2)

                            elif user_menu_choice == 4:
                                print()
                                print("Back to Main Menu")
                                sleep(2)
                                run_user_menu = False

                            elif user_menu_choice == 5:
                                print()
                                print("Quitting Program")
                                sleep(2)
                                run_user_menu = False
                                run_main_menu = False

                            else:
                                pass

                    except ValueError:
                        print()
                        print("Bad Value User Menu")
                        continue
                    else:
                        break

            elif main_menu_choice == 3:
                print("Quitting Program")
                run_main_menu = False

            else:
                print()
                print("How about a valid menu choice, douche bag?")
                sleep(2)

        except ValueError:
            print()
            print("Bad Value Main Menu")
            continue
        else:
            break

