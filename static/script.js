// Initialize movie modal
const movieModal = new bootstrap.Modal(document.getElementById('movieModal'));

// Add click handlers for movie cards
document.addEventListener('DOMContentLoaded', function() {
    // Add click handlers to all movie cards
    document.querySelectorAll('.movie-card').forEach(card => {
        card.addEventListener('click', function() {
            const movieId = this.dataset.movieId;
            showMovieDetails(movieId);
        });
    });
});

function showMovieDetails(movieId) {
    fetch(`/movie_details/${movieId}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const details = data.details;
                const credits = data.credits;
                const similar = data.similar;

                // Update modal content
                document.querySelector('.modal-title').textContent = details.title;
                document.getElementById('modalPoster').src = details.poster_path;
                document.getElementById('movieOverview').textContent = details.overview;
                document.getElementById('movieRelease').textContent = details.release_date;
                document.getElementById('movieRating').textContent = `⭐ ${details.vote_average}/10 (${details.vote_count} votes)`;
                document.getElementById('movieRuntime').textContent = `${details.runtime} minutes`;
                document.getElementById('movieGenres').textContent = details.genres.join(', ');

                // Update cast
                const castHTML = credits.cast.map(person => `
                    <div class="cast-member">
                        <img src="${person.profile_path || '/static/placeholder.jpg'}" alt="${person.name}">
                        <div class="name">${person.name}</div>
                        <div class="character">${person.character}</div>
                    </div>
                `).join('');
                document.getElementById('movieCast').innerHTML = castHTML;

                // Update similar movies
                const similarHTML = similar.slice(0, 6).map(movie => `
                    <div class="col-md-2 mb-3">
                        <div class="movie-card" data-movie-id="${movie.id}">
                            <img src="${movie.poster_path}" class="img-fluid rounded movie-poster" alt="${movie.title}">
                            <div class="movie-info">
                                <h5>${movie.title}</h5>
                                <div class="rating">⭐ ${movie.vote_average}</div>
                            </div>
                        </div>
                    </div>
                `).join('');
                document.getElementById('similarMovies').innerHTML = similarHTML;

                // Show modal
                movieModal.show();

                // Add click handlers to similar movie cards
                document.querySelectorAll('#similarMovies .movie-card').forEach(card => {
                    card.addEventListener('click', function() {
                        movieModal.hide();
                        setTimeout(() => {
                            showMovieDetails(this.dataset.movieId);
                        }, 500);
                    });
                });
            }
        })
        .catch(error => console.error('Error:', error));
}

document.getElementById('movieForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const movieTitle = document.getElementById('movieTitle').value;
    
    fetch('/recommend_by_movie', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `movie_title=${encodeURIComponent(movieTitle)}`
    })
    .then(response => response.json())
    .then(data => {
        const recommendationsDiv = document.getElementById('movieRecommendations');
        if (data.success) {
            let html = '<div class="mt-4">';
            data.recommendations.forEach(rec => {
                html += `
                    <div class="recommendation-item">
                        <img src="${rec.poster_path}" class="recommendation-poster" alt="${rec.title}">
                        <div class="recommendation-content">
                            <div class="recommendation-title">${rec.title}</div>
                            <div class="recommendation-overview">${rec.overview}</div>
                            <div class="recommendation-score">
                                Similarity: ${rec.similarity_score}% | Rating: ⭐ ${rec.vote_average}/10
                            </div>
                        </div>
                    </div>
                `;
            });
            html += '</div>';
            recommendationsDiv.innerHTML = html;
        } else {
            recommendationsDiv.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('movieRecommendations').innerHTML = 
            '<div class="alert alert-danger">An error occurred while fetching recommendations.</div>';
    });
});

document.getElementById('userForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const userId = document.getElementById('userId').value;
    
    fetch('/recommend_by_user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `user_id=${encodeURIComponent(userId)}`
    })
    .then(response => response.json())
    .then(data => {
        const recommendationsDiv = document.getElementById('userRecommendations');
        if (data.success) {
            let html = '<div class="mt-4">';
            data.recommendations.forEach(rec => {
                html += `
                    <div class="recommendation-item">
                        <img src="${rec.poster_path}" class="recommendation-poster" alt="${rec.title}">
                        <div class="recommendation-content">
                            <div class="recommendation-title">${rec.title}</div>
                            <div class="recommendation-overview">${rec.overview}</div>
                            <div class="recommendation-score">
                                Predicted Rating: ${rec.predicted_rating} | Current Rating: ⭐ ${rec.vote_average}/10
                            </div>
                        </div>
                    </div>
                `;
            });
            html += '</div>';
            recommendationsDiv.innerHTML = html;
        } else {
            recommendationsDiv.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('userRecommendations').innerHTML = 
            '<div class="alert alert-danger">An error occurred while fetching recommendations.</div>';
    });
});
