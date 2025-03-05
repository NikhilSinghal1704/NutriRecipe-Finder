import requests
import streamlit as st
import bcrypt
import json
import time
from datetime import datetime, timedelta
from streamlit_cookies_manager import CookieManager

# Initialize the cookie manager (make sure cookies are ready)
cookies = CookieManager()
if not cookies.ready():
    st.stop()  # Ensure cookies are ready before proceeding

# Function to inject CSS for background image and styling
def set_background_image(image_url):
    st.markdown(
        f"""
        <style> 
        .stApp {{
            background-image: url("{image_url}");
            background-size: cover;
            background-position: center;
            height: 100vh;
        }}
        /* Animations */
        @keyframes fadeIn {{
            0% {{ opacity: 0; }}
            100% {{ opacity: 1; }}
        }}
        @keyframes slideIn {{
            0% {{ transform: translateY(50px); opacity: 0; }}
            100% {{ transform: translateY(0); opacity: 1; }}
        }}
        @keyframes zoomIn {{
            0% {{ transform: scale(0.9); opacity: 0; }}
            100% {{ transform: scale(1); opacity: 1; }}
        }}
        /* Styling the login and signup boxes */
        .login-box, .signup-box {{
            border: 2px solid #4CAF50;
            border-radius: 10px;
            padding: 30px;
            margin: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            background-color: rgba(255, 255, 255, 0.8);
            animation: fadeIn 1s ease-in-out;
        }}
        .login-box h3, .signup-box h3 {{
            text-align: center;
            color: #4CAF50;
        }}
        .login-box {{
            animation: slideIn 1s ease-out;
        }}
        .signup-box {{
            animation: zoomIn 1s ease-out;
        }}
        /* Set the title color to black */
        h1 {{
            color: black;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Function to hash a password using bcrypt
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Function to check a password against its stored hash
def check_password(stored_hash, password):
    return bcrypt.checkpw(password.encode('utf-8'), stored_hash)

# Function to load users from a JSON file
def load_users():
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
        return users
    except FileNotFoundError:
        return {}

# Function to save a new user to the JSON file
def save_user(username, password_hash):
    users = load_users()
    users[username] = password_hash.decode("utf-8")
    with open("users.json", "w") as f:
        json.dump(users, f)

# Function to manage login
def login(username, password):
    users = load_users()
    if username in users and check_password(bytes(users[username], "utf-8"), password):
        st.session_state.username = username
        cookies["username"] = username  # Store username in cookie
        cookies.save()  # Save cookie
        st.success(f"Logged in as {username}")
        st.session_state.logged_in = True
        st.session_state.last_activity_time = datetime.now()
        st.rerun()  # Use st.rerun() here instead of st.experimental_rerun()
    else:
        st.error("Invalid username or password!")

def auto_login():
    """
    Check if a username exists in the cookies and update session state accordingly.
    """
    username = cookies.get("username")
    if username:
        st.session_state.username = username
        st.session_state.logged_in = True


def initialize_session():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'last_activity_time' not in st.session_state:
        st.session_state.last_activity_time = datetime.now()
    
    # Check session expiration (e.g., 30 minutes)
    if st.session_state.logged_in:
        elapsed = datetime.now() - st.session_state.last_activity_time
        if elapsed > timedelta(minutes=30):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.warning("Session expired due to inactivity. Please log in again.")

def logout():
    # Ensure cookies are ready
    if not cookies.ready():
        st.stop()
    # Clear cookie and update session state
    cookies["username"] = ""
    cookies.save()
    st.session_state.username = None
    st.session_state.logged_in = False
    st.success("Logged out successfully!")
    st.rerun()


def get_unsplash_photo_url(query, page=1, per_page=1, order_by="relevant", access_key="opo7qcROYPcFNaJ7oSVGSFD4Fs1YCoBEKSERwt9WolY", **kwargs):
    """
    Retrieve the URL for a photo from Unsplash for a given search query.
    
    Parameters:
        query (str): Search term.
        page (int): Page number to retrieve (default: 1).
        per_page (int): Number of items per page (default: 1).
        order_by (str): How to sort the photos ("latest" or "relevant", default: "relevant").
        access_key (str): Your Unsplash API access key.
        **kwargs: Additional optional parameters (e.g., collections, content_filter, color, orientation).
    
    Returns:
        str or None: URL of the first photo (using the "regular" size) from the search results, or None if not found.
    """
    endpoint = "https://api.unsplash.com/search/photos"
    params = {
        "query": query,
        "page": page,
        "per_page": per_page,
        "order_by": order_by,
        "collections": "146349, 333903, 10577541, 5Tac4lV554s, IIhSWTa-LaU",
        "orientation" : "squarish",
        **kwargs,
    }
    headers = {
        "Authorization": f"Client-ID {access_key}"
    }
    
    response = requests.get(endpoint, params=params, headers=headers)
    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        return None
    
    data = response.json()
    results = data.get("results", [])
    if results:
        # Return the URL of the first photo using the "regular" size.
        return results[0]["urls"].get("regular")
    return None

def load_profiles():
    try:
        with open("profiles.json", "r") as f:
            profiles = json.load(f)
        return profiles
    except FileNotFoundError:
        return {}

def save_profile(username, profile_data):
    profiles = load_profiles()
    profiles[username] = profile_data
    with open("profiles.json", "w") as f:
        json.dump(profiles, f)

def get_profile(username):
    try:
        with open("profiles.json", "r") as f:
            profiles = json.load(f)
        return profiles.get(username)
    except FileNotFoundError:
        # If the file doesn't exist, no profiles are saved.
        return None

# Example usage:
if __name__ == "__main__":
    # Replace with your actual access key.
    photo_url = get_unsplash_photo_url("Pineapple")
    if photo_url:
        print("Photo URL:", photo_url)
    else:
        print("No photo found.")
