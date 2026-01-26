# PyQt6 DeepSeek Chatbot (ChatGPT-style UI)
# Requires: pip install PyQt6 requests

import sys
import requests
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel, QScrollArea
)
from PyQt6.QtCore import Qt

# ================= CONFIG =================
API_KEY = "YOUR_NEW_API_KEY_HERE"
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "deepseek/deepseek-chat"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://yourwebsite.com",
    "X-Title": "Jarvis"
}
# =========================================

class ChatBubble(QLabel):
    def __init__(self, text, is_user=False):
        super().__init__(text)
        self.setWordWrap(True)
        self.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        if is_user:
            self.setStyleSheet("""
                background-color: #0b5ed7;
                color: white;
                padding: 10px;
                border-radius: 12px;
                max-width: 400px;
            """)
            self.setAlignment(Qt.AlignmentFlag.AlignRight)
        else:
            self.setStyleSheet("""
                background-color: #2b2b2b;
                color: white;
                padding: 10px;
                border-radius: 12px;
                max-width: 400px;
            """)
            self.setAlignment(Qt.AlignmentFlag.AlignLeft)


class ChatWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jarvis - DeepSeek AI")
        self.resize(700, 800)

        self.messages = [
            {"role": "system", "content": "You are Jarvis, a helpful assistant."}
        ]

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        title = QLabel("🤖 Jarvis AI (DeepSeek)")
        title.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        main_layout.addWidget(title)

        # Scroll Area for chat
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.addStretch()

        self.scroll.setWidget(self.chat_container)
        main_layout.addWidget(self.scroll)

        # Input area
        input_layout = QHBoxLayout()

        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Type your message...")
        self.input_box.returnPressed.connect(self.send_message)

        self.send_btn = QPushButton("Send")
        self.send_btn.clicked.connect(self.send_message)

        input_layout.addWidget(self.input_box)
        input_layout.addWidget(self.send_btn)

        main_layout.addLayout(input_layout)

        self.setStyleSheet("""
            QWidget { background-color: #121212; color: white; }
            QLineEdit { padding: 8px; border-radius: 8px; background: #1e1e1e; }
            QPushButton { padding: 8px 15px; border-radius: 8px; background: #0b5ed7; color: white; }
            QPushButton:hover { background: #0a53be; }
        """)

    def add_message(self, text, is_user=False):
        bubble = ChatBubble(text, is_user)

        wrapper = QWidget()
        layout = QHBoxLayout(wrapper)

        if is_user:
            layout.addStretch()
            layout.addWidget(bubble)
        else:
            layout.addWidget(bubble)
            layout.addStretch()

        self.chat_layout.insertWidget(self.chat_layout.count() - 1, wrapper)

        QApplication.processEvents()
        self.scroll.verticalScrollBar().setValue(
            self.scroll.verticalScrollBar().maximum()
        )

    def send_message(self):
        text = self.input_box.text().strip()
        if not text:
            return

        self.input_box.clear()
        self.add_message(text, True)

        self.messages.append({"role": "user", "content": text})

        self.get_ai_response()

    def get_ai_response(self):
        payload = {
            "model": MODEL,
            "messages": self.messages
        }

        try:
            r = requests.post(API_URL, headers=HEADERS, json=payload, timeout=60)

            if r.status_code != 200:
                self.add_message("Error: API request failed")
                return

            data = r.json()
            reply = data["choices"][0]["message"]["content"]

            self.messages.append({"role": "assistant", "content": reply})
            self.add_message(reply, False)

        except Exception as e:
            self.add_message(f"Error: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatWindow()
    window.show()
    sys.exit(app.exec())
