import pandas as pd
import pickle

# Load your CSV
csv_path = 'DataSets/tmdb_5000_movies.csv'
df = pd.read_csv(csv_path)

# Select relevant columns and rename for consistency
movies_list = df[['id', 'title', 'genres']].rename(columns={'id': 'movie_id'}).to_dict(orient='records')

# Save as pickle
with open('ML_Model/movies_dict.pkl', 'wb') as f:
    pickle.dump(movies_list, f)

print(f"Saved {len(movies_list)} movies to ML_Model/movies_dict.pkl") 