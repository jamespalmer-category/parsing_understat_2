import pandas as pd
import json

def player_dict_to_df(player_dict : dict) -> pd.DataFrame:
    """
    params
    :game_dict: Our dictionary with key 'Player data'

    target
    :df: DataFrame with some cleaner data from our dictionary

    Encode/decode the player data to give us a list of dictionaries
    and create a dataframe out of them all.
    """
    
    player_data = player_dict['Player data']

    player_df = pd.DataFrame()
    for game in player_data:

        #add to main df, NB we wrap game in square brackets else we get an error.
        player_df = pd.concat([player_df, pd.DataFrame.from_dict([game])], axis = 0, ignore_index = True)

    return player_df