from abc import ABC, abstractmethod
from model.game import Game


class GameService(ABC):

    @abstractmethod
    def generate_game(self) -> Game:
        pass

    @abstractmethod
    def verify(self, game: Game):
        pass
