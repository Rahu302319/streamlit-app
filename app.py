import streamlit as st
import requests
import uuid
import time
import random

# ---------------- CONFIGURATION ----------------
# 🔒 NOTE: For a real app, use st.secrets. For now, this is fine for testing.
API_KEY = "k_5726942c2615.Ru4o2RnRMhojD1vr497bDFPuTPM5_1Cnjn5xc0qZvytZFBTLNPFzrA"
URL = "https://platform.qubrid.com/api/v1/qubridai/chat/completions"
MODEL = "Qwen/Qwen3-Coder-30B-A3B-Instruct"

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="JARVIS",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS (The "Cute" Style) ----------------
st.markdown("""
<style>
    /* General App Background */
    .stApp {
        background-color: #ffffff;
    }
    
    /* Sidebar Styling (Dark Mode like ChatGPT) */
    [data-testid="stSidebar"] {
        background-color: #202123;
        color: white;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3, [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] p {
        color: #ececf1 !important;
    }
    
    /* Input Fields in Sidebar */
    [data-testid="stSidebar"] .stTextInput input {
        color: #333;
        background-color: #ffffff;
    }

    /* Buttons */
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        border: 1px solid #4d4d4f;
        background-color: #343541;
        color: white;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        background-color: #40414F;
        border-color: #565869;
    }

    /* Chat Area */
    .main-header {
        text-align: center;
        padding: 1rem;
        color: #333;
        margin-bottom: 2rem;
    }
    
    /* Chat Bubbles */
    .stChatMessage {
        background-color: white;
        border: 1px solid #e5e5e5;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        margin-bottom: 10px;
    }
    .stChatMessage[data-testid="chat-message-user"] {
        background-color: #f7f7f8;
    }
    
    /* Hide Default Header */
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = None
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are JARVIS, a helpful AI."}]
if "chat_history" not in st.session_state:
    st.session_state.chat_history = ["Previous Chat 1", "Project Ideas", "Recipes"]

# ---------------- HELPER FUNCTIONS ----------------
def get_ai_response(messages):
    """Fetches response from Qubrid API or falls back to mock data."""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "messages": messages,
        "max_tokens": 500,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(URL, headers=headers, json=payload, timeout=8)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"⚠️ API Error ({response.status_code}): {response.text}"
    except Exception:
        # Fallback for Demo Purposes
        time.sleep(1)
        return random.choice([
            "I'm listening! Tell me more about that. 🌸",
            "That's super interesting! I'm operating in demo mode right now, but I love chatting.",
            "I'm experiencing some network hiccups, but I'm still here with you! 🤖",
            "Could you explain that in a different way? I want to make sure I understand."
        ])

# ---------------- SIDEBAR LOGIC ----------------
with st.sidebar:
    st.markdown("## 🤖 J.A.R.V.I.S")
    
    if not st.session_state.authenticated:
        # --- LOGIN / SIGNUP VIEW ---
        st.markdown("---")
        st.write("Please identify yourself:")
        
        auth_mode = st.radio("Mode", ["Log In", "Sign Up"], horizontal=True, label_visibility="collapsed")
        
        email = st.text_input("Email Address", placeholder="name@example.com")
        password = st.text_input("Password", type="password", placeholder="••••••••")
        
        if st.button("✨ Continue", type="primary"):
            if email and password:
                with st.spinner("Authenticating..."):
                    time.sleep(0.8)  # Simulate network delay
                    st.session_state.authenticated = True
                    st.session_state.username = email.split('@')[0].capitalize()
                    st.rerun()
            else:
                st.warning("Please fill in both fields.")
        
        st.info("ℹ️ Tip: You can use any fake email to test the demo!")
        
    else:
        # --- LOGGED IN VIEW ---
        if st.button("➕ New Chat"):
            st.session_state.messages = [{"role": "system", "content": "You are JARVIS."}]
            st.rerun()
            
        st.markdown("### 🕒 Recent Chats")
        for chat in st.session_state.chat_history:
            st.button(f"💬 {chat}", key=chat)
            
        st.markdown("---")
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown("👤")
        with col2:
            st.markdown(f"**{st.session_state.username}**")
            
        if st.button("Log Out"):
            st.session_state.authenticated = False
            st.session_state.messages = []
            st.rerun()

# ---------------- MAIN APPLICATION ----------------
if not st.session_state.authenticated:
    # --- LANDING PAGE (Logged Out) ---
    st.markdown("""
    <div style='text-align: center; margin-top: 100px;'>
        <h1>👋 Welcome to JARVIS</h1>
        <p style='color: #666; font-size: 1.2rem; margin-bottom: 30px;'>
            Your intelligent, friendly, and helpful AI companion.
        </p>
        <div style='background: #f7f7f8; padding: 30px; border-radius: 15px; display: inline-block; border: 1px solid #e5e5e5;'>
            <h3>👈 Get Started</h3>
            <p>Please <b>Sign Up</b> or <b>Log In</b> using the sidebar on the left.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
else:
    # --- CHAT INTERFACE (Logged In) ---
    
    # 1. Header
    st.markdown(f"""
    <div class="main-header">
        <h1>🤖 JARVIS</h1>
        <p style='color: #888;'>Hello, <b>{st.session_state.username}</b>! How can I help you today?</p>
    </div>
    """, unsafe_allow_html=True)

    # 2. Chat History
    # We use a container so the input bar stays fixed at bottom if needed
    chat_container = st.container()

    with chat_container:
        for msg in st.session_state.messages:
            if msg["role"] != "system":
                with st.chat_message(msg["role"], avatar="👤" if msg["role"] == "user" else "🤖"):
                    st.write(msg["content"])

    # 3. Chat Input
    if prompt := st.chat_input("Send a message..."):
        # Display User Message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.write(prompt)

        # Display Assistant Response
        with st.chat_message("assistant", avatar="🤖"):
            response_placeholder = st.empty()
            full_response = ""
            
            with st.spinner("Thinking..."):
                full_response = get_ai_response(st.session_state.messages)
            
            # Simulate typing effect
            for chunk in full_response.split(" "):
                full_response += chunk + " "
                # In a real app we'd build the string progressively, 
                # but for this demo, just printing the final result looks cleaner
                
            response_placeholder.write(full_response)
            
        st.session_state.messages.append({"role": "assistant", "content": full_response})
