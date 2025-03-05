import streamlit as st
from utils import get_unsplash_photo_url
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title("Recipe Detail")

# 1. Retrieve recipe index from query parameters using st.query_params
query_params = st.query_params
recipe_id = query_params.get("id", None)

recipe = None

if recipe_id is not None:
    try:
        recipe_id = int(recipe_id)
    except ValueError:
        st.error("Invalid recipe index in URL.")
        st.stop()
        
    # Ensure data is available
    if "data" not in st.session_state:
        st.error("No data found in session. Please go back and select a recipe.")
        st.stop()
    
    data = st.session_state.data
    if recipe_id < 0 or recipe_id >= len(data):
        st.error("Recipe index out of range.")
        st.stop()
    
    row = data.iloc[recipe_id]
    recipe = row.to_dict()

# 2. Fallback to st.session_state.selected_recipe if no valid index is provided.
if recipe is None:
    if "selected_recipe" in st.session_state:
        recipe = st.session_state.selected_recipe
    else:
        st.warning("No recipe selected. Please go back and choose a recipe.")
        st.stop()

# 3. Render the recipe details.

# Title: Use the recipe name
st.markdown(f"<h1 style='color:#2C3E50;'>{recipe.get('name', 'N/A')}</h1>", unsafe_allow_html=True)

# Container for image and description side by side.
st.markdown("""
<style>
.recipe-detail-container {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    align-items: center;
    background-color: #F5F5F5;
    padding: 20px;
    border-radius: 10px;
}
.recipe-detail-image {
    flex: 1;
    min-width: 300px;
}
.recipe-detail-description {
    flex: 2;
    min-width: 300px;
    font-size: 16px;
    color: #34495E;
}
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="recipe-detail-container">
    <div class="recipe-detail-image">
        <img src="{recipe.get('image_url', '')}" alt="Recipe Image" style="width:100%; border-radius:8px;">
    </div>
    <div class="recipe-detail-description">
        <p>{recipe.get('translated_description', 'No description available.')}</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# Extended Ingredients Table or Ingredient Grid
display_extended_ingredients = False
extended_ingredients = []

spoonacular_flag = 0

if not pd.isna(recipe['spoonacular_analysis']):
    import ast
    spoonacular_flag = 1
    try:
        analysis = ast.literal_eval(recipe['spoonacular_analysis'])
        caloric_breakdown = analysis.get('nutrition', None).get('caloricBreakdown', None)
        nutrients_list = analysis.get('nutrition', None).get('nutrients', None)
        extended_ingredients = analysis.get('extendedIngredients', None)
        if extended_ingredients:
            display_extended_ingredients = True
    except Exception as e:
        st.warning("Error parsing Spoonacular analysis. Showing default ingredients.")

if display_extended_ingredients:
    st.markdown("<h2 style='color:#27AE60;'>Ingredients</h2>", unsafe_allow_html=True)
    
    df = pd.DataFrame(extended_ingredients)
    
    # Convert the 'meta' list to a comma-separated string
    df['meta'] = df['meta'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)
    
    # Update the 'image' column to render an image using Spoonacular's CDN
    df['image'] = df['image'].apply(lambda img: f"<img src='https://spoonacular.com/cdn/ingredients_100x100/{img}' width='50'/>" if img else '')
    
    # Keep relevant columns
    df = df[['image', 'name', 'amount', 'unit', 'meta']]
    
    # Render the table as HTML without index and allow HTML rendering
    st.markdown(df.to_html(escape=False, index=False), unsafe_allow_html=True)

    
else:
    st.markdown("<h2 style='color:#27AE60;'>Ingredients</h2>", unsafe_allow_html=True)
    ingredients = recipe.get('listed_translated_ingredients', [])
    if isinstance(ingredients, str):
        # Assume comma-separated if not a list.
        ingredients = [ing.strip() for ing in ingredients.split(",") if ing.strip()]

    cols = st.columns(4)
    for i, ing in enumerate(ingredients):
        with cols[i % 4]:
            # Use Unsplash placeholder image based on the ingredient name.
            img_url = get_unsplash_photo_url(ing)
            if img_url is None:
                # Provide a default image URL or skip showing the image
                img_url = "https://www.arisoapp.com/img/Ingredient.jpg"
            st.image(img_url, use_container_width=True)
            st.markdown(f"<p style='text-align:center;'>{ing}</p>", unsafe_allow_html=True)


st.markdown("<hr>", unsafe_allow_html=True)

# Prep Section: Display the list of ingredients quantity and prep time.
st.markdown("<h3 style='color:#2C3E50;'>Prep</h3>", unsafe_allow_html=True)
prep_list = recipe.get('listed_translated_ingredients_quantity', '')
if isinstance(prep_list, str):
    # Split by newline or comma.
    if "\n" in prep_list:
        prep_items = [item.strip() for item in prep_list.split("\n") if item.strip()]
    else:
        prep_items = [item.strip() for item in prep_list.split(",") if item.strip()]
else:
    prep_items = prep_list

for item in prep_items:
    st.markdown(f"- {item}")

st.markdown(f"**Prep Time:** {recipe.get('prep_time (in mins)', 'N/A')} mins", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

st.markdown(f"**Cook Time:** {recipe.get('cook_time (in mins)', 'N/A')} mins", unsafe_allow_html=True)

# Instructions Section: Display translated instructions.
st.markdown("<h3 style='color:#2980B9;'>Instructions</h3>", unsafe_allow_html=True)
st.markdown(recipe.get('translated_instructions', 'No instructions available.'), unsafe_allow_html=True)

if spoonacular_flag == 1 and caloric_breakdown:
    st.markdown("<h2 style='color:#27AE60;'>Caloric Breakdown</h2>", unsafe_allow_html=True)
    
    # Extract labels and values from the caloricBreakdown dictionary
    labels = list(caloric_breakdown.keys())
    sizes = list(caloric_breakdown.values())

    sizes = np.array(sizes, dtype=float)
    sizes = np.nan_to_num(sizes, nan=0.0)
    sizes = sizes.tolist()
    
    # Create a pie chart
    fig, ax = plt.subplots(figsize=(2, 2))
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#FF9999','#99FF99','#9999FF'])
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    st.pyplot(fig)
else:
    st.info("Caloric breakdown data not available.")

if spoonacular_flag == 1 and nutrients_list:
    df_nutrients = pd.DataFrame(nutrients_list)
    selected_cols = ['name', 'amount', 'unit', 'percentOfDailyNeeds']
    df_nutrients = df_nutrients[selected_cols]
    
    # Format the 'amount' column: format as one decimal place without commas.
    df_nutrients['amount'] = df_nutrients['amount'].apply(
        lambda x: f"{x:.2f}" if isinstance(x, (int, float)) else x
    )

    df_nutrients['percentOfDailyNeeds'] = df_nutrients['percentOfDailyNeeds'].apply(
        lambda x: f"{x:.2f}" if isinstance(x, (int, float)) else x
    )
    
    st.markdown("<h2 style='color:#27AE60;'>Nutritional Information</h2>", unsafe_allow_html=True)
    st.table(df_nutrients)
else:
    st.info("Nutrient data not available.")