from service.quizz_service import QuizzService
from model.movie import Movie
from model.quizz import Quizz
import random
import uuid


class QuizzServiceImpl(QuizzService):

    def generate_quizz(self, movies: list[Movie]) -> Quizz:
        quizz_id = self.get_unique_id()
        correct_movie = movies.pop(self.__get_random_num__())
        option_movie_1 = movies[0]
        option_movie_2 = movies[1]
        option_movie_3 = movies[2]
        option_movie_4 = movies[3]
        return Quizz(quizz_id, correct_movie, option_movie_1, option_movie_2, option_movie_3, option_movie_4)
    
    def verify_quizz(self, option_movie_id: str, quizz: Quizz) -> bool:
        return option_movie_id == quizz.get_correct_movie_id()

    def get_unique_id(self):
        return str(uuid.uuid4())

    def __get_random_num__(self):
        return random.randint(0, 4)