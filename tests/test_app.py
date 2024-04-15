from unittest.mock import Mock
from app import app as flask_app
import pytest

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


