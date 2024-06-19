import cfbd
api_key = 'MC/a7S2MZGhbO3j+PqUgCUnkK4yuSH+DhAxoi7kSLBF3+Wrt5N2QY8uFQ/OvsPW/'
configuration = cfbd.Configuration()
configuration.api_key['Authorization'] = api_key
configuration.api_key_prefix['Authorization'] = 'Bearer'
api_games = cfbd.GamesApi(cfbd.ApiClient(configuration))
api_teams= cfbd.TeamsApi(cfbd.ApiClient(configuration))
api_betting = cfbd.BettingApi(cfbd.ApiClient(configuration))
api_metrics = cfbd.MetricsApi(cfbd.ApiClient(configuration))
api_stats = cfbd.StatsApi(cfbd.ApiClient(configuration))
api_ratings = cfbd.RatingsApi(cfbd.ApiClient(configuration))
api_recruit = cfbd.RecruitingApi(cfbd.ApiClient(configuration))

class Data:  

#TODO: add winner to bettinglines function
    def bettingLines(game_id):
        """
        :param game_id: game id of individual game
        :return favorite: betting favorite
        :return total: actual total points scored in game
        :return point_diff: actual point differential of game
        :return over_under: pregame over under line
        :return spread: pregame spread line
        """
        try:
        # Attempt to retrieve betting data
            betting_data = api_betting.get_lines(game_id=game_id)[0].to_dict()
            
            # Extract necessary information
            total = betting_data['home_score'] + betting_data['away_score']
            favorite = betting_data['lines'][3]['formatted_spread'].split(' -')[0]
            point_diff = abs(betting_data['home_score'] - betting_data['away_score'])
            over_under = betting_data['lines'][3]['over_under']
            spread = betting_data['lines'][3]['spread']
            
            return favorite, total, point_diff, over_under, spread

        except (IndexError, KeyError):
            # Handle the case where betting data is not available or incomplete
            print("Error: Betting data is not available for this game.")
            return None
        


    def getWeeklyGames(year,week,division='fbs'):
        """
        :param year: year of data
        :param week: week of data
        :param division: division of data
        :return bettable_games: list of fbs games and info associated
        """
        keys_to_keep = ['id','season','week','start_date','neutral_site','attendance','venue_id','home_team','home_conference','home_points','home_pregame_elo','away_team','away_conference','away_points','away_pregame_elo']
        games = api_games.get_games(year=year,week=week,division=division)
        bettable_games = []
        for game in games:
            game = game.to_dict()     
            if game['away_division'] != 'fcs' and game['home_division'] != 'fcs':
                game=[{key: game[key] for key in keys_to_keep}]
                bettable_games.append(game)
        
        return bettable_games
    

    def flatten_dict(d, parent_key='', sep='_'):
        """
        Flattens dictionary i.e. removes nested dictionaries
        """
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)


    def getAdvancedSeasonStats(year,week,team):
        """
        Returns defensive advanced stats of team

        :param year: year of season
        :param week: week of season
        :param team: team that is wanted
        :return dat_def: advanced defensive statistics
        :return dat_off: advanced offensive statistics
        """
        dat = api_stats.get_advanced_team_season_stats(year=year,team=team,start_week=1,end_week=week,exclude_garbage_time=True)[0].to_dict()
        dat_def = dat['defense']
        dat_off = dat['offense']
        keys_to_pop = ['total_ppa','line_yards_total','second_level_yards_total','open_field_yards_total','total_opportunies','rushing_plays_total_ppa','passing_plays_total_ppa']
        dat_def=flatten_dict(dat_def)
        dat_off=flatten_dict(dat_off)
        for key in keys_to_pop:
            dat_def.pop(key)
            dat_off.pop(key)
        return dat_def, dat_off
    
    
