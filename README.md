# NutriRecipe Finder

NutriRecipe Finder is a Streamlit-powered app that helps users find Indian dishes depending on their nutritional choices and available ingredients. The app uses a large dataset and advanced NLP techniques to deliver tailored meal recommendations that include nutritional information.

## Overview

This project uses a Kaggle dataset, [7000+ International Cuisine](https://www.kaggle.com/datasets/rumitpathare/indian-recipes), to provide a comprehensive collection of recipes. The core features include:

- **Data Cleaning & Analysis:** Uses Pandas to clean and analyze the dataset.
- **Nutritional Information:** Integrates with Spoonacular's Analyze Recipe endpoint to enrich recipes with nutritional details.
- **Ingredient Filtering:** Implements a filtering mechanism where users can specify:
  - **Must-Have Ingredients**
  - **Acceptable (Nice-to-Have) Ingredients**
  - **Excluded Ingredients**
  
  Recipes are then ranked based on a matching score derived from the provided ingredients.
  
- **User Profile & Dietary Preferences:** A Streamlit application enables users to create profiles, specifying diet types (Veg, Egg, Non-Veg), which refines search results.
- **Embeddings for Enhanced Matching:** Uses the Sentence Transformer library with the pretrained model [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) to generate embeddings for the translated and cleaned ingredient list of each recipe, as well as for user-supplied ingredients.
- **Additional Filtering Options:** Users can also filter recipes by cuisine, dish type, and sort them by preparation time (both ascending and descending).

## Features

- **Dataset Analysis:** Cleans and processes over 5000 recipes for improved usability.
- **Nutritional Insights:** Fetches and integrates nutrition data using Spoonacular.
- **Custom Recipe Filtering:** Allows filtering based on available, desired, and excluded ingredients.
- **Personalized Experience:** Supports diet-specific searches through a user profile.
- **Advanced Embedding Matching:** Utilizes NLP embeddings to score recipe matches accurately.
- **Flexible Sorting & Filtering:** Offers sorting by preparation time and additional filters such as cuisine and dish type.

## Installation

 - ### Prerequisites

   - Python 3.8 or higher
   - [Streamlit](https://streamlit.io/)
   - [Pandas](https://pandas.pydata.org/)
   - [SentenceTransformers](https://www.sbert.net/)
   - Other dependencies (e.g., requests) as specified in the `requirements.txt`

 - ### Setup Instructions

   1. **Clone the Repository:**

      ```bash
      git clone https://github.com/NikhilSinghal1704/NutriRecipe-Finder
      cd NutriRecipe-Finder
      ```

   2. **Create a Virtual Environment:**

      ```bash
      python -m venv venv
      ```

   3. **Activate the Virtual Environment:**

      - On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```
      - On Windows:
        ```bash
        venv\Scripts\activate
        ```

   4. **Install the Dependencies:**

      ```bash
      pip install -r requirements.txt
      ```

## Dataset

The project utilizes the [7000+ International Cuisine](https://www.kaggle.com/datasets/rumitpathare/indian-recipes) dataset available on Kaggle. Make sure to review the dataset’s license and terms of use if you plan to distribute or modify the data.

## Usage

To launch the application, simply run:

```bash
streamlit run main.py
```

Once running, follow these steps within the application:
- Create or update your profile with dietary preferences (Veg, Egg, Non-Veg).
- Specify your available ingredients and any ingredients to exclude.
- Optionally apply additional filters (cuisine, dish type, preparation time).
- View the filtered recipes ranked by their matching score.
