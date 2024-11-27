from movie_recommender import MovieRecommender

def main():
    # Initialize the recommender system
    print("Initializing Movie Recommender System...")
    recommender = MovieRecommender('movies.csv', 'ratings.csv')
    
    # Test content-based recommendations
    print("\n1. Content-based recommendations for 'Toy Story':")
    recommendations = recommender.content_based_recommendations("Toy Story")
    for rec in recommendations:
        print(f"Movie: {rec['title']}")
        print(f"Genres: {rec['genres']}")
        print(f"Similarity Score: {rec['similarity_score']}%\n")
    
    # Test collaborative filtering
    print("\n2. Collaborative filtering recommendations for user 1:")
    recommendations = recommender.collaborative_recommendations(1)
    for rec in recommendations:
        print(f"Movie: {rec['title']}")
        print(f"Genres: {rec['genres']}")
        print(f"Predicted Rating: {rec['predicted_rating']}\n")
    
    # Get top-rated movies
    print("\n3. Top 5 rated movies (with at least 100 reviews):")
    top_movies = recommender.get_top_rated_movies(min_reviews=100).head()
    print(top_movies)
    
    # Show rating distribution
    print("\n4. Displaying rating distribution (close the plot window to continue)...")
    recommender.visualize_ratings_distribution()

if __name__ == "__main__":
    main()
