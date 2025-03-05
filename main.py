import streamlit as st

# Must be the first Streamlit command!
st.set_page_config(
    page_title="Nutrisense - Nutritious Recipes",
    page_icon="🌱",
    layout="wide"
)

import time
import pandas as pd
from sentence_transformers import SentenceTransformer
from utils import auto_login

@st.cache_resource
def load_resources():
    progress_bar = st.progress(0)
    
    with st.spinner("📂 Loading datasets..."):
        data = pd.read_csv('Spoonacular_Analysis.csv')
        ingredients_df = pd.read_csv("Ingredients.csv")
        progress_bar.progress(33)
    
    with st.spinner("🤖 Loading AI Model..."):
        model = SentenceTransformer('all-MiniLM-L6-v2')
        progress_bar.progress(66)

    with st.spinner("🔍 Generating embeddings..."):
        embeddings = model.encode(data['Translated_Ingredients'].tolist())
        progress_bar.progress(100)
    
    progress_bar.empty()
    return data, ingredients_df, model, embeddings

# Load resources once and store in session state.
if "data" not in st.session_state:
    data, ingredients_df, model, embeddings = load_resources()
    st.session_state.data = data
    st.session_state.ingredients_df = ingredients_df
    st.session_state.model = model
    st.session_state.embeddings = embeddings

auto_login()

recipe_results_page    = st.Page("recipe_results.py", title="Recipe Results", icon="📋")
recipe_detail_page     = st.Page("recipe_detail.py", title="Recipe Detail", icon="🍲")
ingredient_search_page = st.Page("ingredient_search.py", title="Ingredient Search", icon="🔍")
    

if st.session_state.get("logged_in", False):
    # User is logged in: load the main recipe pages.
    user_profile_page      = st.Page("user_profile.py", title="User Profile", icon="👤")
    all_recipes_page       = st.Page("all_recipes.py", title="All Recipes", icon="📚")
    logout_page            = st.Page("logout.py", title="Logout", icon="🚪")
    
    pages = {
        "Account": [user_profile_page, logout_page],
        "Recipes": [ingredient_search_page, all_recipes_page, recipe_results_page, recipe_detail_page]
    }
else:
    # User is not logged in: show login and signup pages.
    login_page  = st.Page("login.py", title="Login", icon="🔑")
    signup_page = st.Page("signup.py", title="Sign Up", icon="📝")
    
    pages = [login_page,
             signup_page,
             recipe_results_page,
             recipe_detail_page,
            ]

# Create the multipage navigation.
pg = st.navigation(pages)
pg.run()

