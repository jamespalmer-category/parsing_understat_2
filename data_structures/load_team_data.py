import pandas as pd
import json

def team_dict_to_df(team_dict : dict) -> dict:
    """
    params
    :game_dict: Our dictionary with key 'Team data'

    target
    :df: DataFrame with some cleaner data from our dictionary

    Encode/decode the team data to give us a list of dictionaries,
    We then clean up each dictionary and create a dataframe out of
    them all.
    """

    #Fix the dictionary up to make a dataframe
    team_data = team_dict['Team data']
    for key in list(team_data.keys()):
        team_data[team_data[key]['title']] = team_data[key]
        del team_data[key]
    for team in list(team_data.keys()):
        team_data[team] = team_data[team]['history']

    team_data_dict = {}
    for team in list(team_data.keys()):

        #the dictionaries all represent games, hence we call these games again.
        team_df = pd.DataFrame()
        for game in team_data[team]:

            #Rename titles found within our json.
            game['ppda att'] = game['ppda']['att']
            game['ppda def'] = game['ppda']['def']
            game['ppda allowed att'] = game['ppda_allowed']['att']
            game['ppda allowed def'] = game['ppda_allowed']['def']

            #delete entries we no longer need
            del game['ppda']
            del game['ppda_allowed']

            #add to main df
            team_df = pd.concat([team_df, pd.DataFrame.from_dict([game])], axis = 0)

        team_data_dict[team] = team_df

    return team_data_dict