import pickle

import pandas as pd
import requests
import streamlit as st

st.title("Movie Recommender System")

def fetch_movie_details(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=db4ea80d12abfa38f3ac579163d4ada6'
    )
    data = response.json()
    
    # Extract poster URL and movie link
    poster_url = "https://image.tmdb.org/t/p/w500" + data.get('poster_path', '')
    movie_link = f"https://www.themoviedb.org/movie/{movie_id}"
    
    return poster_url, movie_link


def recommend(movie):
    movie_index = movies[movies_lists == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    recommended_movies_posters = []
    recommended_movies_links = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        
        # Fetch poster and movie link in a single call
        poster_url, movie_link = fetch_movie_details(movie_id)
        recommended_movies_posters.append(poster_url)
        recommended_movies_links.append(movie_link)
    
    return recommended_movies, recommended_movies_posters, recommended_movies_links

movies=pickle.load(open('movies.pkl','rb'))
movies_lists=movies['title'].values

similarity=pickle.load(open('similarity.pkl','rb'))
Selected_Movie_Name = st.selectbox(
'How would you like to be contacted?',
(movies_lists))


if st.button('Recommend'):
    names, posters, links = recommend(Selected_Movie_Name)
    col1, col2, col3, col4, col5 = st.columns(5, gap="medium")
    
    # Helper function to display clickable image with a link
    def display_movie(col, name, poster, link):
        with col:
            # HTML for a clickable image
            clickable_image = f"""
            <a href="{link}" target="_blank">
                <img src="{poster}" alt="{name}" style="width:100%; border-radius:10px;">
            </a>
            """
            st.markdown(clickable_image, unsafe_allow_html=True)
            st.text(name)  # Movie title below the image
    
    # Display recommendations in columns
    display_movie(col1, names[0], posters[0], links[0])
    display_movie(col2, names[1], posters[1], links[1])
    display_movie(col3, names[2], posters[2], links[2])
    display_movie(col4, names[3], posters[3], links[3])
    display_movie(col5, names[4], posters[4], links[4])


