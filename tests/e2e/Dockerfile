FROM mcr.microsoft.com/playwright/python:v1.45.0-jammy
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN playwright install
WORKDIR /movie-quizz-app
COPY . .
ENV FLASK_APP=app.py
CMD ["gunicorn" , "--bind", "0.0.0.0:8000", "app:app"]
EXPOSE 8000
