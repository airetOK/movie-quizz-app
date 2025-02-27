from abc import ABC, abstractmethod
from model.movie import Movie
from model.quizz import Quizz


class QuizzService(ABC):

    @abstractmethod
    def generate_quizz(self, movies: list[Movie]):
        pass

    @abstractmethod
    def verify_quizz(self, option_movie_id: str, quizz: Quizz):
        pass

    @abstractmethod
    def load_quizzes(self, count: int = 10):
        pass

    @abstractmethod
    def get_unique_id(self):
        pass
