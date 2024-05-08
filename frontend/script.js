document.addEventListener('DOMContentLoaded', function() {
    const generateButton = document.getElementById('generateButton');
    const textInput = document.getElementById('textInput');
    const outputDiv = document.getElementById('output');

    generateButton.addEventListener('click', function() {
        const inputText = textInput.value.trim();
        if (inputText !== '') {
            // Send inputText to backend for processing (to be implemented)
            // For now, just display the input text as output
            outputDiv.innerText = inputText;
        } else {
            outputDiv.innerText = 'Please enter some text.';
        }
    });
});