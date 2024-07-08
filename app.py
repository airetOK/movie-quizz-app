from flask import Flask, render_template, request
from client.movie_api_client import MovieApiClient
from service.movie_service_impl import MovieServiceImpl
from service.quizz_service_impl import QuizzServiceImpl
from service.game_service_impl import GameServiceImpl

app = Flask(__name__)
''' API client '''
client = MovieApiClient()
''' Services '''
movie_service = MovieServiceImpl(client)
quizz_service = QuizzServiceImpl(movie_service)
game_service = GameServiceImpl(quizz_service)
''' Data '''
quizzes = {}
game_quizzes = {}


@app.route("/")
def main_menu():
    return render_template("main-menu.html")


@app.route("/start")
def start_game():
    game = game_service.generate_game()
    game_quizzes[game.get_id()] = game.get_quizzes()
    return render_template("game.html",
                           game_id=game.get_id(),
                           quizzes=game.get_quizzes())


@app.route("/game/<game_id>")
def game(game_id):
    return render_template("game.html",
                           game_id=game_id,
                           quizzes=game_quizzes[game_id])


@app.route("/game/<game_id>/verify", methods=['POST'])
def game_verify(game_id):
    if request.method == 'POST':
        questions = game_quizzes[game_id]
        result = game_service.verify(questions, request.form['correct-answers'].split('-'))
        return render_template("game-result.html", game_result=result, game_id=game_id)


@app.route("/quizz")
def new_quizz():
    quizz = quizz_service.generate_quizz(movie_service.get_five_random_movies())
    quizzes[quizz.get_id()] = quizz
    return render_template("quizz.html", quizz=quizz)


@app.route("/quizz/<id>")
def quizz(id):
    return render_template("quizz.html", quizz=quizzes[id])


@app.route("/quizz/<id>/verify", methods=['POST'])
def verify(id):
    if request.method == 'POST':
        return render_template("result.html",
                               quizz_id=id,
                               is_correct=quizz_service.verify_quizz(
                                   request.form['option_movie_id'], quizzes[id]))
