import pytest
from unittest.mock import Mock

from model.game import Game
from model.game_result import GameResult
from tests.sample_data import mock_movies, mock_quizzes
from client.movie_api_client import MovieApiClient
from service.movie_service_impl import MovieServiceImpl
from service.quizz_service_impl import QuizzServiceImpl
from service.game_service_impl import GameServiceImpl


@pytest.fixture()
def mock_quizz_service():
    movie_api_client = MovieApiClient()
    movie_api_client.get_top_rated_movies = Mock(return_value=mock_movies*4)
    movie_api_client.get_image_url_by_movie_id = Mock(
        return_value="/test_image_path.jpg")
    movie_service = MovieServiceImpl(movie_api_client)
    return QuizzServiceImpl(movie_service)


def test_generate_game(mock_quizz_service):
    game_service = GameServiceImpl(mock_quizz_service)
    game = game_service.generate_game()
    assert Game == type(game)
    assert 10 == len(game.get_quizzes())


def test_verify_game_all_correct_answers(mock_quizz_service):
    game_service = GameServiceImpl(mock_quizz_service)
    game_result = game_service.verify(mock_quizzes, ['1', '2', '3', '4', '5'])
    assert GameResult == type(game_result)
    assert 5 == game_result.get_total_amount()
    assert 5 == game_result.get_correct_answers()


def test_verify_game_all_incorrect_answers(mock_quizz_service):
    game_service = GameServiceImpl(mock_quizz_service)
    game_result = game_service.verify(mock_quizzes, ['5', '4', '2', '2', '1'])
    assert GameResult == type(game_result)
    assert 5 == game_result.get_total_amount()
    assert 0 == game_result.get_correct_answers()


def test_verify_game_3_correct_answers(mock_quizz_service):
    game_service = GameServiceImpl(mock_quizz_service)
    game_result = game_service.verify(mock_quizzes, ['1', '7', '3', '7', '5'])
    assert GameResult == type(game_result)
    assert 5 == game_result.get_total_amount()
    assert 3 == game_result.get_correct_answers()
