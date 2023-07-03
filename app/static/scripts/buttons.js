fetch('/genre')
    .then(response => response.json())
    .then(data => {
        const genreButtonsDiv = document.getElementById('genreButtons');
        data.forEach(genre => {
            const button = document.createElement('input');
            button.type = 'submit';
            button.name = 'genre';
            button.value = genre;
            button.classList.add('genre-button');
            
            genreButtonsDiv.appendChild(button);
            button.addEventListener('click', function(event) {
                event.preventDefault();
                 
                const clickedGenre = genre;
                const clickedGenreInput = document.getElementById('clickedGenre');
                
                clickedGenreInput.value = clickedGenre;
                const form = document.getElementById('form');
                form.submit();
            });
        });
    });