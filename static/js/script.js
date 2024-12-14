document.addEventListener('DOMContentLoaded', function() {
    const generateButton = document.getElementById('generateButton');
    const textInput = document.getElementById('hate-comment');
    const outputDiv = document.getElementById('output');
    const problemStatement = document.getElementById('problem-statement');

    const button_formell = document.getElementById('Formell');
    const button_humor = document.getElementById('Humorvoll');
    const button_konfrontativ = document.getElementById('Konfrontativ');
    const button_einfühlsam = document.getElementById('Einfühlsam');

    //selection of output length
    let maxWords = 200;
    const length_buttons = document.querySelectorAll('.length-button');

    //set default active "mittel" button
    document.getElementById('mittel').classList.add('active');
    
    // Add click event listeners for all length buttons
    length_buttons.forEach((button) => {
        button.addEventListener('click', function () {
            // Remove 'active' class from all buttons
            length_buttons.forEach(btn => btn.classList.remove('active'));

            // Add 'active' class to the clicked button
            button.classList.add('active');

            // Set maxWords based on the button clicked
            if (button.id === 'kurz') {
                maxWords = 100;
            } else if (button.id === 'mittel') {
                maxWords = 200;
            } else if (button.id === 'lang') {
                maxWords = 300;
            }
        });
    });

    button_formell.style.backgroundColor = "#a3e077";
    CN_formell = localStorage.getItem('CN_formell');

    //check if there is a generated CN
    if (CN_formell) {
        outputDiv.textContent = CN_formell;
        problemStatement.textContent = localStorage.getItem('problem-statement');
    } else {
        outputDiv.textContent = "Keine CN gefunden.";
    }

    generateButton.addEventListener('click', function() {
        const inputText = textInput.value.trim();

        generateButton.innerText = "Bitte warten...";
        generateButton.disabled = true;

        button_formell.style.backgroundColor = "#a3e077";
        button_humor.style.backgroundColor = "#5EA62B";
        button_konfrontativ.style.backgroundColor = "#5EA62B";
        button_einfühlsam.style.backgroundColor = "#5EA62B";

        if (inputText !== '') {
            fetch('/generateCN', 
            {
                method: 'POST', 
                headers: {
                    'Content-Type': 'application/json'
                }, 
                body: JSON.stringify({
                    "text": inputText,
                    "wordLimit": maxWords.toString()
                })
            })
            .then(response => response.json())
            .then(data => {
                localStorage.setItem('CN_formell', data.CN_formell);
                localStorage.setItem('CN_humor', data.CN_humor);
                localStorage.setItem('CN_konfrontativ', data.CN_konfrontativ);
                localStorage.setItem('CN_einfühlsam', data.CN_einfühlsam);

                outputDiv.innerText = data.CN_formell;
                problemStatement.innerText = data.problem;
            })
            .catch(error => {
                outputDiv.innerText = 'Error: ' + error;
            })
            .finally(() => {
                generateButton.disabled = false;
                generateButton.innerText = 'Gegenrede generieren';
            });
        } else {
            outputDiv.innerText = 'Please enter some text.';
            generateButton.disabled = false;
            generateButton.innerText = 'Gegenrede generieren';
        }
    });


    button_formell.addEventListener('click', function() 
    {
        outputDiv.textContent = localStorage.getItem('CN_formell');
        button_formell.style.backgroundColor = "#a3e077";
        button_humor.style.backgroundColor = "#5EA62B";
        button_konfrontativ.style.backgroundColor = "#5EA62B";
        button_einfühlsam.style.backgroundColor = "#5EA62B";
    });

    button_humor.addEventListener('click', function() 
    {
        outputDiv.textContent = localStorage.getItem('CN_humor');
        button_formell.style.backgroundColor = "#5EA62B";
        button_humor.style.backgroundColor = "#a3e077";
        button_konfrontativ.style.backgroundColor = "#5EA62B";
        button_einfühlsam.style.backgroundColor = "#5EA62B";
    });

    button_konfrontativ.addEventListener('click', function() 
    {
        outputDiv.textContent = localStorage.getItem('CN_konfrontativ');
        button_formell.style.backgroundColor = "#5EA62B";
        button_humor.style.backgroundColor = "#5EA62B";
        button_konfrontativ.style.backgroundColor = "#a3e077";
        button_einfühlsam.style.backgroundColor = "#5EA62B";
    });

    button_einfühlsam.addEventListener('click', function() 
    {
        outputDiv.textContent = localStorage.getItem('CN_einfühlsam');
        button_formell.style.backgroundColor = "#5EA62B";
        button_humor.style.backgroundColor = "#5EA62B";
        button_konfrontativ.style.backgroundColor = "#5EA62B";
        button_einfühlsam.style.backgroundColor = "#a3e077";
    });

});