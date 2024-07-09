from unittest.mock import patch, Mock, MagicMock
import pytest

from app import app as flask_app
from tests.sample_data import mock_quizzes, mock_movies, mock_game
from service.quizz_service_impl import QuizzServiceImpl
from service.movie_service_impl import MovieServiceImpl
from service.game_service_impl import GameServiceImpl


@pytest.fixture()
def app():
    app = flask_app
    app.config.update({
        "TESTING": True,
    })

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_main_menu(client):
    response = client.get("/")
    assert 200 == response.status_code


def test_start_game(client):
    with patch.object(GameServiceImpl, "generate_game", return_value=MagicMock()) as mock_generate_game:
        response = client.get("/start")

    mock_generate_game.assert_called_once
    assert 200 == response.status_code


def test_verify_game_all_answers_correct(client):
    with patch.object(GameServiceImpl, "generate_game", return_value=mock_game) as mock_generate_game:
        response_start = client.get("/start")
        response_verify = client.post(f"/game/{mock_game.get_id()}/verify",
                                      data={'correct-answers': ['1-2-3-4-5']})
    mock_generate_game.assert_called_once
    assert 200 == response_start.status_code
    assert 200 == response_verify.status_code
    assert b'5\n' in response_verify.data


def test_verify_game_2_answers_correct(client):
    with patch.object(GameServiceImpl, "generate_game", return_value=mock_game) as mock_generate_game:
        response_start = client.get("/start")
        response_verify = client.post(f"/game/{mock_game.get_id()}/verify",
                                      data={'correct-answers': ['1-2-777-777-777']})
    mock_generate_game.assert_called_once
    assert 200 == response_start.status_code
    assert 200 == response_verify.status_code
    assert b'2\n' in response_verify.data


def test_verify_game_none_answers_correct(client):
    with patch.object(GameServiceImpl, "generate_game", return_value=mock_game) as mock_generate_game:
        response_start = client.get("/start")
        response_verify = client.post(f"/game/{mock_game.get_id()}/verify",
                                      data={'correct-answers': ['777-777-777-777-777']})
    mock_generate_game.assert_called_once
    assert 200 == response_start.status_code
    assert 200 == response_verify.status_code
    assert b'0\n' in response_verify.data


def test_new_quizz(client):
    response = client.get("/quizz")
    assert 200 == response.status_code


def test_5_positive_quizzes(client):
    movie_service = MovieServiceImpl(Mock())
    movie_service.get_five_random_movies = Mock(return_value=mock_movies)

    for index in range(len(mock_quizzes)):
        quizz = mock_quizzes[index]
        with patch.object(QuizzServiceImpl, "generate_quizz", return_value=quizz) as mock_generate_quizz:
            response_quizz = client.get("/quizz")
            response_verify = client.post(f"/quizz/{quizz.get_id()}/verify",
                                          data={'option_movie_id': quizz.get_correct_movie_id()})

        movie_service.get_five_random_movies.assert_called_once
        mock_generate_quizz.assert_called_once
        assert 200 == response_quizz.status_code
        assert 200 == response_verify.status_code
        assert b'<i class="fa fa-check-circle fa-5x" aria-hidden="true"></i>' in response_verify.data


def test_3_positive_quizzes_2_negative_quizzes(client):
    movie_service = MovieServiceImpl(Mock())
    movie_service.get_five_random_movies = Mock(return_value=mock_movies)

    for index in range(3):
        quizz = mock_quizzes[index]
        with patch.object(QuizzServiceImpl, "generate_quizz", return_value=quizz) as mock_generate_quizz:
            response_quizz = client.get("/quizz")
            response_verify = client.post(f"/quizz/{quizz.get_id()}/verify",
                                          data={'option_movie_id': quizz.get_correct_movie_id()})

        movie_service.get_five_random_movies.assert_called_once
        mock_generate_quizz.assert_called_once
        assert 200 == response_quizz.status_code
        assert 200 == response_verify.status_code
        assert b'<i class="fa fa-check-circle fa-5x" aria-hidden="true"></i>' in response_verify.data

    for index in range(2):
        quizz = mock_quizzes[index]
        with patch.object(QuizzServiceImpl, "generate_quizz", return_value=quizz) as mock_generate_quizz:
            response_quizz = client.get("/quizz")
            response_verify = client.post(f"/quizz/{quizz.get_id()}/verify",
                                          data={'option_movie_id': 'wrong_option_id'})

        movie_service.get_five_random_movies.assert_called_once
        mock_generate_quizz.assert_called_once
        assert 200 == response_quizz.status_code
        assert 200 == response_verify.status_code
        assert b'<i class="fa fa-times fa-5x" aria-hidden="true"></i>' in response_verify.data


def test_3_negative_quizzes_2_positive_quizzes(client):
    movie_service = MovieServiceImpl(Mock())
    movie_service.get_five_random_movies = Mock(return_value=mock_movies)

    for index in range(3):
        quizz = mock_quizzes[index]
        with patch.object(QuizzServiceImpl, "generate_quizz", return_value=quizz) as mock_generate_quizz:
            response_quizz = client.get("/quizz")
            response_verify = client.post(f"/quizz/{quizz.get_id()}/verify",
                                          data={'option_movie_id': 'wrong_option_id'})

        movie_service.get_five_random_movies.assert_called_once
        mock_generate_quizz.assert_called_once
        assert 200 == response_quizz.status_code
        assert 200 == response_verify.status_code
        assert b'<i class="fa fa-times fa-5x" aria-hidden="true"></i>' in response_verify.data

    for index in range(2):
        quizz = mock_quizzes[index]
        with patch.object(QuizzServiceImpl, "generate_quizz", return_value=quizz) as mock_generate_quizz:
            response_quizz = client.get("/quizz")
            response_verify = client.post(f"/quizz/{quizz.get_id()}/verify",
                                          data={'option_movie_id': quizz.get_correct_movie_id()})

        movie_service.get_five_random_movies.assert_called_once
        mock_generate_quizz.assert_called_once
        assert 200 == response_quizz.status_code
        assert 200 == response_verify.status_code
        assert b'<i class="fa fa-check-circle fa-5x" aria-hidden="true"></i>' in response_verify.data


def test_5_negative_quizzes(client):
    movie_service = MovieServiceImpl(Mock())
    movie_service.get_five_random_movies = Mock(return_value=mock_movies)

    for index in range(len(mock_quizzes)):
        quizz = mock_quizzes[index]
        with patch.object(QuizzServiceImpl, "generate_quizz", return_value=quizz) as mock_generate_quizz:
            response_quizz = client.get("/quizz")
            response_verify = client.post(f"/quizz/{quizz.get_id()}/verify",
                                          data={'option_movie_id': 'wrong_option_id'})

        movie_service.get_five_random_movies.assert_called_once
        mock_generate_quizz.assert_called_once
        assert 200 == response_quizz.status_code
        assert 200 == response_verify.status_code
        assert b'<i class="fa fa-times fa-5x" aria-hidden="true"></i>' in response_verify.data
