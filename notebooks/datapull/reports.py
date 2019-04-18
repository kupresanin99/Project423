def run_reports():

    import pandas as pd
    from datetime import datetime
    import glob

    path = 'daily_results'
    all_files = glob.glob(path + "/*.csv")

    results = pd.concat((pd.read_csv(f) for f in all_files))

    results.drop(results.columns[0], axis=1, inplace=True)
    results['year'] = datetime.now().year
    results['date'] = pd.to_datetime(results[['year', 'month', 'day']])
    results.drop(['month', 'day', 'year', 'predicted.run.rank', 'predicted.bookie.rank'], axis=1, inplace=True)

    print()
    print("Profit since tracking began on April 14:")
    print("Presume each bet is $100")
    print()
    # Report 1:  Running total of just betting the best daily bet
    report1 = results.groupby('date').apply(lambda t: t[t['betting.opportunity'] == t['betting.opportunity'].max()])
    print("Bet the best bet each day:", report1['bet.result'].sum(), "   Total Bets:", report1['bet.result'].count())

    # Report 2:  Running total of betting every game for which we have data
    print("Bet every game each day:", results['bet.result'].sum(), "    Total Bets:", results['bet.result'].count())

    # Report 3:  Bet the Cubs games only
    report3 = results[(results['home'] == "CHC") | (results['away'] == "CHC")]
    print("Bet only the Cubs games:", report3['bet.result'].sum(), "     Total Bets:", report3['bet.result'].count())
    print()
