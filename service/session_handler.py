from flask import session
from typing import Dict


class SessionHandler:

    __CORRECT_ANSWERS: str = "correct_answers"
    __TOTAL_QUIZZES: str = "total_quizzes"

    def initialize(self):
        session.setdefault(self.__TOTAL_QUIZZES, 0)
        session.setdefault(self.__CORRECT_ANSWERS, 0)

    def store_quizz_result(self, is_correct: bool):
        session[self.__TOTAL_QUIZZES] += 1
        if is_correct:
            session[self.__CORRECT_ANSWERS] += 1

    def get_data(self) -> Dict[str, int]:
        return {self.__TOTAL_QUIZZES: session.get(self.__TOTAL_QUIZZES, 0),
                self.__CORRECT_ANSWERS: session.get(self.__CORRECT_ANSWERS, 0)}
