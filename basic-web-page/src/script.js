// This file contains the JavaScript code that handles user input for the year.
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('yearForm');
    const yearInput = document.getElementById('yearInput');
    const result = document.getElementById('result');

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const year = yearInput.value;
        result.textContent = `You entered the year: ${year}`;
    });
});