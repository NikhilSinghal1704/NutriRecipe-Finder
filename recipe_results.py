import streamlit as st
import pandas as pd
import math

# Ensure search results exist
if "search_results" not in st.session_state or not st.session_state.search_results:
    st.error("No search results found. Please perform a search first.")
    st.stop()

data = st.session_state.data  # Full dataset
search_results = st.session_state.search_results  # List of (id, score) tuples

st.title("🍽️ Recommended Recipes")

# Convert search results into a DataFrame for easier filtering and sorting
results_df = pd.DataFrame(search_results, columns=["id", "score"])
results_df["score"] *= 100  # Convert match score to percentage
results_df = results_df.merge(data, left_on="id", right_index=True)

# **Sidebar Filters**
st.sidebar.header("🔍 Filter Recipes")

selected_diet = st.sidebar.selectbox("Filter by Diet:", ["All"] + sorted(results_df["diet"].dropna().unique().tolist()))
selected_cuisine = st.sidebar.selectbox("Filter by Cuisine:", ["All"] + sorted(results_df["cuisine"].dropna().unique().tolist()))
selected_course = st.sidebar.selectbox("Filter by Course:", ["All"] + sorted(results_df["course"].dropna().unique().tolist()))

# **Sorting Options**
sort_options = {
    "Match Score (Descending)": ("score", False),
    "Match Score (Ascending)": ("score", True),
    "Cooking Time (Ascending)": ("cook_time (in mins)", True),
    "Cooking Time (Descending)": ("cook_time (in mins)", False),
}
selected_sort = st.sidebar.selectbox("Sort by:", list(sort_options.keys()))

# **Apply Filters**
if selected_diet != "All":
    results_df = results_df[results_df["diet"] == selected_diet]
if selected_cuisine != "All":
    results_df = results_df[results_df["cuisine"] == selected_cuisine]
if selected_course != "All":
    results_df = results_df[results_df["course"] == selected_course]

# **Sorting**
sort_column, ascending_order = sort_options[selected_sort]
results_df = results_df.sort_values(by=sort_column, ascending=ascending_order)

# **Pagination Setup**
ITEMS_PER_PAGE = 10
total_pages = max(1, math.ceil(len(results_df) / ITEMS_PER_PAGE))
page = st.sidebar.number_input("Page:", min_value=1, max_value=total_pages, value=1, step=1)

# **Calculate Range for Pagination**
start_idx = (page - 1) * ITEMS_PER_PAGE
end_idx = min(start_idx + ITEMS_PER_PAGE, len(results_df))
paginated_results = results_df.iloc[start_idx:end_idx]

# **Show Total Pages**
st.write(f"📄 **Page {page} of {total_pages}**")

st.markdown("""
<style>
.recipe-card {
    display: flex;
    gap: 15px;
    padding: 15px;
    background-color: #1E1E1E;
    border-radius: 10px;
    box-shadow: 2px 2px 10px rgba(255,255,255,0.1);
    margin-bottom: 15px;
}
.recipe-card img {
    width: 100px;
    height: 100px;
    object-fit: cover;
    border-radius: 8px;
}
.recipe-info {
    flex: 1;
}
.recipe-title {
    font-size: 18px;
    font-weight: bold;
    color: #ffffff;
}
.recipe-details {
    color: #bbbbbb;
    font-size: 14px;
}
.recipe-description {
    max-height: 60px;
    overflow-y: auto;
    padding-right: 5px;
    color: #cccccc;
    font-size: 13px;
    background-color: rgba(255,255,255,0.1);
    padding: 5px;
    border-radius: 5px;
}
</style>
""", unsafe_allow_html=True)

# **Display Recipes with Scrollable Description**
for _, recipe in paginated_results.iterrows():
    description = recipe['description'] if pd.notna(recipe['description']) else "No description available."

    st.markdown(f"""
    <div class="recipe-card">
        <img src="{recipe['image_url']}" alt="Image not available">
        <div class="recipe-info">
            <a href="/recipe_detail?id={recipe['id']}" class="btn-container"><div class="recipe-title">{recipe['name']}</div></a>
            <div class="recipe-details">⏱️ <b>Cooking Time:</b> {recipe['cook_time (in mins)']} mins</div>
            <div class="recipe-details">🔥 <b>Match Score:</b> {recipe['score']:.2f}%</div>
            <div class="recipe-description">{description}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
