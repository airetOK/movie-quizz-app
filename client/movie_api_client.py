import os
import httpx
import logging
from dotenv import load_dotenv
import json

from model.movie import Movie

logger = logging.getLogger(__name__)
load_dotenv()


class MovieApiClient():

    IMAGE_URL_TEMPLATE = 'https://image.tmdb.org/t/p/original{}'
    TOP_RATED_MOVIES_URL_TEMPLATE = 'https://api.themoviedb.org/3/movie/top_rated?page={}'
    MOVIE_IMAGES_URL_TEMPLATE = 'https://api.themoviedb.org/3/movie/{}/images'

    def __init__(self) -> None:
        self.auth_header = {'Authorization':
                            f'Bearer {os.getenv("API_ACCESS_TOKEN")}'}

    def get_top_rated_movies(self, page: int) -> list[Movie]:
        resp = httpx.get(self.TOP_RATED_MOVIES_URL_TEMPLATE.format(page),
                         headers=self.auth_header)
        logger.info(
            f'The status code for request to get top rated movies on the page {page} is {resp.status_code}')

        results = json.loads(resp.content)['results']
        return [Movie(movie['id'], movie['title']) for movie in results]

    def get_image_url_by_movie_id(self, id: str) -> str:
        resp = httpx.get(self.MOVIE_IMAGES_URL_TEMPLATE.format(id),
                         headers=self.auth_header)
        logger.info(
            f'The status code for request to get image by movie id "{id}" is {resp.status_code}')

        file_path = json.loads(resp.content)['backdrops'][0]['file_path']
        return self.IMAGE_URL_TEMPLATE.format(file_path)
