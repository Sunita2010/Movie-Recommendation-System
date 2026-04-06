import pandas as pd
import re

# Load dataset
# Note: Ensure 'movies.csv' is in the same folder as this script
movies = pd.read_csv(
    'movies.csv',
    nrows=3000,
    low_memory=True,
    on_bad_lines='skip'
)

movies['title'] = movies['title'].astype(str)
movies['genres'] = movies['genres'].fillna('')

# 🎯 Get all unique genres for the dropdown
def get_all_genres():
    genre_set = set()
    for g in movies['genres']:
        # Splits 'Action|Adventure' into ['Action', 'Adventure']
        for genre in g.split('|'):
            if genre.strip():
                genre_set.add(genre.strip())
    return sorted(list(genre_set))

# 🎯 Filter 1: Recommend by Movie Name
def recommend(movie_name):
    movie_name = movie_name.lower()
    # Clean the search string
    keyword = re.sub(r'[^a-zA-Z0-9 ]', '', movie_name)
    # Find movies containing that keyword
    filtered = movies[movies['title'].str.lower().str.contains(keyword, na=False)]
    return filtered['title'].head(10).tolist()

# 🎯 Filter 2: Recommend by Selected Genre
def recommend_by_genre(selected_genre):
    # Find movies where the genre string contains the selected genre
    filtered = movies[movies['genres'].str.contains(selected_genre, case=False, na=False)]
    return filtered['title'].head(10).tolist()
