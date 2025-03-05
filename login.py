import streamlit as st
import time
from utils import login, set_background_image, initialize_session

initialize_session()

# Set background image (replace URL if needed)
background_image_url = "https://images.unsplash.com/photo-1591189863430-ab87e120f312?q=80&w=2070&auto=format&fit=crop"
set_background_image(background_image_url)

#st.markdown('<div class="login-box"> Hello </div>', unsafe_allow_html=True)
st.subheader("Login")
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    with st.spinner("Logging in..."):
        time.sleep(2)  # Simulate delay
        if username and password:
            login(username, password)
        else:
            st.error("Please enter both username and password")
st.markdown('</div>', unsafe_allow_html=True)
