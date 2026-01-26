import streamlit as st
import requests
import json
import time

# ---------------- CONFIGURATION ----------------
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

# ---------------- API LOGIC (FIXED FOR SSE/STREAMING) ----------------
def get_ai_response(prompt, history):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Prepare messages
    messages = [{"role": "system", "content": "You are a helpful AI assistant."}]
    for msg in history:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": MODEL,
        "messages": messages,
        "max_tokens": 1000,
        "temperature": 0.7,
        "stream": False  # Important: Force non-streaming response
    }

    try:
        response = requests.post(URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            try:
                data = response.json()
                # Check for different response structures
                if 'choices' in data and len(data['choices']) > 0:
                    choice = data['choices'][0]
                    if 'message' in choice:
                        return choice['message']['content']
                    elif 'text' in choice:
                        return choice['text']
                    elif 'delta' in choice and 'content' in choice['delta']:
                        return choice['delta']['content']
                
                # If structure is different, return the whole response for debugging
                return f"⚠️ Unexpected response structure: {json.dumps(data, indent=2)}"
                
            except json.JSONDecodeError:
                # Check if it's SSE format and extract content
                content = ""
                for line in response.text.strip().split('\n'):
                    if line.startswith('data: '):
                        if line == 'data: [DONE]':
                            continue
                        try:
                            chunk_data = json.loads(line[6:])  # Remove 'data: ' prefix
                            if 'choices' in chunk_data and len(chunk_data['choices']) > 0:
                                choice = chunk_data['choices'][0]
                                if 'delta' in choice and 'content' in choice['delta']:
                                    content += choice['delta']['content']
                        except:
                            pass
                return content if content else f"⚠️ Raw SSE response: {response.text[:500]}"
                
        else:
            return f"❌ Server Error ({response.status_code}): {response.text[:500]}"

    except requests.exceptions.Timeout:
        return "❌ Request timeout. Please try again."
    except Exception as e:
        return f"❌ Connection Error: {str(e)}"

# ---------------- APP LAYOUT ----------------

if not st.session_state.authenticated:
    # === LOGIN SCREEN ===
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
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
        
        # Debug mode toggle
        st.markdown("---")
        debug_mode = st.checkbox("Debug Mode", help="Show API response details")
        
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
            
            # Display response
            response_placeholder.markdown(full_response)
            
            # Debug info
            if 'debug_mode' in st.session_state and st.session_state.debug_mode:
                with st.expander("Debug Info"):
                    st.code(full_response, language="text")
        
        # 3. Save History
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# ---------------- FOOTER ----------------
st.sidebar.markdown("---")
st.sidebar.caption("Made with ❤️ using Streamlit")
