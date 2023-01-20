from data_structures.load_json import get_understat_data, load_json
from data_structures.load_game_data import game_dict_to_df
from data_structures.load_player_data import player_dict_to_df
from data_structures.load_team_data import team_dict_to_df

from config import URL, CUMSUM_LIST
from preprocessing.team_preprocessing import calc_cumulative_stats, put_game_data_in_team_data

#Get the json data into 3 lists of dictionaries
league_jsonstr_data = get_understat_data(URL)
league_gtp_data = load_json(league_jsonstr_data)

#Get the game, team, player data into a DataFrame
league_game_data = game_dict_to_df(league_gtp_data)
league_team_data = team_dict_to_df(league_gtp_data)
league_player_data = player_dict_to_df(league_gtp_data)


#Add the cumulative statistics
league_team_cum_added = calc_cumulative_stats(league_team_data, CUMSUM_LIST)

#Add the opposition teams
league_team_opps_added = put_game_data_in_team_data(league_team_cum_added, league_game_data)