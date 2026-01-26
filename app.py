# Streamlit DeepSeek Chatbot (ChatGPT-style Web App)
# Requirements: pip install streamlit requests

import streamlit as st
import requests

# ================= CONFIG =================
API_KEY = "sk-33854520720e4a5f92b2bcbf6e112d32"   # 🔐 Put your OpenRouter API key here
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "deepseek/deepseek-chat"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://yourwebsite.com",
    "X-Title": "Jarvis"
}
# =========================================

st.set_page_config(page_title="Jarvis AI", page_icon="🤖", layout="centered")

st.title("🤖 Jarvis AI")
st.caption("Powered by DeepSeek via OpenRouter")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are Jarvis, a helpful AI assistant."}
    ]

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    elif msg["role"] == "assistant":
        st.chat_message("assistant").write(msg["content"])

# User input box
user_input = st.chat_input("Type your message...")

if user_input:
    # Show user message
    st.chat_message("user").write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    payload = {
        "model": MODEL,
        "messages": st.session_state.messages
    }

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=60)

                if response.status_code != 200:
                    st.error("API Error: " + response.text)
                else:
                    data = response.json()
                    reply = data["choices"][0]["message"]["content"]
                    st.write(reply)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": reply
                    })

            except Exception as e:
                st.error(f"Error: {str(e)}")

# Sidebar
with st.sidebar:
    st.header("⚙ Settings")

    if st.button("🧹 Clear Chat"):
        st.session_state.messages = [
            {"role": "system", "content": "You are Jarvis, a helpful AI assistant."}
        ]
        st.rerun()

    st.markdown("---")
    st.markdown("**Model:** DeepSeek Chat")
    st.markdown("**Platform:** OpenRouter")

