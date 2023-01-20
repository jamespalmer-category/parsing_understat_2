import pandas as pd
from typing import List

def calc_cumulative_stats(team_data_dict: dict, col_list : List) -> dict:
    """
    params
    :team_data_dict: The dictionary of teams and their dfs which we want to find cumulative stats of
    :col_list: The list of column names we want to find cumulative statistics of

    outputs
    team_data_dict with the data having cumulative stats 

    Gets us the cumulative sums of whichever columns we want
    """
    for team in list(team_data_dict.keys()):
        team_df = team_data_dict[team]
        for col in team_df.columns:
            if col in col_list:
                team_df[col + ' cum'] = team_df[col].cumsum()
        team_data_dict[team] = team_df

    return team_data_dict

def put_game_data_in_team_data(team_dict_data: dict, game_df: pd.DataFrame) -> dict:
    """
    params
    :team_data_dict: The dictionary of teams and their dfs
    :game_df: The table of games from the season

    outputs
    team_data_dict with the individual game data for each team

    Gets us the game data from each game and appends it to each df in our dictionary
    """
    for team in list(team_dict_data.keys()):
        team_df = team_dict_data[team]

        rows_to_drop = []
        for i in range(0, len(game_df)):
            if (game_df['Home Team'][i] != team and game_df['Away Team'][i] != team):
                rows_to_drop.append(i)
        Team_Games = game_df.drop(rows_to_drop)

        Team_Opps = []
        Prob_Win = []
        Prob_Draw = []
        Prob_Lose = []

        for i in list(Team_Games.index):

            if game_df['Home Team'][i] != team:
                Team_Opps.append(game_df['Home Team'][i])
                Prob_Win.append(game_df['Probability Away Win'][i])
                Prob_Draw.append(game_df['Probability Draw'][i])
                Prob_Lose.append(game_df['Probability Home Win'][i])
                
            else:
                Team_Opps.append(game_df['Away Team'][i])
                Prob_Win.append(game_df['Probability Home Win'][i])
                Prob_Draw.append(game_df['Probability Draw'][i])
                Prob_Lose.append(game_df['Probability Away Win'][i])
                

        team_df['Opponent'] = Team_Opps
        team_df['Prob Win'] = Prob_Win
        team_df['Prob Draw'] = Prob_Draw
        team_df['Prob Lose'] = Prob_Lose

        team_dict_data[team] = team_df

    return team_dict_data

def rolling_form_stats(team_dict_data : dict, n : int, form_list : List) -> dict:
    """
    params
    :team_data_dict: The dictionary of teams and their dfs which we want to find form stats of
    :n: number of previous games we want to count
    :form_list: The list of column names we want to find form statistics of

    outputs
    team_data_dict with the data having form stats 

    Gets us rolling form stats for columns that we want
    """
    #Getting stats for form of all the teams
    for team in list(team_dict_data.keys()):
        team_df = team_dict_data[team]

        for col in form_list:
            team_df[col + ' in last ' + str(n)] = team_df[col].rolling(min_periods=1, window=n).sum()
        
        team_dict_data[team] = team_df

    return team_dict_data

def get_opposition_team_data(team_dict_data : dict) -> dict:
    """
    params
    :team_data_dict: The dictionary of teams and their dfs which we want to find cumulative stats of

    outputs
    team_data_dict with the stats of the opposition leading up to the game.

    Get us the data from the opposing team for each game and appends it to the dataframe.
    """
    for team in list(team_dict_data.keys()):
        team_df = team_dict_data[team]

        #Make first row have 0s coz the teams haven't played yet (this season...)
        df_new = pd.DataFrame(index = [0], columns=team_df.columns)
        df_new = df_new.fillna(0)
        # Making a dataframe which has the OPP data from the previous gameweek - BUG HERE
        for i in range(1, len(list(team_df['Opponent']))):
            opp_df = team_dict_data[team_df['Opponent'][i]]
            opp_last_game = opp_df.iloc[i-1].to_frame()
            opp_last_gameT = opp_last_game.T
            df_new = pd.concat([df_new, opp_last_gameT], ignore_index=True)
        #Making new columns and adding them to the dataframe

        #check the columns!
        opp_dict = {team_df.columns[i]: ['Opp' + col for col in team_df.columns][i] for i in range(len(team_df.columns))}
        df_new.rename(columns = opp_dict, inplace = True)
        df_new = pd.concat([team_df, df_new], axis = 1)
        team_dict_data[team] = df_new
    
    return team_dict_data