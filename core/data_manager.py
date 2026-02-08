"""
OSINT Profiler - Data Manager
Модуль для работы с базой данных (CRUD операции)
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import uuid


class DataManager:
    """Класс для управления базой данных OSINT-целей"""
    
    def __init__(self, db_path: str = "data/database.json"):
        self.db_path = db_path
        self._ensure_db_exists()
    
    def _ensure_db_exists(self):
        """Создает файл БД если его нет"""
        if not os.path.exists(self.db_path):
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            self._save_data({"targets": []})
    
    def _load_data(self) -> Dict:
        """Загружает данные из JSON"""
        with open(self.db_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _save_data(self, data: Dict):
        """Сохраняет данные в JSON"""
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def create_target(self, target_data: Dict) -> str:
        """
        Создает новую цель
        
        Args:
            target_data: Словарь с данными цели
            
        Returns:
            ID созданной цели
        """
        data = self._load_data()
        
        # Генерируем ID если его нет
        if 'id' not in target_data:
            target_data['id'] = f"target_{uuid.uuid4().hex[:8]}"
        
        # Добавляем временные метки
        now = datetime.now().isoformat()
        target_data['created_at'] = now
        target_data['updated_at'] = now
        
        data['targets'].append(target_data)
        self._save_data(data)
        
        return target_data['id']
    
    def get_target(self, target_id: str) -> Optional[Dict]:
        """
        Получает цель по ID
        
        Args:
            target_id: ID цели
            
        Returns:
            Словарь с данными цели или None
        """
        data = self._load_data()
        
        for target in data['targets']:
            if target['id'] == target_id:
                return target
        
        return None
    
    def get_all_targets(self) -> List[Dict]:
        """
        Получает список всех целей
        
        Returns:
            Список словарей с данными целей
        """
        data = self._load_data()
        return data['targets']
    
    def update_target(self, target_id: str, updates: Dict) -> bool:
        """
        Обновляет данные цели
        
        Args:
            target_id: ID цели
            updates: Словарь с обновлениями
            
        Returns:
            True если обновление прошло успешно
        """
        data = self._load_data()
        
        for i, target in enumerate(data['targets']):
            if target['id'] == target_id:
                # Обновляем поля
                target.update(updates)
                target['updated_at'] = datetime.now().isoformat()
                data['targets'][i] = target
                self._save_data(data)
                return True
        
        return False
    
    def delete_target(self, target_id: str) -> bool:
        """
        Удаляет цель
        
        Args:
            target_id: ID цели
            
        Returns:
            True если удаление прошло успешно
        """
        data = self._load_data()
        
        for i, target in enumerate(data['targets']):
            if target['id'] == target_id:
                data['targets'].pop(i)
                self._save_data(data)
                return True
        
        return False
    
    def search_targets(self, query: str) -> List[Dict]:
        """
        Ищет цели по запросу (в именах, тегах, заметках)
        
        Args:
            query: Поисковый запрос
            
        Returns:
            Список найденных целей
        """
        data = self._load_data()
        results = []
        query_lower = query.lower()
        
        for target in data['targets']:
            # Ищем в имени
            if 'personal' in target and 'full_name' in target['personal']:
                if query_lower in target['personal']['full_name'].lower():
                    results.append(target)
                    continue
            
            # Ищем в тегах
            if 'tags' in target:
                if any(query_lower in tag.lower() for tag in target['tags']):
                    results.append(target)
                    continue
            
            # Ищем в заметках
            if 'notes' in target and query_lower in target['notes'].lower():
                results.append(target)
        
        return results
    
    def add_timeline_event(self, target_id: str, event: Dict) -> bool:
        """
        Добавляет событие в таймлайн цели
        
        Args:
            target_id: ID цели
            event: Словарь с данными события
            
        Returns:
            True если добавление прошло успешно
        """
        target = self.get_target(target_id)
        
        if not target:
            return False
        
        if 'timeline' not in target:
            target['timeline'] = []
        
        target['timeline'].append(event)
        
        # Сортируем по дате
        target['timeline'].sort(key=lambda x: x['date'])
        
        return self.update_target(target_id, target)
    
    def add_connection(self, target_id: str, connection: Dict) -> bool:
        """
        Добавляет связь к цели
        
        Args:
            target_id: ID цели
            connection: Словарь с данными связи
            
        Returns:
            True если добавление прошло успешно
        """
        target = self.get_target(target_id)
        
        if not target:
            return False
        
        if 'connections' not in target:
            target['connections'] = []
        
        target['connections'].append(connection)
        
        return self.update_target(target_id, target)


if __name__ == "__main__":
    # Пример использования
    dm = DataManager()
    
    # Создаем тестовую цель
    test_target = {
        "personal": {
            "full_name": "Тестовый Пользователь",
            "birth_date": "1990-01-01"
        },
        "tags": ["test"]
    }
    
    target_id = dm.create_target(test_target)
    print(f"✅ Создана цель: {target_id}")
    
    # Получаем цель
    target = dm.get_target(target_id)
    print(f"📋 Цель: {target['personal']['full_name']}")
    
    # Обновляем
    dm.update_target(target_id, {"notes": "Тестовая цель"})
    print("✏️ Цель обновлена")