import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def get_embedding(text,model):
    """Convert a text input into an embedding vector."""
    return model.encode(text)

def recommend_recipes(user_must_have, user_nice_to_have, user_exclude, data, model, embeddings):
    """
    Recommend recipes based on must-have, nice-to-have, and exclude ingredients.

    user_must_have: List of required ingredients
    user_nice_to_have: List of optional but preferred ingredients
    user_exclude: List of ingredients to avoid
    data: The DataFrame containing recipes
    embeddings: The precomputed embeddings for recipes
    """

    # Combine user input into a single query stringddd
    must_have_str = ', '.join(user_must_have)
    nice_to_have_str = ', '.join(user_nice_to_have)

    # Generate embeddings for user input
    must_have_embedding = get_embedding(must_have_str, model)
    nice_to_have_embedding = get_embedding(nice_to_have_str, model) if user_nice_to_have else None

    # Compute similarity between must-have ingredients and recipes
    must_have_similarities = cosine_similarity([must_have_embedding], embeddings)[0]
    
    # If nice-to-have is given, compute additional similarity
    nice_to_have_similarities = cosine_similarity([nice_to_have_embedding], embeddings)[0] if nice_to_have_embedding is not None else np.zeros(len(embeddings))

    # Filter recipes based on must-have and exclude ingredients
    filtered_indices = []
    for i, ingredients in enumerate(data['listed_translated_ingredients']):
        # Ensure must-have ingredients are present
        if not all(ing in ingredients for ing in user_must_have):
            continue
        # Ensure excluded ingredients are NOT present
        if any(ing in ingredients for ing in user_exclude):
            continue
        # If recipe passes both conditions, add to results
        filtered_indices.append(i)

    # Score & Rank recipes
    scores = [
        (idx, must_have_similarities[idx] + 0.5 * nice_to_have_similarities[idx])
        for idx in filtered_indices
    ]
    
    # Sort by score (higher is better)
    scores.sort(key=lambda x: x[1], reverse=True)

    # Return top 5 recommended recipes
    top_recipes = scores

    return top_recipes