import pandas as pd

# Load small dataset (IMPORTANT)
movies = pd.read_csv(
    'movies.csv',
    nrows=3000,
    low_memory=True,
    on_bad_lines='skip'
)

# Clean data
movies['title'] = movies['title'].astype(str)
movies['genres'] = movies['genres'].fillna('')

# 🎯 Recommendation function (lightweight)
def recommend(movie):
    movie = movie.lower()

    # Find similar movies by genre
    try:
        genre = movies[movies['title'].str.lower() == movie]['genres'].values[0]
    except:
        return []

    similar_movies = movies[movies['genres'] == genre]

    # Remove same movie
    similar_movies = similar_movies[similar_movies['title'].str.lower() != movie]

    # Return top 10
    return similar_movies['title'].head(10).tolist()