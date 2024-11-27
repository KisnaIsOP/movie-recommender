# 🎬 Movie Recommendation System

An intelligent, web-based movie recommendation platform that combines machine learning with real-time movie data from TMDB.

## ✨ Features

### 🎯 Recommendation Engine
- Content-based recommendations using movie genres
- Collaborative filtering based on user ratings
- Real-time movie information from TMDB
- Trending movies showcase
- Top-rated movies analysis

### 🌐 Web Interface
- Responsive movie card design
- Interactive movie details modal
- Dynamic content loading
- Real-time search functionality
- Beautiful and modern UI

### 🛠 Technical Features
- Flask-based REST API
- Caching for improved performance
- Secure API key management
- Comprehensive error handling
- Detailed logging system

## 🚀 Setup

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Configure Environment**
   - Copy `.env.example` to `.env`
   - Get a TMDB API key from https://www.themoviedb.org/settings/api
   - Add your TMDB API key to `.env`:
     ```
     TMDB_API_KEY=your_api_key_here
     ```

3. **Download Dataset**
   - Visit: https://grouplens.org/datasets/movielens/
   - Download the "ml-latest-small.zip" dataset
   - Extract `movies.csv` and `ratings.csv` to the project directory

4. **Run the Application**
```bash
python app.py
```

## 🏗 Architecture

### 🔄 Backend Components
1. **Flask Application (`app.py`)**
   - REST API endpoints
   - Request handling
   - Response formatting
   - Caching implementation

2. **Movie Recommender (`movie_recommender.py`)**
   - Content-based filtering
   - Collaborative filtering
   - Dataset analysis
   - Rating predictions

3. **TMDB Client (`tmdb_client.py`)**
   - Real-time movie data
   - Movie search
   - Cast and crew information
   - Similar movies recommendations

### 🎨 Frontend Components
1. **HTML Template (`templates/index.html`)**
   - Responsive layout
   - Bootstrap integration
   - Dynamic content sections

2. **JavaScript (`static/script.js`)**
   - AJAX requests
   - Modal handling
   - Dynamic content updates
   - Error handling

3. **CSS (`static/style.css`)**
   - Modern design
   - Responsive layouts
   - Animations and transitions
   - Consistent theming

## 🔧 Configuration

### Environment Variables (`.env`)
```
TMDB_API_KEY=your_api_key_here
FLASK_ENV=development
FLASK_DEBUG=1
CACHE_TYPE=SimpleCache
CACHE_DEFAULT_TIMEOUT=300
```

### Application Settings (`config.py`)
- API configuration
- Cache settings
- Dataset paths
- Recommendation parameters
- TMDB API settings

## 📦 Dependencies

- Flask 3.0.0
- pandas 2.1.3
- numpy 1.26.2
- scikit-learn 1.3.2
- tmdbv3api 1.9.0
- python-dotenv 1.0.0
- Flask-Caching 2.1.0
- Additional dependencies in `requirements.txt`

## 🚧 Known Limitations

- Recommendation quality depends on dataset size
- Real-time data requires active TMDB API key
- Performance may vary with large datasets

## 🔮 Future Improvements

1. **Features**
   - User authentication
   - Personalized watchlists
   - Rating submission
   - Advanced recommendation algorithms

2. **Technical**
   - Docker containerization
   - Advanced caching strategies
   - Comprehensive testing
   - Performance optimization

## 📝 Note

This system combines the MovieLens dataset with real-time TMDB data to provide a comprehensive movie recommendation experience. The quality of recommendations depends on both the dataset size and the availability of TMDB API services.
