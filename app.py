import streamlit as st
import requests
from model import recommend, movies, get_all_genres, recommend_by_genre

# 🎬 Page config
st.set_page_config(page_title="Movie Recommender", layout="wide")

# 🎨 Custom CSS for the Report
st.markdown("""
    <style>
    .title { text-align: center; font-size: 40px; font-weight: bold; color: #ff4b4b; margin-bottom: 30px; }
    .card { background-color: #1c1c1c; padding: 15px; border-radius: 12px; text-align: center; border: 1px solid #444; }
    .movie-name { color: white; font-weight: bold; margin-top: 10px; min-height: 50px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🎬 Movie Recommendation System</div>", unsafe_allow_html=True)

# 🎯 Sidebar Filter Selection
st.sidebar.header("Filter Settings")
mode = st.sidebar.radio("Search Preference:", ["By Movie Name", "By Genre"])

# TMDB API Key
API_KEY = "f91b3dec6078903951125470f6f28507"

def fetch_poster(movie_name):
    try:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_name}"
        response = requests.get(url).json()
        if response['results']:
            path = response['results'][0]['poster_path']
            return f"https://image.tmdb.org/t/p/w500/{path}"
    except:
        return None
    return None

# 🛠️ Search Logic
recommendations = []
search_target = ""

if mode == "By Movie Name":
    search_target = st.selectbox("Select a movie you like:", movies['title'].values)
    if st.button("Recommend Similar Movies"):
        recommendations = recommend(search_target)
else:
    all_genres = get_all_genres()
    search_target = st.selectbox("Select a genre:", all_genres)
    if st.button(f"Show Top {search_target} Movies"):
        recommendations = recommend_by_genre(search_target)

# 🎥 Displaying the Results
if recommendations:
    st.subheader(f"Results for: {search_target}")
    cols = st.columns(5)
    
    for i, movie in enumerate(recommendations):
        with cols[i % 5]:
            poster_url = fetch_poster(movie)
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            
            if poster_url:
                st.image(poster_url)
            else:
                st.markdown("<div style='height:200px; background:#333; color:white; display:flex; align-items:center; justify-content:center; border-radius:8px;'>No Image</div>", unsafe_allow_html=True)
            
            st.markdown(f"<div class='movie-name'>{movie}</div>", unsafe_allow_html=True)
            st.markdown(f"[▶️ Trailer](https://www.youtube.com/results?search_query={movie}+trailer)")
            st.markdown("</div>", unsafe_allow_html=True)
elif st.button and search_target:
    st.warning("No movies found for this selection.")
