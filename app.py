import streamlit as st
import requests
import time

# ---------------- CONFIGURATION ----------------
# ⚠️ Ensure this API Key is 100% correct and has credits/access
API_KEY = "k_5726942c2615.Ru4o2RnRMhojD1vr497bDFPuTPM5_1Cnjn5xc0qZvytZFBTLNPFzrA"
URL = "https://platform.qubrid.com/api/v1/qubridai/chat/completions"
MODEL = "Qwen/Qwen3-Coder-30B-A3B-Instruct"

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Jarvis Pro",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS (ChatGPT Style) ----------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Dark Sidebar */
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

    /* Input Field */
    .stTextInput input {
        color: white;
        background-color: #40414F;
        border: 1px solid #565869;
        border-radius: 8px;
    }
    
    /* Login Card */
    .login-box {
        background-color: white;
        padding: 40px;
        border-radius: 12px;
        text-align: center;
        width: 100%;
        max-width: 400px;
        margin: auto;
    }
    .login-box h2 { color: #333 !important; }
    .login-box p { color: #666 !important; }
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- API LOGIC (DEBUG MODE) ----------------
def get_ai_response(prompt, history):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # OpenAI-compatible payload structure
    messages = [{"role": "system", "content": "You are a helpful AI assistant."}]
    for msg in history:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": MODEL,
        "messages": messages,
        "max_tokens": 1000,
        "temperature": 0.7
    }

    try:
        response = requests.post(URL, headers=headers, json=payload, timeout=20)
        
        # 1. Check if the request was successful
        if response.status_code == 200:
            try:
                # Try to parse JSON
                return response.json()['choices'][0]['message']['content']
            except Exception:
                # If JSON fails, show raw text (This fixes your error!)
                return f"⚠️ API Error: Valid 200 OK, but response was not JSON.\nRaw output: {response.text}"
        else:
            # 2. Return the actual error message from server
            return f"❌ Server Error ({response.status_code}): {response.text}"

    except Exception as e:
        return f"❌ Connection Error: {str(e)}"

# ---------------- APP LAYOUT ----------------

if not st.session_state.authenticated:
    # === LOGIN SCREEN ===
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        # HTML Login Card
        st.markdown("""
        <div class="login-box">
            <h2>👋 Welcome Back</h2>
            <p>Please log in to continue</p>
        </div>
        """, unsafe_allow_html=True)
        
        email = st.text_input("Email Address", placeholder="user@example.com")
        password = st.text_input("Password", type="password", placeholder="••••••")
        
        if st.button("Continue", use_container_width=True):
            if email and password:
                with st.spinner("Verifying..."):
                    time.sleep(1)
                    st.session_state.authenticated = True
                    st.rerun()
            else:
                st.warning("Please fill in all fields.")

else:
    # === CHAT INTERFACE ===
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🤖 Jarvis Pro")
        if st.button("➕ New Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
        st.markdown("---")
        st.caption("Using Model:")
        st.code(MODEL, language="text")
        
        if st.button("🚪 Log Out", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

    # Chat Area
    # Display History
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar="👤" if msg["role"] == "user" else "🤖"):
            st.markdown(msg["content"])

    # Chat Input
    if prompt := st.chat_input("Send a message..."):
        # 1. User Message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

        # 2. AI Response
        with st.chat_message("assistant", avatar="🤖"):
            response_placeholder = st.empty()
            
            with st.spinner("Generating..."):
                full_response = get_ai_response(prompt, st.session_state.messages[:-1])
            
            response_placeholder.markdown(full_response)
        
        # 3. Save History
        st.session_state.messages.append({"role": "assistant", "content": full_response})
