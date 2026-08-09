from ollama import Client
import os

def load_system_prompt():
    prompt_path = os.path.join("..", "prompts", "system_prompt.txt")
    try:
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Ты — помощник в Football Manager. Отвечай на русском языке."

def ask_model(user_question, team_data=None):
    client = Client(host="http://localhost:11434")
    system_prompt = load_system_prompt()
    full_prompt = f"{system_prompt}\n\n"
    if team_data:
        full_prompt += f"Данные о команде:\n{team_data}\n\n"
    full_prompt += f"Вопрос: {user_question}"
    response = client.chat(
        model="gemma3:latest",
        messages=[
            {"role": "user", "content": full_prompt}
        ]
    )
    return response["message"]["content"]

def main():
    print("=" * 50)
    print("ФУТБОЛЬНЫЙ АССИСТЕНТ ДЛЯ FM2026")
    print("=" * 50)
    team_data = """
Игроки:
- Иванов (ST): Скорость=15, Удар=12, Хладнокровие=8, Пас=11
- Петров (CB): Скорость=9, Отбор=18, Прыжки=14, Решение=12
- Сидоров (CM): Скорость=14, Пас=16, Выносливость=15, Решение=14
- Смирнов (LW): Скорость=17, Дриблинг=14, Кросс=13, Решение=10
- Козлов (GK): Рефлексы=16, Один-на-один=15, Концентрация=13
"""
    
    question = "Какой состав мне выпустить на матч против команды, которая играет в быстрые контратаки?"
    
    print("\nАнализирую данные...")
    print("-" * 50)
    
    answer = ask_model(question, team_data)
    
    print("\nРЕКОМЕНДАЦИЯ:")
    print("-" * 50)
    print(answer)
    print("-" * 50)

if __name__ == "__main__":
    main()