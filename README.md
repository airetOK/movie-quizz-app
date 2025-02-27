## General info
This MVC application built on Flask is using The MovieDB API to generate quizzes about movies.

## Local develeopment

1. Create the virtual environment.
Execute from the root project **python -m venv venv**

>NOTE: don't change the name for your virtual environment,
>because *.gitignore* includes *venv*

2. Start the virtual environemnt.
Go to **/path/to/new/virtual/environment/Scripts**,
then execute **Activate.ps1**

3. Install the dependencies.
From the project's root run **pip install -r requirements.txt**

4. Create .env file.
Create the **.env** file. Copy paste the content from **.env.example** to .env file, and update the *API_ACCESS_TOKEN* with the existing one.


5. Start the application.
From the root execute **flask --app app run**.
The application is living on *http://localhost:5000* by default.
Send your first request on *http://localhost:5000/quizz*

## Run docker container
Before the creating a container, create the **.env** file (look to the *Local development section, 4th point*)
From the project's root execute **docker-compose up -d**.
The application is living on *http://localhost:5000* by default.
Send your first request on *http://localhost:5000/quizz*

## Run unit tests
From the project's root execute **pytest**.

## Run e2e tests
The e2e is executing in the separate docker container.
First, execute **playwright install** from the project's root. This command installs the chromium's driver.
After that, execute **docker-compose up -d**.
The container for e2e testing lives on *http://localhost:5001*.
Execute **pytest/tests/e2e**.

## Generate code coverage
From the project's root execute

 - **coverage run**
 - **coverage report -m**
 - **covergae html**

The coverage report will be stored in the *coverage_html_report/index.html* file.

## Pre-commit setup
Execute **pre-commit install** to set up the git hook scripts.
After that *pre-commit* will run automatically on *git commit*.
