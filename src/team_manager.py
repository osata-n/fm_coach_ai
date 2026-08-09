import json
import os
from typing import List, Dict, Optional
from player import Player

class TeamManager:
    """Управляет составом команды: загрузка, обновление, поиск."""
    
    def __init__(self, data_file: str = None):
        """
        data_file — путь к JSON-файлу с данными команды.
        Если не указан, используются тестовые данные.
        """
        self.players: List[Player] = []
        self.data_file = data_file
        
        if data_file and os.path.exists(data_file):
            self.load_from_file(data_file)
        else:
            self._load_sample_data()
    
    def _load_sample_data(self):
        """Загружает тестовые данные (для отладки)."""
        sample_players = [
            {
                "basic": {"name": "Иван Иванов", "age": 24, "country": "Россия", 
                         "reputation": 65, "playing_time": "Регулярно", 
                         "ability": 145, "potential": 160, 
                         "ability_league_level": "Высший дивизион",
                         "potential_league_level": "Топ-клуб"},
                "attributes": {
                    "technical": {"crossing": 12, "dribbling": 14, "finishing": 15, "passing": 13},
                    "mental": {"composure": 12, "decisions": 14, "determination": 16, "vision": 13, "work_rate": 15},
                    "physical": {"pace": 16, "stamina": 14, "strength": 12}
                },
                "fitness": {"condition": 92},
                "morale": 78,
                "contract": {"wage": 45000},
                "coach_report": {"summary": "Опасный нападающий", "strengths": ["Скорость"], "weaknesses": ["Игра головой"]}
            },
            {
                "basic": {"name": "Петр Петров", "age": 28, "country": "Россия", 
                         "reputation": 70, "playing_time": "Основной", 
                         "ability": 155, "potential": 158,
                         "ability_league_level": "Высший дивизион"},
                "attributes": {
                    "technical": {"tackling": 17, "marking": 16, "passing": 12},
                    "mental": {"decisions": 15, "positioning": 16, "work_rate": 14},
                    "physical": {"pace": 13, "strength": 16, "jumping_reach": 15}
                },
                "fitness": {"condition": 88},
                "morale": 82,
                "contract": {"wage": 52000},
                "coach_report": {"summary": "Надежный защитник", "strengths": ["Отбор"], "weaknesses": ["Скорость"]}
            },
            {
                "basic": {"name": "Сергей Сидоров", "age": 22, "country": "Россия", 
                         "reputation": 55, "playing_time": "Резерв", 
                         "ability": 120, "potential": 145,
                         "ability_league_level": "Средний дивизион"},
                "attributes": {
                    "technical": {"passing": 14, "dribbling": 12, "crossing": 13},
                    "mental": {"vision": 15, "decisions": 13, "work_rate": 16},
                    "physical": {"pace": 14, "stamina": 15}
                },
                "fitness": {"condition": 95},
                "morale": 70,
                "contract": {"wage": 28000},
                "coach_report": {"summary": "Перспективный полузащитник", "strengths": ["Видение"], "weaknesses": ["Физика"]}
            }
        ]
        self.players = [Player(p) for p in sample_players]
    
    def load_from_file(self, filepath: str):
        """Загружает команду из JSON-файла."""
        self.data_file = filepath
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Если в файле массив игроков
        if isinstance(data, list):
            self.players = [Player(p) for p in data]
        elif isinstance(data, dict) and "players" in data:
            self.players = [Player(p) for p in data["players"]]
        else:
            raise ValueError("Неверный формат данных: ожидается массив или объект с ключом 'players'")
    
    def save_to_file(self, filepath: str = None):
        """Сохраняет текущий состав в JSON-файл."""
        if filepath is None:
            filepath = self.data_file
        if filepath is None:
            raise ValueError("Не указан путь для сохранения")
        
        data = [p.data for p in self.players]
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    
    def get_player_by_name(self, name: str) -> Optional[Player]:
        """Находит игрока по имени (первое совпадение)."""
        for p in self.players:
            if p.get_name().lower() == name.lower():
                return p
        return None
    
    def get_players_by_position(self, position: str) -> List[Player]:
        """Возвращает всех игроков на указанной позиции."""
        return [p for p in self.players if p.get_position() == position]
    
    def add_player(self, player_data: Dict):
        """Добавляет нового игрока в команду."""
        self.players.append(Player(player_data))
    
    def remove_player(self, name: str) -> bool:
        """Удаляет игрока по имени. Возвращает True, если удален."""
        for i, p in enumerate(self.players):
            if p.get_name().lower() == name.lower():
                del self.players[i]
                return True
        return False
    
    def update_player(self, name: str, new_data: Dict) -> bool:
        """Обновляет данные игрока по имени."""
        player = self.get_player_by_name(name)
        if player:
            player.update(new_data)
            return True
        return False
    
    def get_all_players_prompt(self, include_hidden: bool = False) -> str:
        """
        Возвращает текстовое представление всей команды для LLM.
        include_hidden — включать ли скрытые атрибуты.
        """
        lines = ["=== СОСТАВ КОМАНДЫ ===\n"]
        for p in self.players:
            lines.append(p.to_prompt_text(include_hidden))
            lines.append("---")
        return "\n".join(lines)
    
    def get_team_summary(self) -> str:
        """Возвращает краткое резюме команды для быстрой оценки."""
        total = len(self.players)
        avg_age = sum(p.get_age() for p in self.players) / total if total > 0 else 0
        avg_ability = sum(p.get_ability() for p in self.players) / total if total > 0 else 0
        avg_potential = sum(p.get_potential() for p in self.players) / total if total > 0 else 0
        avg_condition = sum(p.get_physical_condition() for p in self.players) / total if total > 0 else 0
        avg_morale = sum(p.get_morale() for p in self.players) / total if total > 0 else 0
        
        return f"""=== Краткий обзор команды ===
Всего игроков: {total}
Средний возраст: {avg_age:.1f}
Средняя CA: {avg_ability:.0f}
Средний PA: {avg_potential:.0f}
Среднее физическое состояние: {avg_condition:.0f}%
Средняя мораль: {avg_morale:.0f}%"""

if __name__ == "__main__":
    tm = TeamManager()
    print(tm.get_team_summary())
    print("\n" + "="*50)
    print("ПОЛНЫЙ ТЕКСТ ДЛЯ МОДЕЛИ:")
    print("="*50)
    print(tm.get_all_players_prompt(include_hidden=False))