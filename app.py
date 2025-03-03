import streamlit as st
import pickle
import pandas as pd
import requests

# Load movie list and similarity matrix
with open("movie_list.pkl", "rb") as f:
    movies = pickle.load(f)

with open("similarity.pkl", "rb") as f:
    similarity = pickle.load(f)

# Convert movies data into DataFrame
movies_df = pd.DataFrame(movies)

# TMDB API Key
TMDB_API_KEY = "579c2e71ddd805ca23c32e9b9d634e37"  # Replace with your actual API key

# Function to fetch movie poster using TMDB API
def fetch_poster(movie_title):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_title}"
    response = requests.get(url).json()
    
    if response["results"]:
        poster_path = response["results"][0].get("poster_path", "")
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
    
    return "https://via.placeholder.com/200x300?text=No+Image"

# Function to recommend movies
def recommend(movie_name):
    idx = movies_df[movies_df["title"] == movie_name].index[0]
    distances = similarity[idx]
    recommended_movies = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:6]

    movie_titles = [movies_df.iloc[i[0]].title for i in recommended_movies]
    movie_posters = [fetch_poster(title) for title in movie_titles]

    return movie_titles, movie_posters

# Streamlit UI
def main():
    st.set_page_config(page_title="WATCHIFY", layout="wide")
    
    # Welcome Section
    st.title("🎬 Welcome to WATCHIFY!")
    st.write("Find movies similar to your favorite ones.")
    
    # Sidebar Movie Selection
    st.sidebar.header("🔍 Search Your Favorite Movie")
    selected_movie = st.sidebar.selectbox("Choose a Movie:", movies["title"].values)
    
    if st.sidebar.button("Get Recommendations"):
        recommended_movies, recommended_posters = recommend(selected_movie)
        
        # Display Recommendations
        st.subheader(f"Movies Similar to: {selected_movie}")
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                st.image(recommended_posters[i], width=150)
                st.write(recommended_movies[i])

if __name__ == "__main__":
    main()

