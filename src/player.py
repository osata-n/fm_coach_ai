import json
import os
from typing import Dict, List, Optional, Any

class Player:
    """Представляет игрока в Football Manager с полным набором данных."""
    
    def __init__(self, data: Dict[str, Any]):
        """
        Инициализирует игрока из словаря данных.
        data — должен соответствовать схеме player_schema.json.
        """
        self.data = data
        self._normalize()
    
    def _normalize(self):
        """Приводит данные к стандартному виду, если чего-то не хватает."""
        self.data.setdefault("basic", {})
        self.data.setdefault("attributes", {})
        self.data.setdefault("coach_report", {})
        self.data.setdefault("positions", {})
        self.data.setdefault("roles", [])
        self.data.setdefault("fitness", {})
        self.data.setdefault("injuries", [])
        self.data.setdefault("match_ratings", [])
        self.data.setdefault("discipline", {})
        self.data.setdefault("contract", {})
    
    def get_name(self) -> str:
        """Возвращает имя игрока."""
        return self.data.get("basic", {}).get("name", "Неизвестный игрок")
    
    def get_position(self) -> str:
        """Возвращает основную позицию."""
        return self.data.get("basic", {}).get("position", "Unknown")
    
    def get_age(self) -> int:
        """Возвращает возраст."""
        return self.data.get("basic", {}).get("age", 0)
    
    def get_ability(self) -> int:
        """Возвращает текущую способность (CA)."""
        return self.data.get("basic", {}).get("ability", 0)
    
    def get_potential(self) -> int:
        """Возвращает потенциал (PA)."""
        return self.data.get("basic", {}).get("potential", 0)
    
    def get_attribute(self, attr_name: str) -> int:
        """
        Возвращает значение атрибута по имени.
        Ищет по всем группам (technical, mental, physical, goalkeeping, hidden).
        """
        attrs = self.data.get("attributes", {})
        for group in attrs.values():
            if isinstance(group, dict) and attr_name in group:
                return group.get(attr_name, 0)
        return 0
    
    def get_all_attributes(self) -> Dict[str, int]:
        """Возвращает плоский словарь всех атрибутов (имя -> значение)."""
        result = {}
        attrs = self.data.get("attributes", {})
        for group_name, group_data in attrs.items():
            if isinstance(group_data, dict):
                for attr_name, value in group_data.items():
                    result[attr_name] = value
        return result
    
    def get_rating_average(self) -> float:
        """Возвращает среднюю оценку за сезон."""
        ratings = self.data.get("match_ratings", [])
        if not ratings:
            return 0
        return sum(ratings) / len(ratings)
    
    def get_physical_condition(self) -> int:
        """Возвращает физическое состояние (%)."""
        return self.data.get("fitness", {}).get("condition", 0)
    
    def get_morale(self) -> int:
        """Возвращает мораль (%)."""
        return self.data.get("morale", 0)
    
    def is_injured(self) -> bool:
        """Возвращает True, если игрок травмирован."""
        injuries = self.data.get("injuries", [])
        return len(injuries) > 0
    
    def has_contract_ending_soon(self, months: int = 6) -> bool:
        """Проверяет, заканчивается ли контракт в ближайшие N месяцев."""
        # Здесь нужна логика с датами, пока заглушка
        return False
    
    def get_playing_time(self) -> str:
        """Возвращает статус игрового времени."""
        return self.data.get("basic", {}).get("playing_time", "")
    
    def to_prompt_text(self, include_hidden: bool = False) -> str:
        """
        Превращает данные игрока в текст для отправки модели.
        include_hidden — включать ли скрытые атрибуты.
        """
        lines = []
        basic = self.data.get("basic", {})
        
        lines.append(f"Игрок: {basic.get('name', 'Неизвестно')}")
        lines.append(f"Возраст: {basic.get('age', 0)}")
        lines.append(f"Позиция: {basic.get('position', 'Unknown')}")
        lines.append(f"Репутация: {basic.get('reputation', 0)}")
        lines.append(f"Текущая способность (CA): {basic.get('ability', 0)}")
        lines.append(f"Потенциал (PA): {basic.get('potential', 0)}")
        lines.append(f"Игровое время: {basic.get('playing_time', '')}")
        
        fitness = self.data.get("fitness", {})
        lines.append(f"Физическое состояние: {fitness.get('condition', 0)}%")
        lines.append(f"Мораль: {self.data.get('morale', 0)}%")
        
        injuries = self.data.get("injuries", [])
        if injuries:
            inj_str = ", ".join([i.get("type", "травма") for i in injuries])
            lines.append(f"Травмы: {inj_str}")
        else:
            lines.append("Травмы: нет")
        
        attrs = self.get_all_attributes()
        if include_hidden:
            attr_str = ", ".join([f"{k}={v}" for k, v in attrs.items() if v > 0])
        else:
            hidden = ["consistency", "dirtiness", "important_matches", "injury_prone", "versatility"]
            visible_attrs = {k: v for k, v in attrs.items() if k not in hidden}
            attr_str = ", ".join([f"{k}={v}" for k, v in visible_attrs.items() if v > 0])
        
        lines.append(f"Атрибуты: {attr_str}")
        
        report = self.data.get("coach_report", {})
        if report.get("summary"):
            lines.append(f"Отчет тренера: {report.get('summary')}")
        if report.get("strengths"):
            lines.append(f"Сильные стороны: {', '.join(report.get('strengths', []))}")
        if report.get("weaknesses"):
            lines.append(f"Слабые стороны: {', '.join(report.get('weaknesses', []))}")
        
        contract = self.data.get("contract", {})
        if contract.get("wage"):
            lines.append(f"Зарплата: {contract.get('wage')}")
        
        return "\n".join(lines)
    
    def has_changed(self, other_data: Dict[str, Any]) -> bool:
        """
        Сравнивает текущие данные с новыми.
        Возвращает True, если есть изменения.
        """
        import json
        return json.dumps(self.data, sort_keys=True) != json.dumps(other_data, sort_keys=True)
    
    def update(self, new_data: Dict[str, Any]):
        """Обновляет данные игрока новыми значениями."""
        self.data.update(new_data)
        self._normalize()
    
    @classmethod
    def from_json(cls, filepath: str):
        """Загружает игрока из JSON-файла."""
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls(data)
    
    def to_json(self, filepath: str):
        """Сохраняет данные игрока в JSON-файл."""
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)