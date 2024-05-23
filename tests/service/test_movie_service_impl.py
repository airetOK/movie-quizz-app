import pytest
from unittest.mock import Mock

from model.movie import Movie
from tests.sample_data import mock_movies
from client.movie_api_client import MovieApiClient
from service.movie_service_impl import MovieServiceImpl


@pytest.fixture()
def mock_client():
    movie_api_client = MovieApiClient()
    movie_api_client.get_top_rated_movies = Mock(return_value=mock_movies*4)
    movie_api_client.get_image_url_by_movie_id = Mock(
        return_value="/test_image_path.jpg")
    return movie_api_client


def test_get_five_random_movies(mock_client):
    movie_service = MovieServiceImpl(mock_client)
    assert len(movie_service.get_five_random_movies()) == 5
    assert movie_service.get_five_random_movies(
    )[0].get_image_url() == "/test_image_path.jpg"
    assert isinstance(movie_service.get_five_random_movies()[4], Movie)
