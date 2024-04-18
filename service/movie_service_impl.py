from service.movie_service import MovieService
from client.movie_api_client import MovieApiClient
from model.movie import Movie
import random


class MovieServiceImpl(MovieService):

    def __init__(self, client: MovieApiClient):
        self.client = client

    def get_five_random_movies(self) -> list[Movie]:
        random_movies = []
        '''get one random movie per page'''
        for page in self.__get_random_pages_nums__():
            movie = self.client.get_top_rated_movies(page)[self.__get_random_movie_num__()]
            movie.set_image_url(self.client.get_image_url_by_movie_id(movie.get_id()))
            random_movies.append(movie)
        return random_movies

    def __get_random_movie_num__(self):
        '''MovieDB API includes 20 movies per page'''
        return random.randint(0, 19)
    
    def __get_random_pages_nums__(self) -> tuple:
        '''MovieDB API includes 465 pages with movies'''
        unique_pages = set()

        while len(unique_pages) != 5:
            unique_pages.add(random.randint(1, 465))

        return unique_pages