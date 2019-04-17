def clean_todays_data(data, month, day):

    import pickle

    data['home.win.pct'] = data['game.home.win'] / (data['game.home.win'] + data['game.home.loss'])
    data['away.win.pct'] = data['game.away.win'] / (data['game.away.win'] + data['game.away.loss'])
    data['home.pitcher.win.pct'] = data['game.home.probable_pitcher.win'] / (
                data['game.home.probable_pitcher.win'] + data['game.home.probable_pitcher.loss'])
    data['away.pitcher.win.pct'] = data['game.away.probable_pitcher.win'] / (
                data['game.away.probable_pitcher.win'] + data['game.away.probable_pitcher.loss'])
    data['total.runs'] = data['game.home.runs'] + data['game.away.runs']  # Response variable!

    # I feel like this is unnecessary ^^^^^^^^^^^^^^^^^
    with open('outfile_april_12_pre', 'rb') as fp:
        baseball_data1 = pickle.load(fp)

    data_all_cols = list(data.columns.values)
    data_good_cols = list(baseball_data1.columns.values)
    data_good_cols.append('home.win.pct')
    data_good_cols.append('away.win.pct')
    data_good_cols.append('home.pitcher.win.pct')
    data_good_cols.append('away.pitcher.win.pct')
    data_good_cols.append('total.runs')
    data = data.drop(list(set(data_all_cols) - set(data_good_cols)), axis=1)
    # data contains only the 67 variables available before today's MLB games start
    # Unnecessary down to here ^^^^^^^^^^^^^^^^^^^

    # Must drop additional variables will not know before game starts
    data = data.drop(['game.away.errors', 'game.away.hits', 'game.away.runs',
                      'game.home.errors', 'game.home.hits', 'game.home.runs'], axis=1)

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

    data['game.weather.forecast.condition'].fillna('unknown', inplace=True)
    data['game.weather.forecast.wind.direction'].fillna('unknown', inplace=True)
    data['game.venue.field_orientation'].fillna('unknown', inplace=True)
    data['game.venue.stadium_type'].fillna('unknown', inplace=True)

    # Weather data simplified
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

    data.dropna(axis=0, inplace=True)

    with open('./daily_data/outfile_{0}_{1}_pre'.format(month, day), 'wb') as fp:
        pickle.dump(data, fp)

    return None


