from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game, User
from games.adapters.datareader.csvdatareader import GameFileCSVReader
from bisect import insort_left
import os
from typing import List


class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__game = list()
        self.__users = set()
        self.__reviews = list()

    def add_game(self, game: Game):
        if isinstance(game, Game):
            insort_left(self.__game, game)

    def get_games(self) -> List[Game]:
        return self.__game

    def get_number_of_game(self):
        return len(self.__game)

    def get_game_by_title(self, name):
        for i in self.__game:
            if i.title == name:
                return i

    def add_user(self, user):
        self.__users.add(user)

    def get_user(self, username):
        for i in self.__users:
            if i.username == username:
                return i

    def add_review(self, review):
        game = self.get_game_by_title(review.game.title)
        user = self.get_user(review.user.username)
        game.add_review(review)
        user.add_review(review)

    def get_reviews_for_game(self, game_title):
        return [review for review in self.__reviews if review.game.title == game_title]

    def add_to_wishlist(self, username, game):
        user = self.get_user(username)
        if user:
            user.add_favourite_game(game)

    def remove_from_wishlist(self, username, game):
        user = self.get_user(username)
        if user:
            user.remove_favourite_game(game)

    def get_wishlist(self, username):
        user = self.get_user(username)
        if user:
            return user.favourite_games

    def is_in_wishlist(self, username, game):
        user = self.get_user(username)
        if user:
            return game in user.favourite_games
        return False


def populate(repo: AbstractRepository):
    dir_name = os.path.dirname(os.path.abspath(__file__))
    game_file_name = os.path.join(dir_name, "data/games.csv")
    reader = GameFileCSVReader(game_file_name)
    reader.read_csv_file()
    games = reader.dataset_of_games
    for game in games:
        repo.add_game(game)
