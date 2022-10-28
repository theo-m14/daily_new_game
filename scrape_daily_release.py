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
    def getAllGame():
        url = 'https://www.millenium.org/guide/111787.html'
        response = requests.get(url)
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')
        filter_html = soup.find_all('li', attrs={'class' : 'article__ulist-item'})
        return GameReleaseScraper.filterGame(filter_html)

    @staticmethod
    def getGamePerDay(required_day):
        month_in_string = get_month_in_string()
        all_game = GameReleaseScraper.getAllGame()
        game_this_day = []
        for game in all_game:
            if required_day in game.date and month_in_string in game.date:
                game_this_day.append(game)
        return game_this_day

    @staticmethod
    def getGameNextWeek():
        month_in_string = get_month_in_string()
        all_game = GameReleaseScraper.getAllGame()
        game_this_week = []
        today = datetime.now().day
        for game in all_game:
            if game.date[0:2].isnumeric():
                game_day = int(game.date[0:2])
            else:
                '''At maximum day are 31 so 38 jump next condition'''
                game_day = 38
            if game_day < today + 7 and game_day >= today and month_in_string in game.date:
                game_this_week.append(game)
        return game_this_week
        
    @staticmethod
    def getGameActualMonth():
        month_in_string = get_month_in_string()
        all_game = GameReleaseScraper.getAllGame()
        game_this_month = []
        for game in all_game:
            if month_in_string in game.date:
               game_this_month.append(game)
        return game_this_month
