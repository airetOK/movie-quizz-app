import pytest
from service.session_handler import SessionHandler
from flask import session
from app import app as flask_app


@pytest.fixture(autouse=True)
def session_handler():
    with flask_app.test_request_context():
        session_handler = SessionHandler()
        session.clear()
        session_handler.initialize()
        yield session_handler


def test_check_initialized_session():
    assert session["correct_answers"] == 0
    assert session["total_quizzes"] == 0


@pytest.mark.parametrize("is_correct", [True])
def test_store_correct_quizz_result(session_handler, is_correct):
    session_handler.store_quizz_result(is_correct)

    assert session["total_quizzes"] == 1
    assert session["correct_answers"] == 1


@pytest.mark.parametrize("is_correct", [False])
def test_store_incorrect_quizz_result(session_handler, is_correct):
    session_handler.store_quizz_result(is_correct)

    assert session["total_quizzes"] == 1
    assert session["correct_answers"] == 0


@pytest.mark.parametrize("is_correct", [True])
def test_get_data(session_handler, is_correct):
    session_handler.store_quizz_result(is_correct)
    session_data = session_handler.get_data()

    assert session_data["total_quizzes"] == 1
    assert session["correct_answers"] == 1
