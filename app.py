import streamlit as st
import requests
import time
import random

# ---------------- CONFIGURATION ----------------
# 🔒 You can stick your API key here or use st.secrets for production
API_KEY = "k_5726942c2615.Ru4o2RnRMhojD1vr497bDFPuTPM5_1Cnjn5xc0qZvytZFBTLNPFzrA"
URL = "https://platform.qubrid.com/api/v1/qubridai/chat/completions"
MODEL = "Qwen/Qwen3-Coder-30B-A3B-Instruct"

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Jarvis AI",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- 🎨 CUSTOM CSS (THE UI MAKEOVER) ----------------
st.markdown("""
<style>
    /* IMPORT FONT (Inter for a clean look) */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* 1. HIDE DEFAULT STREAMLIT JUNK */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* 2. SIDEBAR STYLING (ChatGPT Dark Mode) */
    [data-testid="stSidebar"] {
        background-color: #202123;
        border-right: 1px solid #333;
    }
    [data-testid="stSidebar"] * {
        color: #ECECF1 !important;
    }
    /* Sidebar Inputs */
    [data-testid="stSidebar"] input {
        background-color: #40414F;
        color: white;
        border: 1px solid #565869;
        border-radius: 6px;
    }
    
    /* 3. MAIN CHAT AREA */
    .stApp {
        background-color: #343541; /* Dark Grey Background like ChatGPT */
    }
    
    /* 4. CHAT BUBBLES */
    .stChatMessage {
        background-color: transparent;
        border: none;
    }
    /* User Message Background */
    div[data-testid="chat-message-user"] {
        background-color: #343541; 
        border-bottom: 1px solid #2A2B32;
    }
    /* AI Message Background */
    div[data-testid="chat-message-assistant"] {
        background-color: #444654; /* Slightly lighter grey */
        border-bottom: 1px solid #2A2B32;
    }
    
    /* Text Colors in Chat */
    .stMarkdown p {
        color: #ECECF1 !important;
        font-size: 16px;
        line-height: 1.6;
    }

    /* 5. BUTTON STYLING */
    .stButton > button {
        background-color: #10a37f; /* ChatGPT Green */
        color: white;
        border: none;
        border-radius: 4px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        background-color: #0d8a6a;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    /* Secondary Buttons (Sidebar) */
    [data-testid="stSidebar"] button {
        background-color: #343541;
        border: 1px solid #565869;
    }
    [data-testid="stSidebar"] button:hover {
        background-color: #2A2B32;
    }

    /* 6. LOGIN CARD STYLING */
    .login-container {
        background-color: #ffffff;
        padding: 3rem;
        border-radius: 12px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        text-align: center;
        max-width: 400px;
        margin: 50px auto;
    }
    .login-header {
        color: #333;
        font-weight: 700;
        font-size: 1.8rem;
        margin-bottom: 1rem;
    }
    
    /* Input Field Styling in Main Area */
    .stTextInput input {
        border-radius: 8px;
        padding: 10px;
        border: 1px solid #ddd;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- LOGIC ----------------

def get_response(prompt, history):
    # This keeps the app from crashing if the API key is wrong
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": MODEL, 
        "messages": [{"role": "system", "content": "You are a helpful assistant."}] + history,
        "max_tokens": 1000
    }
    try:
        response = requests.post(URL, headers=headers, json=payload, timeout=5)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
    except:
        pass
    
    # Fallback "Cute" Responses if API fails
    return random.choice([
        "I'm thinking... 🤔",
        "That's a great question! Tell me more.",
        "I'm currently in demo mode, but I love chatting with you! ✨",
        "Could you rephrase that? I want to help!"
    ])

# ---------------- APP LAYOUT ----------------

if not st.session_state.authenticated:
    # === LOGIN PAGE ===
    # We use columns to center the login box perfectly
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background: white; padding: 40px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); text-align: center;">
            <h1 style="color: #333; margin-bottom: 0;">👋 Welcome</h1>
            <p style="color: #666; margin-bottom: 20px;">Please sign in to continue</p>
        </div>
        """, unsafe_allow_html=True)
        
        email = st.text_input("Email", placeholder="user@example.com")
        password = st.text_input("Password", type="password", placeholder="••••••")
        
        if st.button("Sign In", use_container_width=True):
            if email and password:
                with st.spinner("Logging in..."):
                    time.sleep(0.8)
                    st.session_state.authenticated = True
                    st.rerun()
            else:
                st.warning("Please enter any email and password.")

else:
    # === CHAT INTERFACE ===
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🤖 New Chat")
        if st.button("✨ Clear Conversation", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
            
        st.markdown("---")
        st.markdown("### History")
        st.caption("No previous history")
        
        st.markdown("---")
        if st.button("🚪 Log Out", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

    # Main Chat Area
    # If empty, show a welcome message
    if not st.session_state.messages:
        st.markdown("""
        <div style="text-align: center; color: #ECECF1; margin-top: 50px;">
            <h1>Jarvis AI</h1>
            <p>Your intelligent companion. Ask me anything!</p>
        </div>
        """, unsafe_allow_html=True)

    # Display Chat History
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar="👤" if msg["role"] == "user" else "🤖"):
            st.markdown(msg["content"])

    # Chat Input
    if prompt := st.chat_input("Send a message..."):
        # Add User Message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

        # Add AI Response
        with st.chat_message("assistant", avatar="🤖"):
            response_placeholder = st.empty()
            full_response = get_response(prompt, st.session_state.messages)
            
            # Simulate Typing
            display_text = ""
            for char in full_response:
                display_text += char
                if len(display_text) % 5 == 0: # Update every 5 chars for speed
                    response_placeholder.markdown(display_text + "▌")
                    time.sleep(0.005)
            response_placeholder.markdown(display_text)
            
        st.session_state.messages.append({"role": "assistant", "content": full_response})
