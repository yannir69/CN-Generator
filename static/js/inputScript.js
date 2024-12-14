document.addEventListener('DOMContentLoaded', function() 
{
    submitButton = document.getElementById('submit-button');

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

    submitButton.addEventListener('click', function () 
    {
        const comment = document.getElementById('hate-comment').value;
        submitButton.innerText = 'Bitte warten...';
        submitButton.disabled = true;

        if (comment.trim() === "") {
            alert("Bitte geben Sie einen Kommentar ein!"); // Alert for empty input
            return;
        }
        else 
        {
            fetch('/generateCN', 
                {
                    method: 'POST', 
                    headers: {
                        'Content-Type': 'application/json'
                    }, 
                    body: JSON.stringify({
                        "text": comment,
                        "wordLimit": maxWords.toString()
                    })
                })
                .then(response => response.json())
                .then(data => {
                    localStorage.setItem('CN_formell', data.CN_formell);
                    localStorage.setItem('CN_humor', data.CN_humor);
                    localStorage.setItem('CN_konfrontativ', data.CN_konfrontativ);
                    localStorage.setItem('CN_einfühlsam', data.CN_einfühlsam);
                    localStorage.setItem('problem-statement', data.problem);
                    window.location.href = "/CN";
                })
                .catch(error => {
                    localStorage.setItem('CN', "Error");
                })
                .finally(() => {
                    submitButton.disabled = false;
                    submitButton.innerText = 'Gegenrede generieren';
                });
        }
    });
});