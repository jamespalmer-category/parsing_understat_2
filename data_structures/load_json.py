import requests
from bs4 import BeautifulSoup
import json
from typing import List


def get_understat_data(url: str) -> List:
    """
    params
    :url: string corresponding to the url of the understat page we want to parse

    outputs
    :List: list of json strings we get from the website

    Use bs4 and requests to get the json data that is on the webpage.
    We then need 
    """
    result = requests.get(url)
    src = result.content
    soup = BeautifulSoup(src, 'html.parser')
    json_data = soup.find_all("script")

    Game_Table_Player_data = []
    for json_string in json_data[1:4]:
        """
        Convert the entry into a string, then find the first and last
        quotemarks as this finds our json, then put that into a list.
        """
        
        json_string = str(json_string)
        s_1 = json_string.find('\'')
        s_2 = json_string.rfind('\'')
        json_string = json_string[s_1:s_2 + 1]
        Game_Table_Player_data.append(json_string)

    return Game_Table_Player_data

def load_json(json_list : List) -> dict:
    """
    params
    :jason_list: A list of elements with json corresponding to game, team, player data

    outputs
    :dict: Dictionary with the uncoded json and what data it represents
    """
    return {['Game data', 'Team data', 'Player data'][i] : 
    json.loads(json_list[i].encode('ascii').decode('unicode-escape')[1:-1]) for i in range(len(json_list))}

if __name__ == "__main__":
    pl_2223 = get_understat_data('https://understat.com/league/EPL')
    pl_2223_json = load_json(pl_2223)
    print(pl_2223_json)