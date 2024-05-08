import pickle
import streamlit as st
import requests
import pandas as pd

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data.get('poster_path')
    if poster_path:
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        full_path = "https://via.placeholder.com/500x750?text=No+Poster+Available"
    return full_path

def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
    except IndexError:
        st.error("Movie not found in the database. Please select a different movie.")
        return [], []

    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

# Page layout settings
st.set_page_config(page_title='Movie Recommender', layout='wide')

# Load data
movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

# CSS for background image
import streamlit as st

background_style = """
    <style>
    [data-testid="stAppViewBlockContainer"]{
    background-image:url(https://i.ibb.co/6RXXHQC/image.jpg);
    background-size:cover;
    }
  [class="main st-emotion-cache-uf99v8 ea3mdgi8"] {
   background-image:url(https://i.ibb.co/6RXXHQC/image.jpg);
    background-size:cover;
         background-color:rgba(0,0,0,0);
        }
   [data-testid="stHeader"]{
   background-color:rgba(0,0,0,0);
   }
   [data-testid="IframeResizerAnchor"]{
    background-color:rgba(0,0,0,0);
   }
   [data-testid="stFooter"]{
   background-color:rgba(0,0,0,0);
   }
    
    </style>
"""

# Display the background style
st.markdown(background_style, unsafe_allow_html=True)

st.title('Movie Recommender System')



# Sidebar
selected_movie = st.sidebar.selectbox(
    "Select a movie",
    movies['title'].values
)

if st.sidebar.button('Get Recommendations'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    if recommended_movie_names:
        st.sidebar.subheader('Top Recommendations')
        for i, (name, poster) in enumerate(zip(recommended_movie_names, recommended_movie_posters)):
            st.sidebar.text(name)
            st.sidebar.image(poster, use_column_width=True)
    else:
        st.sidebar.error('No recommendations available.')

# Main content
st.write("### Selected Movie:")
st.write(selected_movie)

# Display movie details (if available)
selected_movie_details = movies[movies['title'] == selected_movie]
if not selected_movie_details.empty:
    st.write("### Movie Details:")
    st.write("**Movie ID:**", selected_movie_details['movie_id'].values[0])
    st.write("**Title:**", selected_movie_details['title'].values[0])
    st.write("**Tags:**", selected_movie_details['tags'].values[0])
else:
    st.write("No details available for this movie.")
