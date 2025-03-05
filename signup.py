import streamlit as st
import time
from utils import hash_password, save_user, set_background_image, initialize_session

initialize_session()

# Set background image (replace URL if needed)
background_image_url = "https://images.unsplash.com/photo-1591189863430-ab87e120f312?q=80&w=2070&auto=format&fit=crop"
set_background_image(background_image_url)

#st.markdown('<div class="signup-box">', unsafe_allow_html=True)
st.subheader("Sign Up")
username = st.text_input("Username")
password = st.text_input("Password", type="password")
confirm_password = st.text_input("Confirm Password", type="password")

if st.button("Sign Up"):
    with st.spinner("Signing up..."):
        time.sleep(2)  # Simulate delay
        if username and password and confirm_password:
            if password == confirm_password:
                hashed_password = hash_password(password)
                save_user(username, hashed_password)
                st.session_state.username = username
                st.success(f"Welcome {username}, you have successfully signed up! 🎉")
                st.balloons()
                st.rerun()  # Use st.rerun() instead of st.experimental_rerun()
            else:
                st.error("Passwords do not match")
        else:
            st.error("Please fill in all the fields")
st.markdown('</div>', unsafe_allow_html=True)
