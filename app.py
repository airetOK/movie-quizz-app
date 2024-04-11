from flask import Flask, render_template, request
from client.movie_api_client import MovieApiClient
from service.movie_service_impl import MovieServiceImpl
from service.quizz_service_impl import QuizzServiceImpl

app = Flask(__name__)
client = MovieApiClient()
movie_service = MovieServiceImpl(client)
quizzes = {}


@app.route("/quizz")
def new_quizz():
    quizz = QuizzServiceImpl().generate_quizz(
        movie_service.get_five_random_movies())
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
                               is_correct=QuizzServiceImpl().verify_quizz(request.form['option_movie_id'], quizzes[id]))
