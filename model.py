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
    # 1. Find the selected movie in our database
    selected_movie_row = movies[movies['title'] == movie_name]
    
    if selected_movie_row.empty:
        return []

    # 2. Get the genres of that movie (e.g., "Action|Adventure")
    selected_genres = selected_movie_row.iloc[0]['genres']
    
    # 3. Find other movies that share at least one genre
    # We exclude the selected movie itself so it doesn't recommend itself
    genre_list = selected_genres.split('|')
    
    # Create a filter: check if any of the movie's genres are in our target list
    pattern = '|'.join(genre_list)
    recommendations = movies[
        (movies['genres'].str.contains(pattern, case=False, na=False)) & 
        (movies['title'] != movie_name)
    ]
    
    # 4. Return the top 10 results
    return recommendations['title'].head(10).tolist()

# 🎯 Filter 2: Recommend by Selected Genre
def recommend_by_genre(selected_genre):
    # Find movies where the genre string contains the selected genre
    filtered = movies[movies['genres'].str.contains(selected_genre, case=False, na=False)]
    return filtered['title'].head(10).tolist()
