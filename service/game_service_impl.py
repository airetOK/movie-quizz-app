from service.game_service import GameService
from service.quizz_service import QuizzService
from model.game import Game
from model.quizz import Quizz
from model.game_result import GameResult
import uuid


class GameServiceImpl(GameService):

    def __init__(self, quizz_service: QuizzService) -> None:
        super().__init__()
        self.quizz_service = quizz_service

    def generate_game(self) -> Game:
        return Game(self.__get_unique_id(), self.quizz_service.load_quizzes())

    def verify(self, quizzes: list[Quizz], answers_id: list[str]) -> GameResult:
        correct_answers = 0
        total_amount = len(quizzes)

        for i in range(total_amount):
            if quizzes[i].get_correct_movie_id() == answers_id[i]:
                correct_answers += 1

        return GameResult(total_amount, correct_answers)

    def __get_unique_id(self):
        return str(uuid.uuid4())
