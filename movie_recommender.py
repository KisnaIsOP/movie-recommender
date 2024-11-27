import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import seaborn as sns

class MovieRecommender:
    def __init__(self, movies_path, ratings_path):
        """Initialize the recommender system with movie and rating data paths."""
        try:
            self.movies = pd.read_csv(movies_path)
            self.ratings = pd.read_csv(ratings_path)
            self.content_similarity = None
            self.user_similarity = None
            self._prepare_content_based()
            self._prepare_collaborative()
        except Exception as e:
            raise Exception(f"Failed to initialize MovieRecommender: {str(e)}")

    def _prepare_content_based(self):
        """Prepare the content-based recommendation system."""
        # Create a bag of words for genres
        self.movies['genres'] = self.movies['genres'].fillna('')
        vectorizer = CountVectorizer(tokenizer=lambda x: x.split('|'))
        genre_matrix = vectorizer.fit_transform(self.movies['genres'])
        self.content_similarity = cosine_similarity(genre_matrix, genre_matrix)

    def _prepare_collaborative(self):
        """Prepare the collaborative filtering system."""
        # Create user-movie matrix
        self.user_movie_matrix = self.ratings.pivot(
            index='userId', 
            columns='movieId', 
            values='rating'
        ).fillna(0)
        
        # Compute user similarity
        self.user_similarity = cosine_similarity(self.user_movie_matrix)
        self.user_similarity_df = pd.DataFrame(
            self.user_similarity,
            index=self.user_movie_matrix.index,
            columns=self.user_movie_matrix.index
        )

    def content_based_recommendations(self, movie_title, num_recommendations=5):
        """Get content-based recommendations based on movie genres."""
        try:
            # Find movies matching the title
            matching_movies = self.movies[self.movies['title'].str.contains(
                movie_title, case=False, na=False)]
            
            if matching_movies.empty:
                raise ValueError(f"Movie '{movie_title}' not found in the database.")
            
            # Get the first matching movie
            idx = matching_movies.index[0]
            movie = matching_movies.iloc[0]
            
            # Get similarity scores
            sim_scores = list(enumerate(self.content_similarity[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            
            # Get recommendations
            recommendations = []
            for i in sim_scores[1:num_recommendations+1]:
                movie_data = {
                    'title': self.movies.iloc[i[0]]['title'],
                    'genres': self.movies.iloc[i[0]]['genres'],
                    'similarity': float(i[1])  # Convert numpy float to Python float
                }
                recommendations.append(movie_data)
            
            return recommendations
            
        except ValueError as e:
            raise e
        except Exception as e:
            raise Exception(f"Error getting content-based recommendations: {str(e)}")

    def collaborative_recommendations(self, user_id, num_recommendations=5):
        """Get collaborative filtering recommendations for a user."""
        try:
            if user_id not in self.user_movie_matrix.index:
                raise ValueError(f"User {user_id} not found in the database.")

            # Get user's similarity scores and weighted ratings
            user_scores = self.user_similarity_df[user_id]
            weighted_ratings = (user_scores.dot(self.user_movie_matrix) / 
                              user_scores.sum())
            
            # Exclude movies the user has already rated
            user_seen = self.user_movie_matrix.loc[user_id] > 0
            recommendations = weighted_ratings[~user_seen].sort_values(
                ascending=False).head(num_recommendations)
            
            # Format recommendations
            rec_list = []
            for movie_id, pred_rating in recommendations.items():
                movie_info = self.movies[self.movies['movieId'] == movie_id].iloc[0]
                rec_list.append({
                    'title': movie_info['title'],
                    'genres': movie_info['genres'],
                    'predicted_rating': float(pred_rating)  # Convert numpy float to Python float
                })
            
            return rec_list
            
        except ValueError as e:
            raise e
        except Exception as e:
            raise Exception(f"Error getting collaborative recommendations: {str(e)}")

    def get_top_rated_movies(self, min_reviews=100):
        """Get top-rated movies with a minimum number of reviews."""
        try:
            # Calculate average ratings and number of ratings per movie
            movie_stats = self.ratings.groupby('movieId').agg({
                'rating': ['count', 'mean']
            }).reset_index()
            
            movie_stats.columns = ['movieId', 'rating_count', 'rating_mean']
            
            # Filter movies with minimum number of reviews
            qualified = movie_stats[movie_stats['rating_count'] >= min_reviews]
            
            # Merge with movie information
            top_movies = qualified.merge(self.movies, on='movieId')
            top_movies = top_movies.sort_values('rating_mean', ascending=False)
            
            return top_movies[['title', 'genres', 'rating_count', 'rating_mean']]
            
        except Exception as e:
            raise Exception(f"Error getting top rated movies: {str(e)}")

    def visualize_ratings_distribution(self):
        """Visualize the distribution of movie ratings."""
        try:
            plt.figure(figsize=(10, 6))
            sns.histplot(data=self.ratings, x='rating', bins=10)
            plt.title('Distribution of Movie Ratings')
            plt.xlabel('Rating')
            plt.ylabel('Count')
            plt.show()
        except Exception as e:
            raise Exception(f"Error visualizing ratings distribution: {str(e)}")

# Example usage:
if __name__ == "__main__":
    try:
        # Initialize the recommender with MovieLens dataset
        recommender = MovieRecommender(
            'movies.csv',
            'ratings.csv'
        )
        
        # Get content-based recommendations
        print("\nContent-based recommendations for 'Toy Story':")
        recommendations = recommender.content_based_recommendations("Toy Story")
        for rec in recommendations:
            print(f"Movie: {rec['title']}")
            print(f"Genres: {rec['genres']}")
            print(f"Similarity Score: {rec['similarity'] * 100}%\n")
        
        # Get collaborative filtering recommendations
        print("\nCollaborative filtering recommendations for user 1:")
        recommendations = recommender.collaborative_recommendations(1)
        for rec in recommendations:
            print(f"Movie: {rec['title']}")
            print(f"Genres: {rec['genres']}")
            print(f"Predicted Rating: {rec['predicted_rating']}\n")
        
        # Get top-rated movies
        print("\nTop-rated movies:")
        top_movies = recommender.get_top_rated_movies(min_reviews=100).head()
        print(top_movies)
        
        # Visualize ratings distribution
        recommender.visualize_ratings_distribution()
        
    except Exception as e:
        print(f"Error: {str(e)}")
