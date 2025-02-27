from model.quizz import Quizz


class Game:

    def __init__(self, id: str, quizzes: list[Quizz]) -> None:
        self.id = id
        self.quizzes = quizzes

    def get_id(self):
        return self.id

    def get_quizzes(self):
        return self.quizzes
