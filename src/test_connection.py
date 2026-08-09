# test_connection.py
# Этот скрипт проверяет, работает ли связь между Python и Gemma 3.

from ollama import Client

# Создаем клиент для подключения к Ollama
client = Client(host="http://localhost:11434")

# Отправляем простой запрос модели
response = client.chat(
    model="gemma3:latest",
    messages=[
        {
            "role": "user",
            "content": "Привет! Скажи, что ты умеешь делать, и проверь, работает ли наша связь."
        }
    ]
)

# Выводим ответ модели
print(response["message"]["content"])