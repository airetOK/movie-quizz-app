import pytest
from unittest.mock import Mock, patch

from service.quizz_service_impl import QuizzServiceImpl
from model.quizz import Quizz
from tests.test_data_loader import TestDataLoader

__data_loader = TestDataLoader()


@pytest.fixture()
def test_data_movies():
    return __data_loader.get_movies()


@pytest.fixture()
def mock_movie_service():
    with (patch('client.movie_api_client.MovieApiClient') as MockMovieApiClient,
          patch('service.movie_service_impl.MovieServiceImpl') as MockMovieService):
        mock_movie_api_client = MockMovieApiClient.return_value
        mock_movie_service = MockMovieService(mock_movie_api_client).return_value
        yield mock_movie_service


@patch('uuid.uuid4', return_value="mock_id")
@patch('random.randint', return_value=3)
def test_generate_quizz(mock_uuid, mock_randint, test_data_movies, mock_movie_service):
    mock_movie_service.get_five_random_movies = Mock(return_value=test_data_movies)
    quizz_service = QuizzServiceImpl(mock_movie_service)
    quizz = quizz_service.generate_quizz()

    mock_randint.assert_called_once()
    mock_uuid.assert_called_once()
    mock_movie_service.get_five_random_movies.assert_called_once()
    assert type(quizz) == Quizz
    assert quizz.get_id() == "mock_id"
    assert quizz.get_correct_movie_id() == "4"
    assert len(quizz.get_shuffled_option_movies()) == 5


@patch('random.randint', return_value=2)
def test_verify_quizz(mock_randint, test_data_movies, mock_movie_service):
    mock_movie_service.get_five_random_movies = Mock(return_value=test_data_movies)
    quizz_service = QuizzServiceImpl(mock_movie_service)
    quizz = quizz_service.generate_quizz()

    mock_randint.assert_called_once()
    mock_movie_service.get_five_random_movies.assert_called_once()
    assert quizz_service.verify_quizz("3", quizz)
    assert not quizz_service.verify_quizz("2", quizz)


def test_load_quizzes(test_data_movies, mock_movie_service):
    mock_movie_service.get_five_random_movies = Mock(return_value=test_data_movies * 3)
    quizz_service = QuizzServiceImpl(mock_movie_service)
    quizzes = quizz_service.load_quizzes(count=10)

    assert mock_movie_service.get_five_random_movies.call_count == 10
    assert len(quizzes) == 10
