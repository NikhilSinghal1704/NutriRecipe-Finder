import streamlit as st
import math

st.title("All Recipes")

if "data" not in st.session_state:
    st.write("No recipes found. Try searching!")
    st.stop()
else:
    data = st.session_state.data
    
# Define diet categories mapping
diet_categories = {
    "Veg": [
        "Diabetic Friendly",
        "Gluten Free",
        "High Protein Vegetarian",
        "No Onion No Garlic (Sattvic)",
        "Sugar Free Diet",
        "Vegan",
        "Vegetarian"
    ],
    "Egg": [
        "Eggetarian"
    ],
    "Non-Veg": [
        "High Protein Non Vegetarian",
        "Non Vegeterian"
    ]
}

# Determine allowed diet filter options based on the user's profile.
# Default to Veg if no profile is found.
if "profile" in st.session_state and st.session_state.profile:
    user_diet = st.session_state.profile.get("diet", "Veg")
else:
    user_diet = "Veg"

if user_diet == "Veg":
    allowed_diets = diet_categories["Veg"]
elif user_diet == "Egg":
    allowed_diets = diet_categories["Veg"] + diet_categories["Egg"]
elif user_diet == "Non-Veg":
    allowed_diets = ["All"] + diet_categories["Veg"] + diet_categories["Egg"] + diet_categories["Non-Veg"]
else:
    allowed_diets = []  # fallback

# Build the diet filter options: "All" represents all allowed diets.
diet_filter_options = allowed_diets

# Sidebar filters.
st.sidebar.header("🔍 Filter Recipes")
selected_diet = st.sidebar.selectbox("Filter by Diet:", diet_filter_options, index=0)

selected_cuisine = st.sidebar.selectbox("Filter by Cuisine:", ["All"] + sorted(data["cuisine"].dropna().unique().tolist()))
selected_course = st.sidebar.selectbox("Filter by Course:", ["All"] + sorted(data["course"].dropna().unique().tolist()))

filtered_data = data.copy()
if selected_diet != "All":
    filtered_data = filtered_data[filtered_data["diet"] == selected_diet]
if selected_cuisine != "All":
    filtered_data = filtered_data[filtered_data["cuisine"] == selected_cuisine]
if selected_course != "All":
    filtered_data = filtered_data[filtered_data["course"] == selected_course]

# Pagination setup.
ITEMS_PER_PAGE = 100
total_pages = max(1, math.ceil(len(filtered_data) / ITEMS_PER_PAGE))
page = st.sidebar.number_input("Page:", min_value=1, max_value=total_pages, value=1, step=1)

start_idx = (page - 1) * ITEMS_PER_PAGE
end_idx = min(start_idx + ITEMS_PER_PAGE, len(filtered_data))
recipes_to_display = filtered_data.iloc[start_idx:end_idx]

# Card layout CSS.
st.markdown("""
<style>
.recipe-card {
    height: 380px;
    padding: 10px;
    text-align: center;
    background-color: #1E1E1E;
    border-radius: 10px;
    box-shadow: 2px 2px 10px rgba(255,255,255,0.1);
    margin-bottom: 15px;
}
.recipe-card img {
    width: 100%;
    height: 200px;
    object-fit: cover;
    border-radius: 8px;
}
.recipe-title {
    font-size: 16px;
    font-weight: bold;
    color: #ffffff;
    margin-top: 10px;
}
.recipe-time {
    color: #bbbbbb;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# Display recipes in a grid.
cols = st.columns(4)
for i, (id, recipe) in enumerate(recipes_to_display.iterrows()):
    with cols[i % 4]:
        with st.container():
            # Render the card with position: relative
            st.markdown(f"""
            <div class="recipe-card">
                <img src="{recipe['image_url']}" alt="Image not available">
                <div class="recipe-title">{recipe['name']}</div>
                <div class="recipe-time"><b>Time:</b> {recipe['prep_time (in mins)'] + recipe['cook_time (in mins)']} mins</div>
                <a href="recipe_detail?id={id}" class="btn-container">
                    <button> 
                        View Details
                    </button>
                </a>
            </div>
            """, unsafe_allow_html=True)