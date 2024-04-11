FROM python:3.9.12-slim
RUN apt-get update && \
    apt-get install -y libpq-dev gcc
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
WORKDIR /movie-quizz-app
COPY . .
ENV FLASK_APP=app.py
CMD ["gunicorn" , "--bind", "0.0.0.0:8000", "app:app"]
EXPOSE 8000