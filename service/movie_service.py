from abc import ABC, abstractmethod

class MovieService(ABC):

    @abstractmethod
    def get_five_random_movies(self):
        pass
