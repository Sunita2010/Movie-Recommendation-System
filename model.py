import pandas as pd
import re

# Load dataset
movies = pd.read_csv(
    'movies.csv',
    nrows=3000,
    low_memory=True,
    on_bad_lines='skip'
)

movies['title'] = movies['title'].astype(str)
movies['genres'] = movies['genres'].fillna('')

# 🎯 Get all unique genres
def get_all_genres():
    genre_set = set()
    
    for g in movies['genres']:
        for genre in g.split('|'):
            genre_set.add(genre.strip())
    
    return sorted(list(genre_set))


# 🎯 Recommend function with optional genre filter
def recommend(movie, selected_genres=None):
    movie = movie.lower()

    # Clean keyword
    keyword = re.sub(r'[^a-zA-Z0-9 ]', '', movie)

    # 🔍 Find matching movies (series logic)
    filtered_movies = movies[movies['title'].str.lower().str.contains(keyword, na=False)]

    # 🎯 Apply genre filter if selected
    if selected_genres:
        def match_genre(g):
            return any(gen in g for gen in selected_genres)
        
        filtered_movies = filtered_movies[filtered_movies['genres'].apply(match_genre)]

    if filtered_movies.empty:
        return []

    return filtered_movies['title'].head(10).tolist()
