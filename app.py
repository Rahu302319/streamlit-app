import streamlit as st
import requests
import json
import uuid
from datetime import datetime

# ---------------- CONFIG ----------------
# 🔒 SECURITY NOTE: For production, use st.secrets instead of hardcoding!
API_KEY = "k_5726942c2615.Ru4o2RnRMhojD1vr497bDFPuTPM5_1Cnjn5xc0qZvytZFBTLNPFzrA"
URL = "https://platform.qubrid.com/api/v1/qubridai/chat/completions"
MODEL = "Qwen/Qwen3-Coder-30B-A3B-Instruct"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# ---------------- CUSTOM CSS ----------------
st.set_page_config(
    page_title="J.A.R.V.I.S Lite",
    page_icon="🤖",
    layout="centered"  # Changed to centered for a focused "Chat GPT" feel
)

st.markdown("""
<style>
    /* Gradient Background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Header Styling */
    .main-header {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 20px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Chat Bubbles */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* User Bubble */
    .stChatMessage[data-testid="chat-message-user"] {
        background: rgba(102, 126, 234, 0.2);
        border-left: 5px solid #667eea;
    }
    
    /* Assistant Bubble */
    .stChatMessage[data-testid="chat-message-assistant"] {
        background: rgba(44, 62, 80, 0.5);
        border-left: 5px solid #764ba2;
    }
    
    h1 { color: white !important; font-size: 2.2rem !important; }
    p { color: #e0e0e0 !important; }
    
    /* Remove default Streamlit header decoration */
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div class="main-header">
    <h1>🤖 J.A.R.V.I.S Lite</h1>
    <p>Your Intelligent AI Companion</p>
</div>
""", unsafe_allow_html=True)

# ---------------- SESSION MANAGEMENT ----------------
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are J.A.R.V.I.S, a helpful, witty, and concise AI assistant. Keep answers friendly and smart."}
    ]

# ---------------- CHAT INTERFACE ----------------

# 1. Display Chat History
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"], avatar="👤" if msg["role"] == "user" else "🤖"):
            st.markdown(msg["content"])

# 2. Handle User Input
if user_input := st.chat_input("How can I help you today?"):
    
    # Add User Message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    # Generate AI Response
    with st.chat_message("assistant", avatar="🤖"):
        response_placeholder = st.empty()
        full_response = ""
        
        try:
            # Prepare payload
            payload = {
                "model": MODEL,
                "messages": st.session_state.messages, # Send full history for context
                "max_tokens": 1024,
                "temperature": 0.7
            }
            
            with st.spinner("Processing..."):
                response = requests.post(URL, headers=headers, json=payload, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    if "choices" in data and len(data["choices"]) > 0:
                        full_response = data["choices"][0]["message"]["content"]
                    else:
                        full_response = "I received an empty response from the server."
                else:
                    full_response = f"⚠️ API Error ({response.status_code}): {response.text}"
            
            # Display Response
            response_placeholder.markdown(full_response)
            
            # Add to History
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Connection Error: {str(e)}")

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption(f"⚡ Powered by Qubrid AI | Session: {st.session_state.session_id[:8]}")
