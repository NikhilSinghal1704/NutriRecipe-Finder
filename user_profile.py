import streamlit as st
from utils import save_profile, get_profile  # Assumes save_profile(username, profile_data) is defined in utils.py

# Ensure the user is logged in.
if "username" not in st.session_state or not st.session_state.username:
    st.error("You must be logged in to update your profile.")
    st.stop()

st.title("Update User Profile")

# Retrieve or initialize the profile dictionary.
profile = get_profile(st.session_state.username)
if profile:
    st.session_state.profile = profile
else:
    profile = {}

# Pre-fill the form fields with existing profile data.
first_name = st.text_input("First Name:", value=profile.get("first_name", ""))
last_name = st.text_input("Last Name:", value=profile.get("last_name", ""))
gender_options = ["Male", "Female", "Other"]
gender_default = profile.get("gender", "Male")
if gender_default not in gender_options:
    gender_default = "Male"
gender = st.selectbox("Gender:", gender_options, index=gender_options.index(gender_default))
age = st.number_input("Age:", min_value=1, max_value=100, step=1, value=profile.get("age", 1))
diet_options = ["Veg", "Egg", "Non-Veg"]
diet_default = profile.get("diet", "Veg")
if diet_default not in diet_options:
    diet_default = "Veg"
diet = st.selectbox("Diet:", diet_options, index=diet_options.index(diet_default))

if st.button("Save"):
    new_profile = {
        "username": st.session_state.username,
        "first_name": first_name,
        "last_name": last_name,
        "gender": gender,
        "age": age,
        "diet": diet
    }
    # Update session state.
    st.session_state.profile = new_profile
    # Save the profile to a JSON file.
    save_profile(st.session_state.username, new_profile)
    st.success("Profile updated successfully!")
    st.rerun()
