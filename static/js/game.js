function chooseMovie(clickedButton) {
    const parentRow = clickedButton.closest('.movies');
    const rowButtons = parentRow.querySelectorAll('button');
    Array.from(rowButtons).map(button => { 
        button.style.backgroundColor = '';
        button.style.borderColor = '';
        button.setAttribute('is-movie-correct', 'False');
    });
    clickedButton.style.backgroundColor = 'rgb(74, 191, 34)';
    clickedButton.style.borderColor = 'rgb(74, 191, 34)';
    clickedButton.setAttribute('is-movie-correct', 'True');
}

function appendCorrectAnswersToInputForm() {
    let moviesIds = '';
    const movies = document.querySelectorAll('.movies');
    movies.forEach(movie => {
        const buttons = movie.querySelectorAll('.quizz .btn');
        buttons.forEach(button => {
            if (button.getAttribute('is-movie-correct') === 'True') {
                moviesIds = moviesIds + button.value + '-';
            }
        });
    });
    moviesIds = moviesIds.slice(0, -1);
    
    const submitAnswersButton = document.querySelector('.submit-answers-btn');
    submitAnswersButton.value = moviesIds;
}
