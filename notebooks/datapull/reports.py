def run_yearly_reports():
    import pandas as pd
    from datetime import datetime
    import glob
    from time import sleep

    team_dict = {'TB': 'Tampa Bay Rays', 'NYY': 'New York Yankees', 'TOR': 'Toronto Blue Jays',
                 'BAL': 'Baltimore Orioles', 'BOS': 'Boston Red Sox', 'CLE': 'Cleveland Indians',
                 'MIN': 'Minnesota Twins', 'DET': 'Detroit Tigers', 'CWS': 'Chicago White Sox',
                 'KC': 'Kansas City Royals', 'HOU': 'Houston Astros', 'SEA': 'Seattle Mariners',
                 'TEX': 'Texas Rangers', 'OAK': 'Oakland Athletics', 'LAA': 'Los Angeles Angels',
                 'PHI': 'Philadelphia Phillies', 'NYM': 'New York Mets', 'WSH': 'Washington Nationals',
                 'ATL': 'Atlanta Braves', 'MIA': 'Miami Marlins', 'MIL': 'Milwaukee Brewers',
                 'PIT': 'Pittsburgh Pirates', 'STL': 'St. Louis Cardinals', 'CHC': 'Chicago Cubs',
                 'CIN': 'Cincinnati Reds', 'LAD': 'Los Angeles Dodgers', 'SD': 'San Diego Padres',
                 'ARI': 'Arizona Diamondbacks', 'SF': 'San Francisco Giants', 'COL': 'Colorado Rockies'}

    path = 'daily_results'
    all_files = glob.glob(path + "/*.csv")

    results = pd.concat((pd.read_csv(f) for f in all_files), sort=True)

    results.drop(results.columns[0], axis=1, inplace=True)
    results['year'] = datetime.now().year
    results['date'] = pd.to_datetime(results[['year', 'month', 'day']])
    results.drop(['month', 'day', 'year', 'predicted.run.rank', 'predicted.bookie.rank'], axis=1, inplace=True)

    print()
    print("Profit / Loss Report for the 2019 season:")
    print("(Each bet is $100)")

    # Report 1:  Running total of just betting the best daily bet
    print()
    report1 = results.groupby('date').apply(lambda t: t[t['betting.opportunity'] == t['betting.opportunity'].max()])
    print("Only bet the 10-star pick each day: $", report1['bet.result'].sum(), sep="")
    print("Total Bets: ", report1['bet.result'].count(), sep='')
    print("Winning Percentage: ", round(100 * report1['bet.result'].value_counts()[100] / (report1['bet.result'].value_counts()[100] +
                                                       report1['bet.result'].value_counts()[-100]), 2), "%", sep="")
    sleep(3)
    print()

    # Report 2:  Running total of betting every game for which we have data
    print("Bet every single game every day: $", results['bet.result'].sum(), sep="")
    print("Total Bets: ", results['bet.result'].count(), sep='')
    print("Winning Percentage: ", round(100 * results['bet.result'].value_counts()[100] / (results['bet.result'].value_counts()[100] +
                                                       results['bet.result'].value_counts()[-100]), 2), "%", sep="")
    sleep(3)
    print()

    # Report 3:  Best team to bet
    team_list = list(team_dict.keys())
    max_win = -10000
    best_team = 'XXX'
    for team in team_list:
        report3 = results[(results['home'] == team) | (results['away'] == team)]
        if report3['bet.result'].sum() > max_win:
            max_win = report3['bet.result'].sum()
            best_team = team

    report3 = results[(results['home'] == best_team) | (results['away'] == best_team)]
    print("The best team to bet on has been the", team_dict[best_team])
    print("Bet only the ", team_dict[best_team], " games: $", report3['bet.result'].sum(), sep="")
    print("Total Bets: ", report3['bet.result'].count(), sep='')
    print("Winning Percentage: ", round(100 * report3['bet.result'].value_counts()[100] / (report3['bet.result'].value_counts()[100] +
                                                       report3['bet.result'].value_counts()[-100]), 2), "%", sep="")


def display_gambling_picks(month, day):
    import pandas as pd

    gambling_picks = pd.read_csv('./daily_predictions/predictions_{0}_{1}.csv'.format(month, day))
    gambling_picks.drop(gambling_picks.columns[0], axis=1, inplace=True)
    gambling_picks.drop(['predicted.runs', 'predicted.run.rank', 'predicted.bookie.rank', 'betting.opportunity',
                         'month', 'day'], axis=1, inplace=True)
    print("Sorted from best to worst for ", month, "/", day, sep="")
    print(gambling_picks)


def run_daily_report(month, day):
    import pandas as pd

    daily_report = pd.read_csv('./daily_results/results_{0}_{1}.csv'.format(month, day))
    daily_report.drop(daily_report.columns[0], axis=1, inplace=True)
    daily_report.drop(['predicted.runs', 'predicted.run.rank', 'predicted.bookie.rank', 'betting.opportunity',
                         'month', 'day'], axis=1, inplace=True)
    print("Sorted from best to worst for ", month, "/", day, sep="")
    print(daily_report)
