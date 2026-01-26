import streamlit as st
import requests
import json
from datetime import datetime

# ---------------- CONFIG ----------------
API_KEY = "k_5726942c2615.Ru4o2RnRMhojD1vr497bDFPuTPM5_1Cnjn5xc0qZvytZFBTLNPFzrA"   # <-- put your API key here
URL = "https://platform.qubrid.com/api/v1/qubridai/chat/completions"
MODEL = "Qwen/Qwen3-Coder-30B-A3B-Instruct"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# ---------------- MEMORY SETTINGS ----------------
MAX_MESSAGES = 40
MAX_TOKENS_OUTPUT = 32768
HISTORY_FILE = "chat_history.jsonl"

def trim_messages(messages):
    if len(messages) <= MAX_MESSAGES:
        return messages
    return [messages[0]] + messages[-MAX_MESSAGES:]

def save_message(role, content):
    record = {
        "time": datetime.now().isoformat(),
        "role": role,
        "content": content
    }
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

# ---------------- PAGE SETUP ----------------
st.set_page_config(page_title="J.A.R.V.I.S", page_icon="🧠", layout="centered")
st.title("🧠 J.A.R.V.I.S")
st.caption("Unlimited Memory AI Assistant")

# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are J.A.R.V.I.S, a helpful intelligent AI assistant."}
    ]

# ---------------- SHOW CHAT ----------------
for msg in st.session_state.messages:
    if msg["role"] in ["user", "assistant"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# ---------------- INPUT ----------------
user_input = st.chat_input("Talk to J.A.R.V.I.S...")

if user_input:
    # Save + show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    save_message("user", user_input)

    with st.chat_message("user"):
        st.markdown(user_input)

    # Trim context for AI
    st.session_state.messages = trim_messages(st.session_state.messages)

    # Prepare request
    data = {
        "model": MODEL,
        "messages": st.session_state.messages,
        "temperature": 0.7,
        "max_tokens": MAX_TOKENS_OUTPUT,
        "stream": True,
        "top_p": 1
    }

    # Assistant response
    with st.chat_message("assistant"):
        response_box = st.empty()
        assistant_reply = ""

        try:
            response = requests.post(URL, headers=headers, json=data, stream=True, timeout=300)

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

        except Exception as e:
            assistant_reply = f"⚠️ Error: {str(e)}"

        response_box.markdown(assistant_reply)

    # Save assistant message
    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
    save_message("assistant", assistant_reply)
