import pickle
import pandas as pd
import numpy as np

def test_recommendation_system():
    print("Testing Movie Recommendation System")
    print("=" * 40)
    
    try:
        # Load the data
        print("Loading movie data...")
        movies_dict = pickle.load(open("ML_Model/movies_dict.pkl", "rb"))
        similarity = pickle.load(open("ML_Model/similarity.pkl", "rb"))
        
        # Create DataFrame properly
        movies_df = pd.DataFrame(list(movies_dict.items()), columns=['movie_id', 'description'])
        movies_df['movie_id'] = pd.to_numeric(movies_df['movie_id'], errors='coerce')
        movies_df = movies_df.dropna()  # Remove any rows with invalid movie IDs
        
        # Load original movies CSV
        original_movies = pd.read_csv('DataSets/tmdb_5000_movies.csv')
        # Create a mapping from movie ID to title
        id_to_title = dict(zip(original_movies['id'], original_movies['title']))
        
        # Add titles to our movies DataFrame
        movies_df['title'] = movies_df['movie_id'].map(id_to_title)
        movies_df = movies_df.dropna(subset=['title'])  # Remove rows where title is NaN
        
        print(f"✓ Loaded {len(movies_df)} movies")
        print(f"✓ Similarity matrix shape: {similarity.shape}")
        
        if len(movies_df) == 0:
            print("❌ No movies loaded. Check data structure.")
            return False
        
        # Test with a sample movie
        sample_movie = movies_df['title'].iloc[0]
        print(f"\nTesting with movie: {sample_movie}")
        
        # Find movie index
        idx = movies_df[movies_df['title'] == sample_movie].index[0]
        
        # Get recommendations
        sim_scores = list(enumerate(similarity[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:6]  # Top 5 similar movies
        movie_indices = [i[0] for i in sim_scores]
        recommended_movies = movies_df.iloc[movie_indices]['title'].values.tolist()
        
        print(f"✓ Found {len(recommended_movies)} recommendations")
        print("\nRecommended movies:")
        for i, movie in enumerate(recommended_movies, 1):
            print(f"  {i}. {movie}")
        
        print("\n✅ Recommendation system is working correctly!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    test_recommendation_system() 