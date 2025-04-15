//This is the script that handles the interactions on the final output page
document.addEventListener('DOMContentLoaded', function() {
    const generateButton = document.getElementById('generateButton');
    const textInput = document.getElementById('hate-comment');
    const outputDiv = document.getElementById('output');
    const problemStatement = document.getElementById('problem-statement');

    const button_sachlich = document.getElementById('Sachlich');
    const button_humor = document.getElementById('Humorvoll');
    const button_gegenposition = document.getElementById('Gegenposition');
    const button_empathisch = document.getElementById('Empathisch');

    //selection of output length
    let maxWords = 10;
    const length_buttons = document.querySelectorAll('.length-button');

    //set default active "kurz" button
    document.getElementById('kurz').classList.add('active');
    
    // Add click event listeners for all length buttons
    length_buttons.forEach((button) => {
        button.addEventListener('click', function () {
            // Remove 'active' class from all buttons
            length_buttons.forEach(btn => btn.classList.remove('active'));

            // Add 'active' class to the clicked button
            button.classList.add('active');

            // Set maxWords based on the button clicked
            if (button.id === 'kurz') {
                maxWords = 10;
            } else if (button.id === 'lang') {
                maxWords = 30;
            }
        });
    });

    //set initial selection on the "formell" style
    button_sachlich.style.backgroundColor = "#a3e077";
    CN_formell = localStorage.getItem('CN_formell');

    //check if there is a generated CN
    if (CN_formell) {
        outputDiv.textContent = CN_formell;
        problemStatement.textContent = localStorage.getItem('problem-statement');
    } else {
        outputDiv.textContent = "Keine CN gefunden.";
    }

    //Click-Event of the generate button, this will kick off the CN-generation
    generateButton.addEventListener('click', function() {
        const inputText = textInput.value.trim();

        generateButton.innerText = "Bitte warten...";
        generateButton.disabled = true;

        //set selected style
        button_sachlich.style.backgroundColor = "#a3e077";
        button_humor.style.backgroundColor = "#5EA62B";
        button_gegenposition.style.backgroundColor = "#5EA62B";
        button_empathisch.style.backgroundColor = "#5EA62B";

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
                //this is the received data from app.py
                localStorage.setItem('CN_formell', data.CN_formell);
                localStorage.setItem('CN_humor', data.CN_humor);
                localStorage.setItem('CN_konfrontativ', data.CN_konfrontativ);
                localStorage.setItem('CN_einfühlsam', data.CN_einfühlsam);

                //default output is always the "formell" style
                outputDiv.innerText = data.CN_formell;
                //output the problem statement
                problemStatement.innerText = data.problem;
            })
            .catch(error => {
                outputDiv.innerText = 'Error: ' + error;
            })
            //when everything is done, enable the button again for a new hate comment
            .finally(() => {
                generateButton.disabled = false;
                generateButton.innerText = 'Gegenrede generieren';
            });
        } else {
            //if nothing is entered
            outputDiv.innerText = 'Please enter some text.';
            generateButton.disabled = false;
            generateButton.innerText = 'Gegenrede generieren';
        }
    });

    //All of the below are button color changes for selections
    button_sachlich.addEventListener('click', function() 
    {
        outputDiv.textContent = localStorage.getItem('CN_formell');
        button_sachlich.style.backgroundColor = "#a3e077";
        button_humor.style.backgroundColor = "#5EA62B";
        button_gegenposition.style.backgroundColor = "#5EA62B";
        button_empathisch.style.backgroundColor = "#5EA62B";
    });

    button_humor.addEventListener('click', function() 
    {
        outputDiv.textContent = localStorage.getItem('CN_humor');
        button_sachlich.style.backgroundColor = "#5EA62B";
        button_humor.style.backgroundColor = "#a3e077";
        button_gegenposition.style.backgroundColor = "#5EA62B";
        button_empathisch.style.backgroundColor = "#5EA62B";
    });

    button_gegenposition.addEventListener('click', function() 
    {
        outputDiv.textContent = localStorage.getItem('CN_konfrontativ');
        button_sachlich.style.backgroundColor = "#5EA62B";
        button_humor.style.backgroundColor = "#5EA62B";
        button_gegenposition.style.backgroundColor = "#a3e077";
        button_empathisch.style.backgroundColor = "#5EA62B";
    });

    button_empathisch.addEventListener('click', function() 
    {
        outputDiv.textContent = localStorage.getItem('CN_einfühlsam');
        button_sachlich.style.backgroundColor = "#5EA62B";
        button_humor.style.backgroundColor = "#5EA62B";
        button_gegenposition.style.backgroundColor = "#5EA62B";
        button_empathisch.style.backgroundColor = "#a3e077";
    });

});