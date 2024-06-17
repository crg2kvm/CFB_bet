import cfbd
api_key = 'MC/a7S2MZGhbO3j+PqUgCUnkK4yuSH+DhAxoi7kSLBF3+Wrt5N2QY8uFQ/OvsPW/'
configuration = cfbd.Configuration()
configuration.api_key['Authorization'] = api_key
configuration.api_key_prefix['Authorization'] = 'Bearer'
api_games = cfbd.GamesApi(cfbd.ApiClient(configuration))
api_teams= cfbd.TeamsApi(cfbd.ApiClient(configuration))
api_betting = cfbd.BettingApi(cfbd.ApiClient(configuration))
class Data:
    api_key = 'MC/a7S2MZGhbO3j+PqUgCUnkK4yuSH+DhAxoi7kSLBF3+Wrt5N2QY8uFQ/OvsPW/'
    configuration = cfbd.Configuration()
    configuration.api_key['Authorization'] = api_key
    configuration.api_key_prefix['Authorization'] = 'Bearer'
    api_games = cfbd.GamesApi(cfbd.ApiClient(configuration))
    api_teams= cfbd.TeamsApi(cfbd.ApiClient(configuration))
    api_betting = cfbd.BettingApi(cfbd.ApiClient(configuration))


    def bettingLines(game_id):
        """
        :param game_id: game id of individual game
        :return favorite: betting favorite
        :return total: actual total points scored in game
        :return point_diff: actual point differential of game
        :return over_under: pregame over under line
        :return spread: pregame spread line
        """
        betting_data = api_betting.get_lines(game_id=game_id)[0].to_dict()
        total= betting_data['home_score'] + betting_data['away_score']
        favorite = betting_data['lines'][3]['formatted_spread'].split(' -')[0]
        point_diff=abs(betting_data['home_score']-betting_data['away_score'])
        over_under = betting_data['lines'][3]['over_under']
        spread = betting_data['lines'][3]['spread']
        return  favorite, total, point_diff, over_under, spread