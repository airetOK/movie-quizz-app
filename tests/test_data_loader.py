import json
from typing import List

from model.movie import Movie


class TestDataLoader:

    __TEST_MOVIES_DATA_FILEPATH = "tests/test_data_movies.json"

    def get_movies(self) -> List[Movie]:
        with open(self.__TEST_MOVIES_DATA_FILEPATH, 'r') as f:
            data = json.load(f)
        return [Movie(obj['id'], obj['title']) for obj in data]
