import streamlit as st
import requests
from model import recommend, movies

# 🎬 Page config
st.set_page_config(page_title="Movie Recommender", layout="wide")

# 🎨 Custom CSS
st.markdown("""
    <style>
    body {
        background-color: #0e1117;
    }
    .title {
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        color: #ff4b4b;
    }
    .card {
        background-color: #1c1c1c;
        padding: 10px;
        border-radius: 12px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# 🎬 Title
st.markdown("<div class='title'>🎬 Movie Recommendation System</div>", unsafe_allow_html=True)

# 🎯 Movie dropdown
selected_movie = st.selectbox("Choose a movie", movies['title'].values)

# 🔑 TMDB API KEY (PUT YOUR KEY HERE)
API_KEY = "f91b3dec6078903951125470f6f28507"

# 🎥 Fetch poster
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

# ▶️ YouTube trailer
def get_trailer(movie_name):
    return f"https://www.youtube.com/results?search_query={movie_name}+trailer"

# 🎯 Button
if st.button("Recommend"):

    recommendations = recommend(selected_movie)

    st.subheader("🎥 Recommended Movies")

    cols = st.columns(5)

    for i in range(10):
        with cols[i % 5]:

            if i < len(recommendations):

                movie = recommendations[i]
                poster = fetch_poster(movie)

                st.markdown("<div class='card'>", unsafe_allow_html=True)

                # Poster or fallback
                if poster:
                    st.image(poster)
                else:
                    st.markdown("""
                        <div style="
                            height:220px;
                            display:flex;
                            align-items:center;
                            justify-content:center;
                            background:#333;
                            color:white;
                            border-radius:10px;">
                            Poster Not Available
                        </div>
                    """, unsafe_allow_html=True)

                # Movie title
                st.markdown(f"<p style='color:white'><b>{movie}</b></p>", unsafe_allow_html=True)

                # Trailer button
                st.markdown(f"[▶️ Watch Trailer]({get_trailer(movie)})")

                st.markdown("</div>", unsafe_allow_html=True)
