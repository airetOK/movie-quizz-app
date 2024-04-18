from unittest.mock import patch, Mock
import pytest

from app import app as flask_app
from tests.sample_data import mock_quizzes, mock_movies
from service.quizz_service_impl import QuizzServiceImpl
from service.movie_service_impl import MovieServiceImpl


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
