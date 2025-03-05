from flask import Flask, render_template, request
from flask_session import Session

from client.movie_api_client import MovieApiClient
from service.movie_service_impl import MovieServiceImpl
from service.quizz_service_impl import QuizzServiceImpl
from service.game_service_impl import GameServiceImpl
from service.session_handler import SessionHandler
from configuration.session_configuration import SessionConfiguration

app = Flask(__name__)
app.config.from_object(SessionConfiguration())
Session(app)
''' API client '''
client = MovieApiClient()
''' Services '''
movie_service = MovieServiceImpl(client)
quizz_service = QuizzServiceImpl(movie_service)
game_service = GameServiceImpl(quizz_service)
session_handler = SessionHandler()
''' Data '''
quizzes = {}
game_quizzes = {}


@app.before_request
def initialize_session():
    session_handler.initialize()


@app.route("/")
def main_menu():
    return render_template("main-menu.html",
                           session_data=session_handler.get_data())


@app.route("/start")
def start_game():
    game = game_service.generate_game()
    game_quizzes[game.get_id()] = game.get_quizzes()
    return render_template("game.html",
                           game_id=game.get_id(),
                           quizzes=game.get_quizzes(),
                           session_data=session_handler.get_data())


@app.route("/game/<game_id>")
def game(game_id):
    return render_template("game.html",
                           game_id=game_id,
                           quizzes=game_quizzes[game_id],
                           session_data=session_handler.get_data())


@app.route("/game/<game_id>/verify", methods=['POST'])
def game_verify(game_id):
    if request.method == 'POST':
        questions = game_quizzes[game_id]
        result = game_service.verify(questions, request.form['correct-answers'].split('-'))
        return render_template("game-result.html",
                               game_result=result,
                               game_id=game_id,
                               session_data=session_handler.get_data())


@app.route("/quizz")
def new_quizz():
    quizz = quizz_service.generate_quizz()
    quizzes[quizz.get_id()] = quizz
    return render_template("quizz.html",
                           quizz=quizz,
                           session_data=session_handler.get_data())


@app.route("/quizz/<id>")
def quizz(id):
    return render_template("quizz.html",
                           quizz=quizzes[id],
                           session_data=session_handler.get_data())


@app.route("/quizz/<id>/verify", methods=['POST'])
def verify(id):
    is_correct = quizz_service.verify_quizz(request.form['option_movie_id'], quizzes[id])
    session_handler.store_quizz_result(is_correct)
    if request.method == 'POST':
        return render_template("result.html",
                               is_correct=is_correct,
                               quizz_id=id,
                               session_data=session_handler.get_data())
