import streamlit as st
import ingredient_search_module as ingredient_search

st.title("Ingredient Search")

# Ensure resources are loaded.
if "data" not in st.session_state:
    st.warning("Resources are not loaded yet.")
    st.stop()
else:
    data = st.session_state.data
    ingredients_df = st.session_state.ingredients_df
    model = st.session_state.model
    embeddings = st.session_state.embeddings

# Get the list of ingredients.
ingredient_list = ingredients_df["Translated"].to_list()

must_have = st.multiselect("Must Have:", options=ingredient_list)
nice_to_have = st.multiselect("Nice to Have:", options=ingredient_list)
exclude = st.multiselect("Exclude:", options=ingredient_list)

if st.button("Search"):
    results = ingredient_search.recommend_recipes(must_have, nice_to_have, exclude, data, model, embeddings)
    st.session_state.search_results = results
    st.markdown("### Search Completed")
    #st.page_link("recipe_results.py", label="View Recipe Results", icon="📋")
    st.switch_page("recipe_results.py")
