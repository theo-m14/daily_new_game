from datetime import datetime

import requests
from bs4 import BeautifulSoup

from utils import get_month_in_string, has_numbers


def get_game_today():
    url = 'https://www.millenium.org/guide/111787.html'

    response = requests.get(url)

    html = response.content

    soup = BeautifulSoup(html, 'html.parser')

    all_game_release = soup.find_all('li', attrs={'class' : 'article__ulist-item'})

    month_in_string = get_month_in_string()
    day = str(datetime.now().day)

    game_string = ''
    for game in all_game_release:
        game = game.get_text(strip=True) 
        if ':' in game and '-' in game and has_numbers(game):
            if month_in_string in game and day in game:
                game_string += game + '\n'
                
    if game_string == '':
        return "Pas de jeu aujourd'hui"
    return game_string


