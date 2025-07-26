import numpy as np
import pandas as pd
from flask import Flask, request, render_template, flash, redirect, url_for, jsonify
from flask_login import LoginManager, login_required, current_user
import pickle
from models import db, User, Review, Rating
from auth import auth
import ast
import requests
from datetime import datetime

TMDB_API_KEY = "06f75ebed790f32f3bf8e92c2f46101d"
TMDB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

# Function to fetch poster URL from TMDB
def fetch_poster(title):
    params = {
        "api_key": TMDB_API_KEY,
        "query": title,
    }
    try:
        response = requests.get(TMDB_SEARCH_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            if results and results[0].get("poster_path"):
                return TMDB_IMAGE_BASE + results[0]["poster_path"]
    except Exception as e:
        print(f"TMDB fetch error for '{title}': {e}")
    return "https://via.placeholder.com/300x450?text=No+Image"

# Function to get average rating for a movie
def get_movie_rating(movie_title):
    reviews = Review.query.filter_by(movie_title=movie_title).all()
    if reviews:
        avg_rating = sum(review.rating for review in reviews) / len(reviews)
        return round(avg_rating, 1)
    return None

# Function to get reviews for a movie
def get_movie_reviews(movie_title, limit=3):
    reviews = Review.query.filter_by(movie_title=movie_title).order_by(Review.created_at.desc()).limit(limit).all()
    return reviews

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register blueprints
app.register_blueprint(auth)

# Load the movie recommendation model
with open("ML_Model/movies_dict.pkl", "rb") as f:
    movies_list = pickle.load(f)
movies_df = pd.DataFrame(movies_list)

# Load the similarity matrix
similarity = pickle.load(open("ML_Model/similarity.pkl", "rb"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    movie_input = request.form["movie_name"]

    if movie_input not in movies_df['title'].values:
        error_message = "Movie not found in database. Please try another movie."
        return render_template("index.html", error_message=error_message)
    else:
        idx = movies_df[movies_df['title'] == movie_input].index[0]
        sim_scores = list(enumerate(similarity[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:6]
        movie_indices = [i[0] for i in sim_scores]

        recommended_movies = []
        for i in movie_indices:
            row = movies_df.iloc[i]
            genres = ""
            try:
                genres_list = ast.literal_eval(row['genres'])
                genres = ", ".join([g['name'] for g in genres_list])
            except Exception:
                genres = str(row['genres'])
            overview = row['overview'] if 'overview' in row and pd.notnull(row['overview']) else ""
            # Only add <br> if both genres and overview exist
            if genres and overview:
                description = f"Genres: {genres}<br>{overview}"
            elif genres:
                description = f"Genres: {genres}"
            elif overview:
                description = overview
            else:
                description = ""
            poster_url = fetch_poster(row['title'])

            # Get rating and reviews for this movie
            avg_rating = get_movie_rating(row['title'])
            reviews = get_movie_reviews(row['title'])

            recommended_movies.append({
                "title": row['title'],
                "poster_link": poster_url,
                "overview": description,
                "avg_rating": avg_rating,
                "reviews": reviews
            })

        return render_template("index.html", recommended_movies=recommended_movies)

@app.route("/submit_review", methods=["POST"])
@login_required
def submit_review():
    data = request.get_json()
    movie_title = data.get('movie_title')
    movie_id = data.get('movie_id')
    rating = float(data.get('rating'))
    content = data.get('content')

    if not movie_title or not content or rating < 1 or rating > 5:
        return jsonify({"success": False, "message": "Invalid data"})

    # Check if user already reviewed this movie
    existing_review = Review.query.filter_by(
        user_id=current_user.id,
        movie_title=movie_title
    ).first()

    if existing_review:
        # Update existing review
        existing_review.content = content
        existing_review.rating = rating
        existing_review.created_at = datetime.utcnow()
    else:
        # Create new review
        review = Review(
            movie_title=movie_title,
            movie_id=movie_id,
            content=content,
            rating=rating,
            user_id=current_user.id
        )
        db.session.add(review)

    db.session.commit()

    # Get updated average rating
    avg_rating = get_movie_rating(movie_title)

    return jsonify({
        "success": True,
        "message": "Review submitted successfully!",
        "avg_rating": avg_rating
    })

@app.route("/protected")
@login_required
def protected():
    return "This is a protected page. You are logged in as: " + current_user.username

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
