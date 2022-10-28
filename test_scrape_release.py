#Class Game
#get name
import scrape_daily_release as scrape_release


class TestGame():
    
    game = scrape_release.Game('Mario', 'PC', '30 octobre')
    game_str = 'Mario: PC - 30 octobre'

    
    def test_get_date(self):
        assert self.game.date == '30 octobre'

    def test_get_name(self):
        assert self.game.name == 'Mario'

    def test_get_platorms(self):
        assert self.game.platforms == 'PC'

    def test_search_link(self):
        assert self.game.searchLink == 'https://www.google.com/search?q=Mario+jeu'

    def test_convert_string_to_game(self):
        test_game = scrape_release.Game.convertStringToGame(self.game_str)
        assert test_game.name == self.game.name and test_game.date == self.game.date and test_game.platforms == self.game.platforms


    def test_game_to_string(self):
        assert str(self.game) == "Mario - Plateformes: PC - Date de sortie: 30 octobre - Plus d'info : https://www.google.com/search?q=Mario+jeu"