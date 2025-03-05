import streamlit as st
import time
from utils import logout, set_background_image, initialize_session

# Initialize session state for login tracking.
initialize_session()

# Optionally set a background image for the logout page.
background_image_url = "https://images.unsplash.com/photo-1591189863430-ab87e120f312?q=80&w=2070&auto=format&fit=crop"
set_background_image(background_image_url)

st.title("Logout")
st.write("Click the button below to log out.")

if st.button("Logout"):
    with st.spinner("Logging out..."):
        time.sleep(1)  # Simulate a delay (if needed)
        logout()
