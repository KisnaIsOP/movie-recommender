from tmdbv3api import TMDb, Movie, Trending, Search, Person
import os

class TMDBClient:
    def __init__(self, api_key):
        self.tmdb = TMDb()
        self.tmdb.api_key = api_key
        self.movie = Movie()
        self.trending = Trending()
        self.search = Search()
        self.person = Person()

    def get_trending_movies(self, time_window='week', page=1):
        """Get trending movies for the week or day."""
        try:
            movies = self.trending.movies(time_window=time_window, page=page)
            return [{
                'id': movie.id,
                'title': movie.title,
                'overview': movie.overview,
                'poster_path': f"https://image.tmdb.org/t/p/w500{movie.poster_path}",
                'release_date': movie.release_date,
                'vote_average': movie.vote_average,
                'vote_count': movie.vote_count
            } for movie in movies]
        except Exception as e:
            print(f"Error fetching trending movies: {str(e)}")
            return []

    def search_movies(self, query, page=1):
        """Search for movies by title."""
        try:
            movies = self.search.movies(query, page=page)
            return [{
                'id': movie.id,
                'title': movie.title,
                'overview': movie.overview,
                'poster_path': f"https://image.tmdb.org/t/p/w500{movie.poster_path}" if movie.poster_path else None,
                'release_date': movie.release_date if hasattr(movie, 'release_date') else None,
                'vote_average': movie.vote_average,
                'vote_count': movie.vote_count
            } for movie in movies]
        except Exception as e:
            print(f"Error searching movies: {str(e)}")
            return []

    def get_movie_details(self, movie_id):
        """Get detailed information about a specific movie."""
        try:
            movie = self.movie.details(movie_id)
            return {
                'id': movie.id,
                'title': movie.title,
                'overview': movie.overview,
                'poster_path': f"https://image.tmdb.org/t/p/w500{movie.poster_path}",
                'backdrop_path': f"https://image.tmdb.org/t/p/original{movie.backdrop_path}" if movie.backdrop_path else None,
                'release_date': movie.release_date,
                'vote_average': movie.vote_average,
                'vote_count': movie.vote_count,
                'genres': [genre['name'] for genre in movie.genres],
                'runtime': movie.runtime,
                'budget': movie.budget,
                'revenue': movie.revenue,
                'tagline': movie.tagline,
                'status': movie.status
            }
        except Exception as e:
            print(f"Error fetching movie details: {str(e)}")
            return None

    def get_similar_movies(self, movie_id):
        """Get movies similar to a specific movie."""
        try:
            similar = self.movie.similar(movie_id)
            return [{
                'id': movie.id,
                'title': movie.title,
                'overview': movie.overview,
                'poster_path': f"https://image.tmdb.org/t/p/w500{movie.poster_path}",
                'release_date': movie.release_date if hasattr(movie, 'release_date') else None,
                'vote_average': movie.vote_average
            } for movie in similar]
        except Exception as e:
            print(f"Error fetching similar movies: {str(e)}")
            return []

    def get_movie_credits(self, movie_id):
        """Get cast and crew information for a movie."""
        try:
            movie = self.movie.details(movie_id)
            credits = movie.credits
            cast = [{
                'id': person['id'],
                'name': person['name'],
                'character': person['character'],
                'profile_path': f"https://image.tmdb.org/t/p/w185{person['profile_path']}" if person['profile_path'] else None
            } for person in credits['cast'][:10]]  # Get top 10 cast members
            
            return {'cast': cast}
        except Exception as e:
            print(f"Error fetching movie credits: {str(e)}")
            return {'cast': []}
