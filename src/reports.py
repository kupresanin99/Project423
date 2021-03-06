def run_yearly_reports():
    """Pulls all gambling results from RDS for 2019 season and creates user reports"""
    import pandas as pd
    from time import sleep
    import sqlalchemy as sql
    import config

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

    engine_string = "{}://{}:{}@{}:{}/{}". \
        format(config.conn_type, config.user, config.password, config.host, config.port, config.DATABASE_NAME)
    engine = sql.create_engine(engine_string)

    results = pd.read_sql('SELECT * FROM Reports', con=engine)

    print()
    print("Profit / Loss Report for the 2019 season:")
    print("(Each bet is $100)")

    # Report 1:  Running total of just betting the best daily bet
    print()
    report1 = results.groupby('date').apply(lambda t: t[t['betting_opportunity'] == t['betting_opportunity'].max()])
    print("Only bet the best pick each day: $", report1['bet_result'].sum(), sep="")
    print("Total Bets: ", report1['bet_result'].count(), sep='')
    print("Winning Percentage: ", round(100 * report1['bet_result'].value_counts()[100] / (report1['bet_result'].value_counts()[100] +
                                                       report1['bet_result'].value_counts()[-100]), 2), "%", sep="")
    sleep(3)
    print()

    # Report 2:  Running total of betting every game for which we have data
    print("Bet every single game every day: $", results['bet_result'].sum(), sep="")
    print("Total Bets: ", results['bet_result'].count(), sep='')
    print("Winning Percentage: ", round(100 * results['bet_result'].value_counts()[100] / (results['bet_result'].value_counts()[100] +
                                                       results['bet_result'].value_counts()[-100]), 2), "%", sep="")
    sleep(3)
    print()

    # Report 3:  Best team to bet
    team_list = list(team_dict.keys())
    max_win = -10000
    best_team = 'XXX'
    for team in team_list:
        report3 = results[(results['home'] == team) | (results['away'] == team)]
        if report3['bet_result'].sum() > max_win:
            max_win = report3['bet_result'].sum()
            best_team = team

    report3 = results[(results['home'] == best_team) | (results['away'] == best_team)]
    print("The best team to bet on has been the", team_dict[best_team])
    print("Bet only the ", team_dict[best_team], " games: $", report3['bet_result'].sum(), sep="")
    print("Total Bets: ", report3['bet_result'].count(), sep='')
    print("Winning Percentage: ", round(100 * report3['bet_result'].value_counts()[100] / (report3['bet_result'].value_counts()[100] +
                                                       report3['bet_result'].value_counts()[-100]), 2), "%", sep="")


def should_bet(x):
    """For betting predictions, classifies each game in terms of how good the betting opportunity is - (arbitrary)"""
    if x > 8:
        return 'Huge'
    elif x > 6:
        return 'Good'
    elif x > 4:
        return 'Mediocre'
    else:
        return 'Avoid'


def display_gambling_picks(month, day):
    """For a given date, returns the gambling predictions for the slate of MLB games.  To be served on Flask."""
    import pandas as pd
    import sqlalchemy as sql
    import config
    engine_string = "{}://{}:{}@{}:{}/{}". \
        format(config.conn_type, config.user, config.password, config.host, config.port, config.DATABASE_NAME)
    engine = sql.create_engine(engine_string)

    try:
        gambling_picks = pd.read_sql('SELECT * FROM Predictions WHERE month={0} AND day={1}'.format(month, day), con=engine)
        gambling_picks.drop(gambling_picks.columns[0], axis=1, inplace=True)
        gambling_picks.drop(['predicted_runs', 'predicted_run_rank', 'predicted_bookie_rank',
                             'month', 'day', 'game', 'nonsense'], axis=1, inplace=True)
        gambling_picks['betting_opportunity'] = gambling_picks['betting_opportunity'].apply(should_bet)
        gambling_picks = gambling_picks[['home', 'away', 'bookie', 'bet', 'betting_opportunity']]
        gambling_picks.columns = ['Home', 'Away', 'Line', 'Bet', 'Opportunity']
        print("Sorted from best to worst for ", month, "/", day, sep="")
        print(gambling_picks)

    except:
        print("Data not in RDS yet.  Patience, hermano / hermana.")
        print("Or user error, OK?")


def run_daily_report(month, day):
    """For a given date, returns the gambling results for the slate of MLB games."""
    import pandas as pd
    import config
    import sqlalchemy as sql

    try:
        engine_string = "{}://{}:{}@{}:{}/{}". \
            format(config.conn_type, config.user, config.password, config.host, config.port, config.DATABASE_NAME)
        engine = sql.create_engine(engine_string)
        daily_report = pd.read_sql('SELECT * FROM Reports WHERE month={0} AND day={1}'.format(month, day), con=engine)
        daily_report.drop(daily_report.columns[0], axis=1, inplace=True)
        daily_report.drop(['predicted_runs', 'predicted_run_rank', 'predicted_bookie_rank', 'betting_opportunity',
                             'month', 'day', 'game', 'year', 'date'], axis=1, inplace=True)
        daily_report = daily_report[['home', 'away', 'bookie', 'bet', 'outcome', 'game_result', 'bet_result']]
        daily_report.columns = ['Home', 'Away', 'Line', 'Bet', 'Runs Scored', 'Game Result', 'Bet Result', ]
        print("Sorted from best to worst for ", month, "/", day, sep="")
        print(daily_report)

    except:
        print("Data not in RDS yet.  Patience, hermano / hermana.")
        print("Or user error, OK?")
