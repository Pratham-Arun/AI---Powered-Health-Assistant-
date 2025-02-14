import streamlit as st
import requests
from bs4 import BeautifulSoup
import pytz,os,sys
import datetime


from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# FastAPI backend URLs
API_BASE_URL = os.getenv("API_BASE_URL")
API_AUTH_URL = f"{API_BASE_URL}/auth"
API_CHAT_URL = f"{API_BASE_URL}/healthbot"
API_CHAT_HISTORY_URL = f"{API_BASE_URL}/chat_history"

# Set page config
st.set_page_config(page_title="Health Assistant", page_icon="🩺", layout="wide")

# Disclaimer message
st.markdown(
    """
    **Disclaimer:** Please do not enter any sensitive or personal information into this application.
    The information provided here is for informational purposes only and is not a substitute for professional medical advice.
    """,
    unsafe_allow_html=True
)

# Sidebar - Light/Dark Mode Toggle
with st.sidebar:
    st.title("⚙️ Settings")
    theme = st.radio("Choose Theme", ["🌞 Light Mode", "🌙 Dark Mode"], key="theme")

# Apply Dark Mode if selected
if theme == "🌙 Dark Mode":
    st.markdown(
        """
        <style>
            body, .stApp {
                background-color: #121212 !important;
                color: white !important;
            }
            .stChatMessage, .chat-container, .stTextInput>div>div>input {
                background-color: #1E1E1E !important;
                color: white !important;
                border-radius: 8px;
            }
            .stTextInput>div>div>input {
                border: 1px solid #555 !important;
            }
            .user-message {
                color: #FF4B4B !important;
                font-weight: bold;
                font-size: 18px;
                padding: 10px;
                display: block;
                text-align: left;
            }
            .bot-message {
                color: #4CAF50 !important;
                font-weight: bold;
                font-size: 18px;
                padding: 10px;
                display: block;
                text-align: left;
            }
            .stButton>button {
                background-color: #FF4B4B !important;
                color: white !important;
                border-radius: 8px;
            }
            /* Sidebar Background & Text */
            [data-testid="stSidebar"] {
                background-color: #181818 !important;
                color: white !important;
            }
            [data-testid="stSidebar"] * {
                color: white !important;
            }
            /* Chat history visibility fix */
            .stSelectbox div[data-baseweb="select"] > div {
                color: white !important; /* Ensures chat history dates are visible */
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown("""
        <style>
    /* Override dark background for specific class */
    .st-b7 {
        background-color: #FFFFFF !important; /* Set to white */
    }
    /* Override text color for .st-bs class to ensure visibility */
    .st-bs {
        color: black !important; /* Set to black for visibility */
    }
    /* Override background color for .st-emotion-cache-hzygls */
    .st-emotion-cache-hzygls {
        background-color: #FFFFFF !important; /* Set to white */
    }
    /* Override text color for .st-dy class to red */
    .st-dy {
        color: red !important; /* Set to red */
    }
    /* Override dark background and border colors for other specific classes */
    .st-cp, .st-co, .st-cn, .st-cm, .st-cl {
        background-color: #FFFFFF !important; /* Set to white */
        border-color: #ccc !important; /* Light border color */
    }

    /* General Light Mode Styling for the Application */
    body, .stApp, .block-container, .main, .chat-container, 
    .stChatMessage, .stTextInput>div>div>input, 
    [data-testid="stChatInputContainer"], 
    [data-testid="stTextArea"], [data-testid="stChatInput"] {
        background-color: #FFFFFF !important;
        color: black !important;
        border-radius: 8px;
    }

    /* Fix Chat Input Box in Light Mode */
    [data-testid="stChatInputContainer"] {
        background-color: #FFFFFF !important;
        color: black !important;
        border: 1px solid #ccc !important;
        border-radius: 10px;
    }

    /* Dropdown Styling */
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        color: black !important;
    }

    /* Placeholder Text Styling */
    [data-testid="stChatInputContainer"] textarea::placeholder, 
    [data-testid="stChatInput"] textarea::placeholder {
        color: #555 !important;
        opacity: 1 !important;
        font-weight: bold !important;
    }

    /* Password Input Field */
    input[type="password"] {
        background-color: white !important;
        color: black !important;
        border: 1px solid #ccc !important;
        border-radius: 8px;
    }

    /* Password Visibility Toggle */
    input[type="password"]::-ms-reveal,
    input[type="password"]::-ms-clear,
    input[type="password"]::-webkit-reveal,
    input[type="password"]::-webkit-credentials-auto-fill-button,
    input[type="password"]::-webkit-contacts-auto-fill-button {
        background: transparent !important;
        border: none !important;
        color: #333 !important;
    }

    /* Password Visibility Toggle Button */
    .st-ae.st-ay.st-d1.st-d2.st-cz.st-d0.st-dg.st-br.st-dh.st-bb.st-bs {
        background-color: transparent !important;
        border: none !important;
        cursor: pointer;
        display: flex;
        align-items: center;
        padding: 0;
    }

    /* Ensure Buttons Look Correct */
    .stButton>button {
        background-color: #1E88E5 !important;
        color: white !important;
        border-radius: 8px;
        font-size: 16px;
        padding: 8px 16px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #1565C0 !important;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"], .stSidebar {
        background-color: #F8F9FA !important;
        color: black !important;
    }
    [data-testid="stSidebar"] * {
        color: black !important;
    }

    /* Hide Streamlit Footer and Header for a Clean UI */
    footer, header {
        display: none !important;
    }

    /* Ensure Scrollbars are Subtle */
    ::-webkit-scrollbar {
        background: transparent;
        width: 6px;
    }
    ::-webkit-scrollbar-thumb {
        background: #ccc;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Add custom CSS for blue buttons
st.markdown(
    """
    <style>
    .stButton>button {
        background-color: blue;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Add custom CSS for blue buttons
st.markdown(
    """
    <style>
    .stButton>button {
        background-color: blue;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)
    
# Add custom CSS for blue buttons
st.markdown(
    """
    <style>
    .stButton>button {
        background-color: blue;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize session states
if "auth_token" not in st.session_state:
    st.session_state.auth_token = None
if "username" not in st.session_state:
    st.session_state.username = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = []
if "selected_chat" not in st.session_state:
    st.session_state.selected_chat = None
if "is_guest" not in st.session_state:
    st.session_state.is_guest = True
if "clear_chat_confirm" not in st.session_state:
    st.session_state.clear_chat_confirm = False
if "clear_history_confirm" not in st.session_state:
    st.session_state.clear_history_confirm = False

# Convert UTC timestamp to IST
def convert_utc_to_ist(utc_timestamp):
    if not utc_timestamp:
        return "Unknown Date"

    utc_tz = pytz.utc
    ist_tz = pytz.timezone("Asia/Kolkata")
    
    utc_time = datetime.datetime.strptime(utc_timestamp, "%Y-%m-%d %H:%M:%S").replace(tzinfo=utc_tz)
    ist_time = utc_time.astimezone(ist_tz)
    
    return ist_time.strftime("%Y-%m-%d %I:%M %p")

# Function to send API requests
def api_request(endpoint, method="GET", data=None):
    headers = {"Authorization": f"Bearer {st.session_state.auth_token}"} if st.session_state.auth_token else {}
    url = f"{API_BASE_URL}{endpoint}"

    try:
        if method == "POST":
            response = requests.post(url, json=data, headers=headers)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers)
        else:
            response = requests.get(url, headers=headers)
        
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        st.error(f"⚠️ Unable to connect to the server. Error: {e}")
        return None

# Function to load chat history from API
def load_chat_sessions():
    """Load and display chat sessions in the sidebar."""
    if st.session_state.is_guest:
        return  # Don't load history for guest users

    response = api_request("/chat_history/")
    if response and response.status_code == 200:
        raw_history = response.json().get("history", {})

        if not raw_history:
            st.session_state.chat_sessions = []
            return
        
        chat_sessions = []
        seen_timestamps = set()

        # ✅ Process each chat entry
        for date, chats in raw_history.items():
            for chat in chats:
                chat_id = chat.get("id")
                timestamp = convert_utc_to_ist(chat.get("timestamp", "Unknown Date"))

                # ✅ Prevent duplicate timestamps
                if chat_id and timestamp not in seen_timestamps:
                    chat_sessions.append({"id": chat_id, "timestamp": timestamp})
                    seen_timestamps.add(timestamp)

        st.session_state.chat_sessions = chat_sessions
    else:
        st.session_state.chat_sessions = []

# Function to load selected chat
def load_selected_chat(chat_id):
    """Load chat messages from a specific chat session."""
    response = api_request(f"/chat_history/{chat_id}")

    if response and response.status_code == 200:
        chat_data = response.json()
        st.session_state.messages = [
            {"role": "user", "content": chat_data["query"]},
            {"role": "assistant", "content": chat_data["response"]}
        ]

        # ✅ Display chat messages correctly
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                color = "red" if message["role"] == "user" else "green"
                role_icon = "🧑‍💬" if message["role"] == "user" else "🤖"
                st.markdown(f"<div style='color:{color}; font-weight:bold; font-size:18px;'>{role_icon} <b>{message['role'].capitalize()}:</b> {message['content']}</div>", unsafe_allow_html=True)
    else:
        st.error("⚠️ Failed to load chat messages.")

# Sidebar - User Authentication & Chat History
with st.sidebar:
    st.title("🔑 Login / Signup")

    if st.session_state.auth_token is None:
        auth_mode = st.radio("Choose an option:", ["Login", "Signup", "Guest Access"])

        if auth_mode != "Guest Access":
            username = st.text_input("👤 Username")
            password = st.text_input("🔒 Password", type="password")

        if auth_mode == "Login":
            if st.button("🔓 Login"):
                try:
                    response = requests.post(f"{API_AUTH_URL}/login", json={"username": username, "password": password})
                    # Check if the response is successful
                    if response.status_code == 200:
                        st.session_state.auth_token = response.json()["token"]
                        st.session_state.username = username
                        st.session_state.is_guest = False
                        load_chat_sessions()
                        st.rerun()
                    else:
                        # Handle specific error cases
                        if response.status_code == 422:
                            st.error("❌ Invalid Username or Password")
                        else:
                            st.error("❌ An error occurred during login. Please try again.")
                except requests.exceptions.RequestException:
                    # Handle network errors or other request exceptions
                    st.error("❌ Unable to connect to the server. Please check your connection.")

        elif auth_mode == "Signup":
            if st.button("📝 Signup"):
                try:
                    response = requests.post(f"{API_AUTH_URL}/register", json={"username": username, "password": password})
                    # Check if the signup was successful
                    if response.status_code == 200:
                        st.success("✅ Signup successful! Please log in.")
                    else:
                        # Handle specific error cases
                        if response.status_code == 400:
                            error_detail = response.json().get("detail", "")
                            if "Username already exists" in error_detail:
                                st.error("❌ Signup failed. Username already exists. Please choose a different username.")
                            else:
                                st.error("❌ Signup failed. Please check your details and try again.")
                        else:
                            st.error("❌ An unexpected error occurred during signup. Please try again later.")
                except requests.exceptions.RequestException:
                    # Handle network errors or other request exceptions
                    st.error("❌ Unable to connect to the server. Please check your connection.")

        elif auth_mode == "Guest Access":
            if st.button("👤 Continue as Guest"):
                st.session_state.is_guest = True
                st.session_state.auth_token = "guest"
                st.session_state.username = "Guest"
                st.success("Logged in as guest!")
                st.rerun()

    else:
        st.markdown(f"👤 Logged in as **{st.session_state.username}**")

        # ✅ Ensure chat sessions are loaded
        if not st.session_state.is_guest:
            load_chat_sessions()  

            # ✅ Only show chat history if there are previous chats
            if st.session_state.chat_sessions:
                chat_options = {f"Chat on {chat['timestamp']}": chat["id"] for chat in st.session_state.chat_sessions}

                selected_chat_title = st.selectbox("📜 Chat History by Date", options=list(chat_options.keys()), key="selected_chat_title")

                if st.button("📂 Load Chat"):
                    st.session_state.selected_chat = chat_options.get(selected_chat_title)
                    load_selected_chat(st.session_state.selected_chat)
                    st.rerun()

        # ✅ Logout button
        if st.button("🚪 Logout"):
            st.session_state.auth_token = None
            st.session_state.username = None
            st.session_state.messages = []
            st.session_state.chat_sessions = []
            st.session_state.selected_chat = None
            st.session_state.is_guest = True
            st.rerun()

# Main App - Chat Interface
if st.session_state.auth_token:
    st.markdown("<h1 style='text-align: center;'>🩺 Health Assistant Chatbot</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>💡 Ask me about medical symptoms, treatments, and general health advice!</p>", unsafe_allow_html=True)

    # Display Chat Messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            color = "red" if message["role"] == "user" else "green"
            role_icon = "🧑‍💬" if message["role"] == "user" else "🤖"
            st.markdown(f"<div style='color:{color}; font-weight:bold; font-size:18px;'>{role_icon} <b>{message['role'].capitalize()}:</b> {message['content']}</div>", unsafe_allow_html=True)
    # Chat Input & Processing
    query = st.chat_input("💬 Type your message here...")

    if query:
        query = query.strip()

        st.session_state.messages.append({"role": "user", "content": query})

        with st.chat_message("user"):
            st.markdown(f"<p style='color:red; font-weight:bold; font-size:18px;'>🧑‍💬 <b>You:</b> {query}</p>", unsafe_allow_html=True)

        with st.spinner("🤖 Thinking..."):
            try:
                headers = {"Authorization": f"Bearer guest"} if st.session_state.is_guest else {"Authorization": f"Bearer {st.session_state.auth_token}"}
                response = requests.post(API_CHAT_URL, json={"query": query}, headers=headers)
                response.raise_for_status()
                bot_response = response.json().get("response", "⚠️ Unexpected response format.")

                # Ensure that the entire response is wrapped in green
                formatted_response = bot_response.replace('\n', '<br/>')

            except requests.exceptions.RequestException as e:
                formatted_response = "⚠️ Unable to process your request at the moment. Please try again later."

        st.session_state.messages.append({"role": "assistant", "content": formatted_response})

        with st.chat_message("assistant"):
            # Wrap the entire response in a span with green styling
            st.markdown(f"<span style='color:green; font-weight:bold; font-size:18px;'>🤖 <b>HealthBot:</b> {formatted_response}</span>", unsafe_allow_html=True)

        st.rerun()
    # Clear Chat Button with Confirmation
    st.divider()
    if st.button("🗑️ Clear Chat"):
        st.session_state.clear_chat_confirm = True

    if st.session_state.clear_chat_confirm:
        st.warning("Are you sure you want to clear the chat?")
        if st.button("Yes, clear it"):
            st.session_state.messages.clear()
            st.session_state.selected_chat = None
            st.session_state.clear_chat_confirm = False
            st.success("Chat cleared successfully.")
            st.rerun()
        if st.button("Cancel"):
            st.session_state.clear_chat_confirm = False

    # Delete Chat History Button with Confirmation
    if not st.session_state.is_guest:
        if st.button("🗑️ Delete Chat History"):
            st.session_state.clear_history_confirm = True

        if st.session_state.clear_history_confirm:
            st.warning("Are you sure you want to delete all chat history?")
            if st.button("Yes, delete it"):
                response = api_request("/chat_history/delete/", method="DELETE")
                
                if response and response.status_code == 200:
                    st.session_state.messages.clear()
                    st.session_state.chat_sessions.clear()
                    st.success("✅ Chat history deleted successfully!")
                else:
                    st.error("❌ Failed to delete chat history. Please try again.")
                
                st.session_state.clear_history_confirm = False
                st.rerun()
            if st.button("Cancel"):
                st.session_state.clear_history_confirm = False
else:
    st.markdown("<h2 style='text-align: center;'>🔒 Please log in to access the chatbot.</h2>", unsafe_allow_html=True)
