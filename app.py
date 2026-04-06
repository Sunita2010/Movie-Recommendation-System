import streamlit as st
import requests
# Ensure these functions exist in your model.py
from model import recommend, movies, get_all_genres, recommend_by_genre 

# 🎬 Page config
st.set_page_config(page_title="Movie Recommender", layout="wide")

# 🎨 Custom CSS for a professional Look
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .title { text-align: center; font-size: 45px; font-weight: bold; color: #ff4b4b; margin-bottom: 20px; }
    .card { background-color: #1c1c1c; padding: 15px; border-radius: 15px; text-align: center; height: 100%; border: 1px solid #333; }
    .movie-title { color: white; font-size: 16px; margin-top: 10px; height: 40px; overflow: hidden; }
    </style>
""", unsafe_allow_html=True)

# 🎬 Title
st.markdown("<div class='title'>🎬 Movie Recommendation System</div>", unsafe_allow_html=True)

# 🎯 Select Mode (Sidebar keeps the UI clean)
st.sidebar.header("Filter Options")
mode = st.sidebar.radio("Choose Recommendation Type", ["By Movie", "By Genre"], key="main_mode")

# TMDB API Configuration
API_KEY = "f91b3dec6078903951125470f6f28507"

def fetch_poster(movie_name):
    try:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_name}"
        data = requests.get(url).json()
        if 'results' in data and len(data['results']) > 0:
            poster_path = data['results'][0]['poster_path']
            if poster_path:
                return "https://image.tmdb.org/t/p/w500/" + poster_path
    except:
        return None
    return None

def get_trailer(movie_name):
    return f"https://www.youtube.com/results?search_query={movie_name}+trailer"

# 🛠️ Logic for Inputs
recommendations = []

if mode == "By Movie":
    selected_movie = st.selectbox("Type or select a movie you like:", movies['title'].values)
    if st.button("Show Recommendations"):
        recommendations = recommend(selected_movie)

else:
    all_genres = get_all_genres()
    selected_genre = st.selectbox("Choose a genre:", all_genres)
    if st.button("Show Recommendations"):
        # Ensure your model.py has a function to filter by genre
        recommendations = recommend_by_genre(selected_genre)

# 🎥 Display Results
if recommendations:
    st.subheader(f"🎥 Top Recommendations for {selected_movie if mode == 'By Movie' else selected_genre}")
    
    # Display in a grid of 5 columns
    cols = st.columns(5)
    
    for i, movie in enumerate(recommendations[:10]): # Limit to top 10
        with cols[i % 5]:
            poster = fetch_poster(movie)
            
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            
            if poster:
                st.image(poster, use_container_width=True)
            else:
                st.markdown("<div style='height:250px; background:#333; border-radius:10px; display:flex; align-items:center; justify-content:center;'>No Poster</div>", unsafe_allow_html=True)
            
            st.markdown(f"<p class='movie-title'><b>{movie}</b></p>", unsafe_allow_html=True)
            st.markdown(f"[▶️ Trailer]({get_trailer(movie)})")
            st.markdown("</div>", unsafe_allow_html=True)
