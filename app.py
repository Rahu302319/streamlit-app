import streamlit as st
import requests
import json

# ---------------- CONFIG ----------------
API_KEY = "k_5726942c2615.Ru4o2RnRMhojD1vr497bDFPuTPM5_1Cnjn5xc0qZvytZFBTLNPFzrA"
URL = "https://platform.qubrid.com/api/v1/qubridai/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

MODEL = "Qwen/Qwen3-Coder-30B-A3B-Instruct"

# ---------------- PAGE SETUP ----------------
st.set_page_config(
    page_title="J.A.R.V.I.S AI Assistant",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 J.A.R.V.I.S")
st.caption("Just A Rather Very Intelligent System")

# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are J.A.R.V.I.S, a helpful and intelligent AI assistant."}
    ]

# ---------------- DISPLAY HISTORY ----------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["content"])
    elif msg["role"] == "assistant":
        with st.chat_message("assistant"):
            st.markdown(msg["content"])

# ---------------- INPUT ----------------
user_input = st.chat_input("Talk to J.A.R.V.I.S...")

if user_input:
    # User message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    data = {
        "model": MODEL,
        "messages": st.session_state.messages,
        "temperature": 0.7,
        "max_tokens": 2000,
        "stream": True,
        "top_p": 1
    }

    # Assistant streaming
    with st.chat_message("assistant"):
        response_box = st.empty()
        assistant_reply = ""

        response = requests.post(URL, headers=headers, json=data, stream=True)

        for line in response.iter_lines(decode_unicode=True):
            if not line:
                continue

            if line.startswith("data:"):
                payload = line.replace("data:", "").strip()

                if payload == "[DONE]":
                    break

                try:
                    chunk = json.loads(payload)
                    delta = chunk["choices"][0]["delta"]

                    if "content" in delta:
                        assistant_reply += delta["content"]
                        response_box.markdown(assistant_reply + "▌")

                except:
                    pass

        response_box.markdown(assistant_reply)

    st.session_state.messages.append(
        {"role": "assistant", "content": assistant_reply}
    )


