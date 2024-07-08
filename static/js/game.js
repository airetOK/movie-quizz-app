function chooseMovie(event) {
    for (let button of event.parentNode.childNodes) {
        if (button.value) {
            if (button.style.backgroundColor === 'rgb(74, 191, 34)') {
                button.style.backgroundColor = '';
                button.style.borderColor = '';
                button.setAttribute('is-movie-correct', 'False');
            }
        }
    }
    event.style.backgroundColor = 'rgb(74, 191, 34)';
    event.style.borderColor = 'rgb(74, 191, 34)';
    event.setAttribute('is-movie-correct', 'True');
}

function appendCorrectAnswersToInputForm() {
    let result = '';
    const containers = document.querySelectorAll('.image-container');
    for (let container of containers) {
        for (let button of container.childNodes) {
            if (button.value) {
                if (button.getAttribute('is-movie-correct') === 'True') {
                    result = result + button.value + '-';
                }
            }
        }
    }
    result = result.slice(0, -1);

    const button = document.querySelector('.submit-answers-btn');
    button.value = result
}
