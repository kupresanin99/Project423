def get_predicted_runs(data, month, day):

    from sklearn.ensemble import RandomForestRegressor
    import numpy as np
    import pickle
    import pandas as pd
    from sklearn.model_selection import RandomizedSearchCV
    import math

    data['home.win.pct'] = data['game.home.win'] / (data['game.home.win'] + data['game.home.loss'])
    data['away.win.pct'] = data['game.away.win'] / (data['game.away.win'] + data['game.away.loss'])
    data['home.pitcher.win.pct'] = data['game.home.probable_pitcher.win'] / (
                data['game.home.probable_pitcher.win'] + data['game.home.probable_pitcher.loss'])
    data['away.pitcher.win.pct'] = data['game.away.probable_pitcher.win'] / (
                data['game.away.probable_pitcher.win'] + data['game.away.probable_pitcher.loss'])
    data['total.runs'] = data['game.home.runs'] + data['game.away.runs']

    data = data.drop(['game.away.errors', 'game.away.hits', 'game.away.runs',
                      'game.home.errors', 'game.home.hits', 'game.home.runs'], axis=1)

    data['game.weather.forecast.condition'].fillna('unknown', inplace=True)
    data['game.weather.forecast.wind.direction'].fillna('unknown', inplace=True)
    data['game.venue.field_orientation'].fillna('unknown', inplace=True)
    data['game.venue.stadium_type'].fillna('unknown', inplace=True)

    data['game.weather.forecast.condition'] = data['game.weather.forecast.condition']. \
        str.replace("moderate snow", "Snow", case=False)
    data['game.weather.forecast.condition'] = data['game.weather.forecast.condition']. \
        str.replace("heavy snow", "Snow", case=False)
    data['game.weather.forecast.condition'] = data['game.weather.forecast.condition']. \
        str.replace("moderate or heavy snow showers", "Snow", case=False)
    data['game.weather.forecast.condition'] = data['game.weather.forecast.condition']. \
        str.replace("moderate or snow showers", "Snow", case=False)
    data['game.weather.forecast.condition'] = data['game.weather.forecast.condition']. \
        str.replace("patchy snow", "Snow", case=False)
    data['game.weather.forecast.condition'] = data['game.weather.forecast.condition']. \
        str.replace("patchy light snow", "Snow", case=False)
    data['game.weather.forecast.condition'] = data['game.weather.forecast.condition']. \
        str.replace("light snow", "Snow", case=False)
    data['game.weather.forecast.condition'] = data['game.weather.forecast.condition']. \
        str.replace("light snow, mist", "Snow", case=False)
    data['game.weather.forecast.condition'] = data['game.weather.forecast.condition']. \
        str.replace("squalls", "Snow", case=False)
    data['game.weather.forecast.condition'] = data['game.weather.forecast.condition']. \
        str.replace("snow, mist", "Snow", case=False)
    data['game.weather.forecast.condition'] = data['game.weather.forecast.condition']. \
        str.replace("light sleet", "Snow", case=False)
    data['game.weather.forecast.condition'] = data['game.weather.forecast.condition']. \
        str.replace("light drizzle", "Rain", case=False)
    data['game.weather.forecast.condition'] = data['game.weather.forecast.condition']. \
        str.replace("patchy rain possible", "Rain", case=False)
    data['game.weather.forecast.condition'] = data['game.weather.forecast.condition']. \
        str.replace("Light rain", "Rain", case=False)
    data['game.weather.forecast.condition'] = data['game.weather.forecast.condition']. \
        str.replace("patchy light rain", "Rain", case=False)
    data['game.weather.forecast.condition'] = data['game.weather.forecast.condition']. \
        str.replace("moderate rain", "Rain", case=False)
    data['game.weather.forecast.condition'] = data['game.weather.forecast.condition']. \
        str.replace("light rain shower", "Rain", case=False)
    data['game.weather.forecast.condition'] = data['game.weather.forecast.condition']. \
        str.replace("patchy light drizzle", "Rain", case=False)
    data['game.weather.forecast.condition'] = data['game.weather.forecast.condition']. \
        str.replace("light rain, mist", "Rain", case=False)
    data['game.weather.forecast.condition'] = data['game.weather.forecast.condition']. \
        str.replace("light drizzle, mist", "Rain", case=False)
    data['game.weather.forecast.condition'] = data['game.weather.forecast.condition']. \
        str.replace("Shower in Vicinity", "Rain", case=False)
    data['game.weather.forecast.condition'] = data['game.weather.forecast.condition']. \
        str.replace("overcast", "Cloudy", case=False)
    data['game.weather.forecast.condition'] = data['game.weather.forecast.condition']. \
        str.replace("Thundery outbreaks possible", "Storm", case=False)
    data['game.weather.forecast.condition'] = data['game.weather.forecast.condition']. \
        str.replace("rain shower", "Rain", case=False)
    data['game.weather.forecast.condition'] = data['game.weather.forecast.condition']. \
        str.replace("thunderstorm in vicinity", "Storm", case=False)
    data['game.weather.forecast.condition'] = data['game.weather.forecast.condition']. \
        str.replace("heavy rain", "Storm", case=False)
    data['game.weather.forecast.condition'] = data['game.weather.forecast.condition']. \
        str.replace("torrential rain shower", "Storm", case=False)
    data['game.weather.forecast.condition'] = data['game.weather.forecast.condition']. \
        str.replace("rain with thunderstorm, mist", "Storm", case=False)
    data['game.weather.forecast.condition'] = data['game.weather.forecast.condition']. \
        str.replace("thunderstorm", "Storm", case=False)
    data['game.weather.forecast.condition'] = data['game.weather.forecast.condition']. \
        str.replace("thunderstorm, haze", "Storm", case=False)
    data['game.weather.forecast.condition'] = data['game.weather.forecast.condition']. \
        str.replace("heavy rain, mist", "Rain", case=False)
    data['game.weather.forecast.condition'] = data['game.weather.forecast.condition']. \
        str.replace("Partly cloudy", "Cloudy", case=False)
    data['game.weather.forecast.condition'] = data['game.weather.forecast.condition']. \
        str.replace("Patchy rain", "Rain", case=False)
    data['game.weather.forecast.condition'] = data['game.weather.forecast.condition']. \
        str.replace("Rain, Mist", "Mist", case=False)
    data['game.weather.forecast.condition'] = data['game.weather.forecast.condition']. \
        str.replace("Torrential Rain", "Storm", case=False)
    data['game.weather.forecast.condition'] = data['game.weather.forecast.condition']. \
        str.replace("Moderate or Storm", "Storm", case=False)
    data['game.weather.forecast.condition'] = data['game.weather.forecast.condition']. \
        str.replace("Patchy rain with thunder", "Storm", case=False)
    data['game.weather.forecast.condition'] = data['game.weather.forecast.condition']. \
        str.replace("rain with storm", "Storm", case=False)
    data['game.weather.forecast.condition'] = data['game.weather.forecast.condition']. \
        str.replace("storm, rain", "Storm", case=False)
    data['game.weather.forecast.condition'] = data['game.weather.forecast.condition']. \
        str.replace("storm with storm", "Storm", case=False)
    data['game.weather.forecast.condition'] = data['game.weather.forecast.condition']. \
        str.replace("Storm, Mist", "Mist", case=False)
    data['game.weather.forecast.condition'] = data['game.weather.forecast.condition']. \
        str.replace("Rain with thunder", "Storm", case=False)
    data['game.weather.forecast.condition'] = data['game.weather.forecast.condition']. \
        str.replace("Blowing Widespread Dust", "Haze", case=False)
    data['game.weather.forecast.condition'] = data['game.weather.forecast.condition']. \
        str.replace("Smoke", "Haze", case=False)
    data['game.weather.forecast.condition'] = data['game.weather.forecast.condition']. \
        str.replace("Storm, Haze", "Storm", case=False)
    data['game.weather.forecast.condition'] = data['game.weather.forecast.condition']. \
        str.replace("Haze, Smoke", "Haze", case=False)
    data['game.weather.forecast.condition'] = data['game.weather.forecast.condition']. \
        str.replace("Storm, Fog", "Storm", case=False)
    data['game.weather.forecast.condition'] = data['game.weather.forecast.condition']. \
        str.replace("Haze, Haze", "Haze", case=False)
    data['game.weather.forecast.condition'] = data['game.weather.forecast.condition']. \
        str.replace("Fog", "Mist", case=False)

    # Must drop unnecessary variables
    data = data.drop(['game.away.id', 'game.away.market', 'game.away.name',
                      'game.away.probable_pitcher.first_name',
                      'game.away.probable_pitcher.jersey_number',
                      'game.away.probable_pitcher.last_name',
                      'game.away.probable_pitcher.preferred_name',
                      'game.away_team', 'game.coverage',
                      'game.game_number', 'game.home.id',
                      'game.home.market', 'game.home.name',
                      'game.home.probable_pitcher.first_name',
                      'game.home.probable_pitcher.jersey_number',
                      'game.home.probable_pitcher.last_name',
                      'game.home.probable_pitcher.preferred_name',
                      'game.home_team',
                      'game.scheduled', 'game.status',
                      'game.venue.address', 'game.venue.country',
                      'game.venue.market', 'game.venue.state',
                      'game.venue.zip', 'game.weather.forecast.obs_time',
                      'game.id', 'game.venue.city', 'game.venue.id',
                      'game.double_header', 'game.venue.location.lat',
                      'game.venue.location.lng',
                      'game.away.loss', 'game.away.win',
                      'game.home.loss', 'game.home.win',
                      'game.home.probable_pitcher.win',
                      'game.home.probable_pitcher.loss',
                      'game.away.probable_pitcher.win',
                      'game.away.probable_pitcher.loss',
                      'game.away.probable_pitcher.id',
                      'game.home.probable_pitcher.id',
                      'game.broadcast.network'], axis=1)

    with open('model_data', 'rb') as fp:
        model_data = pickle.load(fp)  # Load up the 2018 modeling data

    model_predict_today = data

    # Make sure all columns match

    feature_list_2018 = set(list(model_data.columns))
    feature_list_today = set(list(model_predict_today.columns))
    intersection = feature_list_today.intersection(feature_list_2018)

    dropable_columns_model = list(feature_list_2018.difference(intersection))
    dropable_columns_today = list(feature_list_today.difference(intersection))

    model_data = model_data.drop(dropable_columns_model, axis=1)
    model_predict_today = model_predict_today.drop(dropable_columns_today, axis=1)

    model_predict_today.dropna(axis=0, inplace=True)
    today = pd.DataFrame()
    today['away'] = model_predict_today['game.away.abbr']
    today['home'] = model_predict_today['game.home.abbr']
    today['month'] = month
    today['day'] = day

    model_data = pd.get_dummies(model_data)
    model_predict_today = pd.get_dummies(model_predict_today)

    feature_list_2018 = set(list(model_data.columns))
    feature_list_today = set(list(model_predict_today.columns))
    intersection = feature_list_today.intersection(feature_list_2018)
    dropable_columns_model = list(feature_list_2018.difference(intersection))
    dropable_columns_today = list(feature_list_today.difference(intersection))

    model_data = model_data.drop(dropable_columns_model, axis=1)
    model_predict_today = model_predict_today.drop(dropable_columns_today, axis=1)

    labels = np.array(model_data['total.runs'])
    features = model_data.drop('total.runs', axis=1)
    features = np.array(features)

    # Get good set of hyperparameters (daily tuning)

    n_estimators = [int(x) for x in np.linspace(start = 200, stop = 2000, num = 10)]  # Number of trees in random forest
    max_features = ['auto', 'sqrt']    # Number of features to consider at every split
    max_depth = [int(x) for x in np.linspace(10, 110, num = 11)]      # Maximum number of levels in tree
    max_depth.append(None)
    min_samples_split = [2, 5, 10]    # Minimum number of samples required to split a node
    min_samples_leaf = [1, 2, 4]    # Minimum number of samples required at each leaf node
    bootstrap = [True, False]    # Method of selecting samples for training each tree
    random_grid = {'n_estimators': n_estimators,    # Create the random grid
                   'max_features': max_features,
                   'max_depth': max_depth,
                   'min_samples_split': min_samples_split,
                   'min_samples_leaf': min_samples_leaf,
                   'bootstrap': bootstrap}

    print("Cooking up today's model, please wait about 5 minutes.")
    print()
    rf = RandomForestRegressor()  # Random search of parameters, using 5 fold cross validation
    rf_random = RandomizedSearchCV(estimator = rf,
                                   param_distributions = random_grid,
                                   n_iter = 20, cv = 5, verbose=0,
                                   random_state=99, n_jobs = -1)
    # Fit the random search model
    rf_random.fit(features, labels)
    print("Today's random forest model parameters: ")
    print("Number of Estimators: ", rf_random.best_params_['n_estimators'])
    print("Bootstrap: ", rf_random.best_params_['bootstrap'])
    print("Maximum Depth: ", rf_random.best_params_['max_depth'])
    print("Maximum Features: ", rf_random.best_params_['max_features'])
    print("Minimum Samples per Leaf: ", rf_random.best_params_['min_samples_leaf'])
    print("Minimum Samples per Split: ", rf_random.best_params_['min_samples_split'])
    print()

    forest_final = RandomForestRegressor(n_estimators=rf_random.best_params_['n_estimators'],
                                         random_state=99,
                                         bootstrap=rf_random.best_params_['bootstrap'],
                                         max_depth=rf_random.best_params_['max_depth'],
                                         max_features=rf_random.best_params_['max_features'],
                                         min_samples_leaf=rf_random.best_params_['min_samples_leaf'],
                                         min_samples_split=rf_random.best_params_['min_samples_split'])

    forest_final.fit(features, labels)
    predictions = forest_final.predict(features)
    predict_features = model_predict_today.drop('total.runs', axis=1)
    predictions_today = forest_final.predict(predict_features)
    today['predicted.runs'] = predictions_today

    errors = labels - predictions
    total_var = labels - np.mean(labels)
    SSE = np.sum(np.power(errors, 2))
    SST = np.sum(np.power(total_var, 2))
    RMSE = math.sqrt(SSE / len(features))
    RSQ = 1 - SSE / SST
    print("The tuned model from ", month, "-", day, " using all available variables has RMSE = ", RMSE, sep="")
    print("The tuned model from ", month, "-", day, " using all available variables has R-Squared = ", RSQ, sep="")
    print()

    return today


