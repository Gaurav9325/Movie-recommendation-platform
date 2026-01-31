from flask import Flask, render_template, request
import pandas as pd
from difflib import SequenceMatcher

app = Flask(__name__)

# Load movies
movies = pd.read_csv("movies.csv")

def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

def recommend_movies(movie_name):
    movie_name = movie_name.lower()

    if movie_name not in movies['title'].str.lower().values:
        return None

    selected_description = movies[movies['title'].str.lower() == movie_name]['description'].values[0]

    movies['score'] = movies['description'].apply(lambda x: similarity(selected_description, x))

    results = movies.sort_values(by="score", ascending=False)

    recommended = results.iloc[1:6]['title'].tolist()

    return recommended


@app.route("/", methods=["GET", "POST"])
def home():
    recommendations = []
    error = ""

    # All movies list for suggestion
    all_movies = movies["title"].tolist()
    suggestions = []

    if request.method == "POST":
        movie_name = request.form.get("movie", "")

        # 🔥 Auto-suggestion logic
        if movie_name:
            suggestions = [m for m in all_movies if movie_name.lower() in m.lower()][:5]

        # 🔥 Recommendation logic
        result = recommend_movies(movie_name)

        if result is None:
            error = "Movie not found in database. Try another movie."
        else:
            recommendations = result

    # ⭐ THIS IS THE RETURN LINE YOU MUST UPDATE
    return render_template(
        "index.html",
        recommendations=recommendations,
        error=error,
        suggestions=suggestions   # ← NEW
    )



if __name__ == "__main__":
    app.run(debug=False)

