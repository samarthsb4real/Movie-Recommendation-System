import streamlit as st
import pickle
import requests

# Creating the API function
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')

    if poster_path:
        full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
        return full_path
    else:
        return ""

# Creating the recommend function
def recommend(movie, num_recommendations):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])[1:num_recommendations + 1]
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances:
        movie_id = movies.iloc[i[0]]['id']
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]]['title'])

    return recommended_movie_names, recommended_movie_posters

st.title('Movie Recommendation System')

# Load the similarity matrix and movies DataFrame from pickle files
try:
    with open('similarity.pkl', 'rb') as f:
        similarity = pickle.load(f)
    with open('movies.pkl', 'rb') as f:
        movies = pickle.load(f)
except FileNotFoundError as e:
    st.error(f"File not found: {e}")
    st.stop()
except pickle.UnpicklingError as e:
    st.error(f"Error unpickling file: {e}")
    st.stop()
except Exception as e:
    st.error(f"An unexpected error occurred: {e}")
    st.stop()

selected = st.selectbox('Enter a movie title', movies['title'].values)
num_recommendations = st.number_input(label='How many similar movies do you want to recommend?', min_value=1, max_value=10, value=5)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected, num_recommendations)
    columns = st.columns(num_recommendations)

    for idx, col in enumerate(columns):
        col.text(recommended_movie_names[idx])
        col.image(recommended_movie_posters[idx])
