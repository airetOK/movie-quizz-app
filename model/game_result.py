class GameResult:

    def __init__(self, total_amount: int, correct_answers: int) -> None:
        self.total_amount = total_amount
        self.correct_answers = correct_answers

    def get_total_amount(self):
        return self.total_amount

    def get_correct_answers(self):
        return self.correct_answers
