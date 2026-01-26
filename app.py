import requests
import json

API_KEY = "sk-33854520720e4a5f92b2bcbf6e112d32"

response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://yourwebsite.com",   # optional
        "X-Title": "Jarvis"                           # <-- your API/App name
    },
    data=json.dumps({
        "model": "openai/gpt-5.2",
        "messages": [
            {
                "role": "user",
                "content": "What is the meaning of life?"
            }
        ]
    })
)

print(response.status_code)
print(response.json())

