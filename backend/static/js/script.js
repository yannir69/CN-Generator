document.addEventListener('DOMContentLoaded', function() {
    const generateButton = document.getElementById('generateButton');
    const textInput = document.getElementById('textInput');
    const outputDiv = document.getElementById('outputDiv');

    generateButton.addEventListener('click', function() {
        const inputText = textInput.value.trim();
        if (inputText !== '') {
            fetch('/generateCN', 
            {method: 'POST', 
            headers: {
                'Content-Type': 'application/json'
            }, 
            body: JSON.stringify(inputText)})
            .then(response => response.text())
            .then(text => {
                outputDiv.innerText = text;
            })
            .catch(error => {
                outputDiv.innerText = 'Error: ' + error;
            });
        } else {
            outputDiv.innerText = 'Please enter some text.';
        }
    });
});