def user_input_lines_and_results(today):

    import numpy as np
    bookie = []
    outcome = []
    print(today)
    for game in range(today.shape[0]):
        print()
        q = "Enter bookie line for " + today.iloc[game, 0] + " vs " + today.iloc[game, 1] + ": "
        bookie.append(float(input(q)))
        a = "Enter runs scored for " + today.iloc[game, 0] + " vs " + today.iloc[game, 1] + ": "
        outcome.append(float(input(a)))

    today['bookie'] = bookie
    today['outcome'] = outcome
    today['predicted.run.rank'] = today['predicted.runs'].rank()
    today['predicted.bookie.rank'] = today['bookie'].rank()
    today['the.bet'] = np.where(today['predicted.run.rank'] - today['predicted.bookie.rank'] >= 0, 'OVER', 'UNDER')
    today['betting.opportunity'] = abs(today['predicted.run.rank'] - today['predicted.bookie.rank'])

    condition_list = [today["outcome"] > today["bookie"],
                      today["outcome"] < today["bookie"],
                      today["outcome"] == today["bookie"]]
    choice_list = ["OVER", "UNDER", "PUSH"]
    today['game.result'] = np.select(condition_list, choice_list)

    condition_list2 = [today["the.bet"] == today["game.result"],
                       (today["the.bet"] != today["game.result"]) & (today["game.result"] != "PUSH"),
                       today["game.result"] == "PUSH"]
    choice_list2 = [100, -100, 0]

    today['bet.result'] = np.select(condition_list2, choice_list2)

    today.sort_values(by=['betting.opportunity'], ascending=False, inplace=True)

    return today


def user_input_lines(today):
    import numpy as np
    bookie = []
    print(today)
    for game in range(today.shape[0]):
        print()
        q = "Enter bookie line for " + today.iloc[game, 0] + " vs " + today.iloc[game, 1] + ": "
        bookie.append(float(input(q)))

    today['bookie'] = bookie
    today['predicted.run.rank'] = today['predicted.runs'].rank()
    today['predicted.bookie.rank'] = today['bookie'].rank()
    today['the.bet'] = np.where(today['predicted.run.rank'] - today['predicted.bookie.rank'] >= 0, 'OVER', 'UNDER')
    today['betting.opportunity'] = abs(today['predicted.run.rank'] - today['predicted.bookie.rank'])
    today.sort_values(by=['betting.opportunity'], ascending=False, inplace=True)

    return today
