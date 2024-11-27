import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration."""
    # Flask
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    DEBUG = os.getenv('FLASK_DEBUG', '0') == '1'
    
    # API Keys
    TMDB_API_KEY = os.getenv('TMDB_API_KEY')
    if not TMDB_API_KEY or TMDB_API_KEY == 'your_api_key_here':
        raise ValueError(
            'TMDB_API_KEY not set! Please set it in your .env file. '
            'Get your API key from https://www.themoviedb.org/settings/api'
        )
    
    # Cache
    CACHE_TYPE = os.getenv('CACHE_TYPE', 'SimpleCache')
    CACHE_DEFAULT_TIMEOUT = int(os.getenv('CACHE_DEFAULT_TIMEOUT', 300))
    
    # Dataset paths
    MOVIES_DATASET = 'movies.csv'
    RATINGS_DATASET = 'ratings.csv'
    
    # Recommendation settings
    DEFAULT_NUM_RECOMMENDATIONS = 5
    MIN_REVIEWS_FOR_TOP_RATED = 100
    
    # TMDB API settings
    TMDB_IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/'
    TMDB_POSTER_SIZE = 'w500'
    TMDB_BACKDROP_SIZE = 'original'
    TMDB_PROFILE_SIZE = 'w185'
