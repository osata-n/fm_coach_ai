from ollama import Client

client = Client(host="http://localhost:11434")

response = client.chat(
    model="gemma3:latest",
    messages=[
        {
            "role": "user",
            "content": "Привет! Скажи, что ты умеешь делать, и проверь, работает ли наша связь."
        }
    ]
)

print(response["message"]["content"])