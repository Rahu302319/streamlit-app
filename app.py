import requests
import json

API_KEY = "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"

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
