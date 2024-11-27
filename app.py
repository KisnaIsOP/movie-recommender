from flask import Flask, render_template, request, jsonify
from flask_caching import Cache
from movie_recommender import MovieRecommender
from tmdb_client import TMDBClient
from config import Config
import json
import os
import logging
from functools import wraps

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize caching
cache = Cache(app)

# Initialize the recommender system
try:
    recommender = MovieRecommender(
        Config.MOVIES_DATASET,
        Config.RATINGS_DATASET
    )
    logger.info("MovieRecommender initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize MovieRecommender: {str(e)}")
    raise

# Initialize TMDB client
try:
    tmdb_client = TMDBClient(Config.TMDB_API_KEY)
    logger.info("TMDBClient initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize TMDBClient: {str(e)}")
    raise

def handle_errors(f):
    """Decorator to handle errors consistently across routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {f.__name__}: {str(e)}")
            return jsonify({
                'success': False,
                'error': str(e),
                'message': 'An error occurred while processing your request.'
            }), 500
    return decorated_function

@app.route('/')
@cache.cached(timeout=300)  # Cache for 5 minutes
@handle_errors
def home():
    # Get trending movies
    trending_movies = tmdb_client.get_trending_movies()
    
    # Get top rated movies from our dataset
    top_rated = recommender.get_top_rated_movies(
        min_reviews=Config.MIN_REVIEWS_FOR_TOP_RATED
    ).head(10)
    
    top_rated_list = [{
        'title': movie['title'],
        'rating': float(movie['rating_mean']),
        'votes': int(movie['rating_count']),
        'genres': movie['genres']
    } for movie in top_rated.to_dict('records')]
    
    return render_template('index.html', 
                         trending_movies=trending_movies, 
                         top_rated=top_rated_list)

@app.route('/recommend_by_movie', methods=['POST'])
@cache.memoize(timeout=300)
@handle_errors
def recommend_by_movie():
    movie_title = request.form.get('movie_title')
    if not movie_title:
        return jsonify({'success': False, 'error': 'Movie title is required'}), 400
        
    # Get recommendations from our dataset
    recommendations = recommender.content_based_recommendations(
        movie_title,
        num_recommendations=Config.DEFAULT_NUM_RECOMMENDATIONS
    )
    
    # Get real-time movie data for the recommendations
    enhanced_recommendations = []
    for rec in recommendations:
        tmdb_results = tmdb_client.search_movies(rec['title'])
        if tmdb_results:
            tmdb_movie = tmdb_results[0]  # Get the first match
            rec.update({
                'poster_path': tmdb_movie['poster_path'],
                'overview': tmdb_movie['overview'],
                'vote_average': tmdb_movie['vote_average'],
                'similarity_score': int(rec['similarity'] * 100)  # Convert to percentage
            })
            enhanced_recommendations.append(rec)
    
    return jsonify({'success': True, 'recommendations': enhanced_recommendations})

@app.route('/recommend_by_user', methods=['POST'])
@cache.memoize(timeout=300)
@handle_errors
def recommend_by_user():
    try:
        user_id = int(request.form.get('user_id'))
    except (TypeError, ValueError):
        return jsonify({'success': False, 'error': 'Valid user ID is required'}), 400
        
    recommendations = recommender.collaborative_recommendations(
        user_id,
        num_recommendations=Config.DEFAULT_NUM_RECOMMENDATIONS
    )
    
    # Enhance recommendations with TMDB data
    enhanced_recommendations = []
    for rec in recommendations:
        tmdb_results = tmdb_client.search_movies(rec['title'])
        if tmdb_results:
            tmdb_movie = tmdb_results[0]
            rec.update({
                'poster_path': tmdb_movie['poster_path'],
                'overview': tmdb_movie['overview'],
                'vote_average': tmdb_movie['vote_average'],
                'predicted_rating': round(float(rec['predicted_rating']), 1)
            })
            enhanced_recommendations.append(rec)
        
    return jsonify({'success': True, 'recommendations': enhanced_recommendations})

@app.route('/search_movies', methods=['POST'])
@cache.memoize(timeout=300)
@handle_errors
def search_movies():
    query = request.form.get('query')
    if not query:
        return jsonify({'success': False, 'error': 'Search query is required'}), 400
        
    movies = tmdb_client.search_movies(query)
    return jsonify({'success': True, 'movies': movies})

@app.route('/movie_details/<int:movie_id>')
@cache.memoize(timeout=300)
@handle_errors
def movie_details(movie_id):
    # Get all movie information in parallel
    details = tmdb_client.get_movie_details(movie_id)
    if not details:
        return jsonify({'success': False, 'error': 'Movie not found'}), 404
        
    credits = tmdb_client.get_movie_credits(movie_id)
    similar = tmdb_client.get_similar_movies(movie_id)
    
    return jsonify({
        'success': True,
        'details': details,
        'credits': credits,
        'similar': similar
    })

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'success': False, 'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'success': False, 'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=Config.DEBUG)
