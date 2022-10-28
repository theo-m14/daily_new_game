from datetime import datetime

import requests
from bs4 import BeautifulSoup

from utils import get_month_in_string, has_numbers

class Game():
    def __init__(self, name, platforms, date) -> None:
        self.date = date
        self.name = name
        self.platforms = platforms
        self.searchLink = 'https://www.google.com/search?q=' + name.replace(' ','') + '+jeu' 

    @staticmethod
    def convertStringToGame(string: str):
        name = string[0:string.rfind(':')]
        platforms = string[string.rfind(':')+2:string.rfind('-')-1]
        date = string[string.rfind('-')+2:len(string)]
        return Game(name,platforms,date)
    
    def __str__(self) -> str:
        return self.name + ' - Plateforme: ' + self.platforms + ' - Date de sortie: ' + self.date + " - Plus d'info : " + self.searchLink


class GameReleaseScraper():

    @staticmethod
    def filterGame(filter_html):
        all_game = []
        for game in filter_html:
            game = game.get_text(strip=True)
            if ':' in game and '-' in game and has_numbers(game):
                all_game.append(Game.convertStringToGame(game))
        return all_game

    @staticmethod
    def getGameToday():
        month_in_string = get_month_in_string()
        day = str(datetime.now().day)
        all_game = GameReleaseScraper.getAllGame()
        game_today = []
        for game in all_game:
            if day in game.date and month_in_string in game.date:
                game_today.append(game)
        if game_today != []:
            return game_today
        else:
            return ["Pas de jeu aujourd'hui"]

    @staticmethod
    def getAllGame():
        url = 'https://www.millenium.org/guide/111787.html'
        response = requests.get(url)
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')
        filter_html = soup.find_all('li', attrs={'class' : 'article__ulist-item'})
        return GameReleaseScraper.filterGame(filter_html)
