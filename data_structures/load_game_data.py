import pandas as pd
import json

def game_dict_to_df(game_dict : dict) -> pd.DataFrame:
    """
    params
    :game_dict: Our dictionary with key 'Game data'

    target
    :df: DataFrame with some cleaner data from our dictionary

    Encode/decode the game data to give us a list of dictionaries,
    We then clean up each dictionary and create a dataframe out of
    them all.
    """
    
    game_data = game_dict['Game data']

    df = pd.DataFrame()
    for game in game_data:

        #Rename titles found within our json.
        game['h'] = game['h']['title']
        game['a'] = game['a']['title']
        game['Home goals'] = game['goals']['h']
        game['Away goals'] = game['goals']['a']
        game['xG Home'] = game['xG']['h']
        game['xG Away'] = game['xG']['a']
        game['Probability Home Win'] = game['forecast']['w']
        game['Probability Draw'] = game['forecast']['d']
        game['Probability Away Win'] = game['forecast']['l']

        #delete entries we no longer need
        del game['goals']
        del game['xG']
        del game['forecast']

        #add to main df, NB we wrap game in square brackets else we get an error.
        df = pd.concat([df, pd.DataFrame.from_dict([game])], axis = 0, ignore_index = True)

    return df