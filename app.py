import pickle
import streamlit as st
import requests
import pandas as pd  # Ensure pandas is imported
from rapidfuzz import process

# Load the movie data and similarity matrix
movies_dict = pickle.load(open('./ML_Model/movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)  # Convert dictionary to DataFrame

similarity = pickle.load(open('./ML_Model/similarity.pkl', 'rb'))

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return None  # Return None if no poster is found

def fetch_tmdb_reviews(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/reviews?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('results', [])
    return []

def recommend(movie):
    # Use fuzzy matching to find the closest movie title
    titles = movies['title'].tolist()
    match, score, idx = process.extractOne(movie, titles, score_cutoff=60)
    if match is None:
        return [], []  # Return empty lists if the movie is not found
    index = movies[movies['title'] == match].index[0]
    distances = sorted(enumerate(similarity[index]), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:  # Skip the first element as it's the selected movie itself
        movie_id = movies.iloc[i[0]].movie_id
        poster_url = fetch_poster(movie_id)
        if poster_url:  # Only add if a valid poster is found
            recommended_movie_posters.append(poster_url)
            recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

# Streamlit UI
st.header('Movie Recommender System')

movie_list = movies['title'].tolist()
movie_input = st.text_input('Type a movie name:')
suggestions = []
selected_movie = None
if movie_input:
    # Fuzzy match top 5 suggestions
    results = process.extract(movie_input, movie_list, limit=5, scorer=process.fuzz.WRatio)
    suggestions = [title for title, score, idx in results if score > 50]
    if movie_input in movie_list:
        selected_movie = movie_input
    elif suggestions:
        selected_movie = suggestions[0]

if suggestions and (not selected_movie or movie_input != selected_movie):
    st.write('Suggestions:')
    for s in suggestions:
        st.write(f'- {s}')

if st.button('Show Recommendation') and selected_movie:
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    if not recommended_movie_names:
        st.error('Movie not found in the database. Please select a valid movie.')
    else:
        cols = st.columns(4)
        for col, name, poster in zip(cols, recommended_movie_names, recommended_movie_posters):
            with col:
                st.text(name)
                st.image(poster)
                movie_id = movies[movies['title'] == name].iloc[0].movie_id
                tmdb_reviews = fetch_tmdb_reviews(movie_id)
                if tmdb_reviews:
                    st.write('TMDb Reviews:')
                    for review in tmdb_reviews[:3]:
                        st.markdown(f"**{review['author']}**: {review['content'][:300]}{'...' if len(review['content']) > 300 else ''}")
