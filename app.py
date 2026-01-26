import streamlit as st
import requests
import time

# ---------------- CONFIGURATION ----------------
# ⚠️ DOUBLE CHECK THESE VALUES
API_KEY = "k_5726942c2615.Ru4o2RnRMhojD1vr497bDFPuTPM5_1Cnjn5xc0qZvytZFBTLNPFzrA"
URL = "https://platform.qubrid.com/api/v1/qubridai/chat/completions"
# If this model name is wrong, the server will reject the request
MODEL = "Qwen/Qwen3-Coder-30B-A3B-Instruct"

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Jarvis Pro",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS (Clean & Professional) ----------------
st.markdown("""
<style>
    /* Import Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Sidebar Dark Mode */
    [data-testid="stSidebar"] {
        background-color: #202123;
    }
    [data-testid="stSidebar"] * {
        color: #ECECF1 !important;
    }

    /* Main Background */
    .stApp {
        background-color: #343541;
    }

    /* Chat Styling */
    div[data-testid="chat-message-user"] {
        background-color: #343541;
        border-bottom: 1px solid #444;
    }
    div[data-testid="chat-message-assistant"] {
        background-color: #444654;
        border-bottom: 1px solid #444;
    }
    
    /* Text Color */
    .stMarkdown p {
        color: #ECECF1 !important;
    }
    
    /* Input Box */
    .stTextInput input {
        color: white;
        background-color: #40414F;
        border: 1px solid #565869;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- REAL API LOGIC ----------------
def get_real_response(prompt, history):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Construct the message history for the API
    messages_payload = [{"role": "system", "content": "You are a helpful assistant."}]
    for msg in history:
        messages_payload.append({"role": msg["role"], "content": msg["content"]})
    
    # Add the new prompt
    messages_payload.append({"role": "user", "content": prompt})

    payload = {
        "model": MODEL,
        "messages": messages_payload,
        "max_tokens": 1000,
        "temperature": 0.7
    }

    try:
        # ⚠️ This is the actual network call
        response = requests.post(URL, headers=headers, json=payload, timeout=15)
        
        # Check for success
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            # RETURN THE ACTUAL ERROR if it fails
            return f"❌ Server Error {response.status_code}: {response.text}"
            
    except Exception as e:
        return f"❌ Connection Failed: {str(e)}"

# ---------------- APP LAYOUT ----------------

if not st.session_state.authenticated:
    # === LOGIN SCREEN ===
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background: white; padding: 30px; border-radius: 10px; text-align: center;">
            <h2 style="color: black; margin:0;">🔐 Login</h2>
        </div>
        """, unsafe_allow_html=True)
        
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        
        if st.button("Sign In", use_container_width=True):
            if email and password:
                st.session_state.authenticated = True
                st.rerun()

else:
    # === CHAT INTERFACE ===
    with st.sidebar:
        st.markdown("### ⚡ Controls")
        if st.button("New Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        if st.button("Log Out", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

    # Display History
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar="👤" if msg["role"] == "user" else "🤖"):
            st.markdown(msg["content"])

    # Handle Input
    if prompt := st.chat_input("Type a message..."):
        # 1. Show User Message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

        # 2. Get Real AI Response
        with st.chat_message("assistant", avatar="🤖"):
            response_placeholder = st.empty()
            
            with st.spinner("Connecting to Server..."):
                full_response = get_real_response(prompt, st.session_state.messages[:-1])
            
            response_placeholder.markdown(full_response)
            
        # 3. Save History
        st.session_state.messages.append({"role": "assistant", "content": full_response})
