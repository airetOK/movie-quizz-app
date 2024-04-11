import random


class Quizz():

    QUESTION_TEMPLATE = "Which image belongs to \'{}\'?"

    def __init__(self, id, correct_movie, option_movie_1, 
                 option_movie_2, option_movie_3, option_movie_4) -> None:
        self.id = id
        self.question = self.QUESTION_TEMPLATE.format(correct_movie.get_title())
        self.correct_movie_id = str(correct_movie.get_id())
        self.option_movie_1 = option_movie_1
        self.option_movie_2 = option_movie_2
        self.option_movie_3 = option_movie_3
        self.option_movie_4 = option_movie_4
        self.option_movie_5 = correct_movie

    def get_shuffled_option_movies(self):
        option_movies = [self.option_movie_1, self.option_movie_2, self.option_movie_3, self.option_movie_4, self.option_movie_5]
        random.shuffle(option_movies)
        return option_movies
    
    def get_id(self):
        return self.id
    
    def get_correct_movie_id(self):
        return self.correct_movie_id
    
    def get_question(self):
        return self.question