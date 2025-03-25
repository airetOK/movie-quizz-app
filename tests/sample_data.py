from model.movie import Movie
from model.quizz import Quizz
from model.game import Game

'''TO:DO remove this module, use test_data_loader.py for receiving sample data
(e.g. see test_quizz_service_impl.py)'''
mock_movies = [
    Movie(1, 'Harry Potter'),
    Movie(2, 'Lord of the Rings'),
    Movie(3, 'Scarface'),
    Movie(4, 'The Godfather'),
    Movie(5, 'Shrek'),
]

mock_quizzes = [
    Quizz('1', mock_movies[0], mock_movies[1],
          mock_movies[2], mock_movies[3], mock_movies[4]),
    Quizz('2', mock_movies[1], mock_movies[0],
          mock_movies[2], mock_movies[3], mock_movies[4]),
    Quizz('3', mock_movies[2], mock_movies[0],
          mock_movies[1], mock_movies[3], mock_movies[4]),
    Quizz('4', mock_movies[3], mock_movies[0],
          mock_movies[1], mock_movies[2], mock_movies[4]),
    Quizz('5', mock_movies[4], mock_movies[0],
          mock_movies[1], mock_movies[2], mock_movies[3])
]

mock_game = Game('1', mock_quizzes)
