from flask import session
from unittest.mock import patch, MagicMock
import pytest

from app import app as flask_app
from tests.sample_data import mock_quizzes, mock_game
from service.quizz_service_impl import QuizzServiceImpl
from service.game_service_impl import GameServiceImpl


@pytest.fixture()
def client():
    flask_app.config.update({
        "TESTING": True,
        "DEBUG": False
    })
    with flask_app.test_client() as client:
        with client.session_transaction() as session:
            session.clear()
        yield client


def test_main_menu(client):
    response = client.get("/")
    assert session["correct_answers"] == 0
    assert session["total_quizzes"] == 0
    assert 200 == response.status_code


def test_start_game(client):
    with patch.object(GameServiceImpl, "generate_game", return_value=MagicMock()) as mock_generate_game:
        response = client.get("/start")

    mock_generate_game.assert_called_once()
    assert 200 == response.status_code


def test_verify_game_all_answers_correct(client):
    with patch.object(GameServiceImpl, "generate_game", return_value=mock_game) as mock_generate_game:
        response_start = client.get("/start")
        response_verify = client.post(f"/game/{mock_game.get_id()}/verify",
                                      data={'correct-answers': ['1-2-3-4-5']})

    mock_generate_game.assert_called_once()
    assert 200 == response_start.status_code
    assert 200 == response_verify.status_code
    assert b'5\n' in response_verify.data


def test_verify_game_2_answers_correct(client):
    with patch.object(GameServiceImpl, "generate_game", return_value=mock_game) as mock_generate_game:
        response_start = client.get("/start")
        response_verify = client.post(f"/game/{mock_game.get_id()}/verify",
                                      data={'correct-answers': ['1-2-777-777-777']})

    mock_generate_game.assert_called_once()
    assert 200 == response_start.status_code
    assert 200 == response_verify.status_code
    assert b'2\n' in response_verify.data


def test_verify_game_none_answers_correct(client):
    with patch.object(GameServiceImpl, "generate_game", return_value=mock_game) as mock_generate_game:
        response_start = client.get("/start")
        response_verify = client.post(f"/game/{mock_game.get_id()}/verify",
                                      data={'correct-answers': ['777-777-777-777-777']})

    mock_generate_game.assert_called_once()
    assert 200 == response_start.status_code
    assert 200 == response_verify.status_code
    assert b'0\n' in response_verify.data


def test_new_quizz(client):
    with patch.object(QuizzServiceImpl, "generate_quizz", return_value=MagicMock()) as mock_generate_quizz:
        response = client.get("/quizz")

    mock_generate_quizz.assert_called_once()
    assert 200 == response.status_code


def test_5_positive_quizzes(client):
    for index in range(len(mock_quizzes)):
        quizz = mock_quizzes[index]
        with patch.object(QuizzServiceImpl, "generate_quizz", return_value=quizz) as mock_generate_quizz:
            response_quizz = client.get("/quizz")
            response_verify = client.post(f"/quizz/{quizz.get_id()}/verify",
                                          data={'option_movie_id': quizz.get_correct_movie_id()})

        mock_generate_quizz.assert_called_once()
        assert 200 == response_quizz.status_code
        assert 200 == response_verify.status_code
        assert b'<i class="fa fa-check-circle fa-5x" aria-hidden="true"></i>' in response_verify.data

    assert session["correct_answers"] == 5
    assert session["total_quizzes"] == 5


def test_3_positive_quizzes_2_negative_quizzes(client):
    for index in range(3):
        quizz = mock_quizzes[index]
        with patch.object(QuizzServiceImpl, "generate_quizz", return_value=quizz) as mock_generate_quizz:
            response_quizz = client.get("/quizz")
            response_verify = client.post(f"/quizz/{quizz.get_id()}/verify",
                                          data={'option_movie_id': quizz.get_correct_movie_id()})

        mock_generate_quizz.assert_called_once()
        assert 200 == response_quizz.status_code
        assert 200 == response_verify.status_code
        assert b'<i class="fa fa-check-circle fa-5x" aria-hidden="true"></i>' in response_verify.data

    for index in range(2):
        quizz = mock_quizzes[index]
        with patch.object(QuizzServiceImpl, "generate_quizz", return_value=quizz) as mock_generate_quizz:
            response_quizz = client.get("/quizz")
            response_verify = client.post(f"/quizz/{quizz.get_id()}/verify",
                                          data={'option_movie_id': 'wrong_option_id'})

        assert 200 == response_quizz.status_code
        assert 200 == response_verify.status_code
        assert b'<i class="fa fa-times fa-5x" aria-hidden="true"></i>' in response_verify.data

    assert session["correct_answers"] == 3
    assert session["total_quizzes"] == 5


def test_3_negative_quizzes_2_positive_quizzes(client):
    for index in range(3):
        quizz = mock_quizzes[index]
        with patch.object(QuizzServiceImpl, "generate_quizz", return_value=quizz) as mock_generate_quizz:
            response_quizz = client.get("/quizz")
            response_verify = client.post(f"/quizz/{quizz.get_id()}/verify",
                                          data={'option_movie_id': 'wrong_option_id'})

        mock_generate_quizz.assert_called_once()
        assert 200 == response_quizz.status_code
        assert 200 == response_verify.status_code
        assert b'<i class="fa fa-times fa-5x" aria-hidden="true"></i>' in response_verify.data

    for index in range(2):
        quizz = mock_quizzes[index]
        with patch.object(QuizzServiceImpl, "generate_quizz", return_value=quizz) as mock_generate_quizz:
            response_quizz = client.get("/quizz")
            response_verify = client.post(f"/quizz/{quizz.get_id()}/verify",
                                          data={'option_movie_id': quizz.get_correct_movie_id()})

        mock_generate_quizz.assert_called_once()
        assert 200 == response_quizz.status_code
        assert 200 == response_verify.status_code
        assert b'<i class="fa fa-check-circle fa-5x" aria-hidden="true"></i>' in response_verify.data

    assert session["correct_answers"] == 2
    assert session["total_quizzes"] == 5


def test_5_negative_quizzes(client):
    for index in range(len(mock_quizzes)):
        quizz = mock_quizzes[index]
        with patch.object(QuizzServiceImpl, "generate_quizz", return_value=quizz) as mock_generate_quizz:
            response_quizz = client.get("/quizz")
            response_verify = client.post(f"/quizz/{quizz.get_id()}/verify",
                                          data={'option_movie_id': 'wrong_option_id'})

        mock_generate_quizz.assert_called_once()
        assert 200 == response_quizz.status_code
        assert 200 == response_verify.status_code
        assert b'<i class="fa fa-times fa-5x" aria-hidden="true"></i>' in response_verify.data

    assert session["correct_answers"] == 0
    assert session["total_quizzes"] == 5
