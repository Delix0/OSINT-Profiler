"""
OSINT Profiler - Report Generator
Генератор HTML-отчетов из данных OSINT
"""

import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape
from typing import Dict, Optional
from core.data_manager import DataManager


class ReportGenerator:
    """Класс для генерации HTML-отчетов"""
    
    def __init__(self, templates_dir: str = "templates", output_dir: str = "output"):
        self.templates_dir = templates_dir
        self.output_dir = output_dir
        self.data_manager = DataManager()
        
        # Настраиваем Jinja2
        self.env = Environment(
            loader=FileSystemLoader(templates_dir),
            autoescape=select_autoescape(['html', 'xml'])
        )
        
        # Добавляем кастомные фильтры
        self.env.filters['format_date'] = self._format_date
        self.env.filters['age'] = self._calculate_age
        
        # Создаем output директорию
        os.makedirs(output_dir, exist_ok=True)
    
    def _format_date(self, date_string: str, format: str = "%d.%m.%Y") -> str:
        """Форматирует дату"""
        try:
            date_obj = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
            return date_obj.strftime(format)
        except:
            return date_string
    
    def _calculate_age(self, birth_date: str) -> int:
        """Вычисляет возраст"""
        try:
            birth = datetime.fromisoformat(birth_date)
            today = datetime.now()
            age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
            return age
        except:
            return 0
    
    def _prepare_data(self, target: Dict) -> Dict:
        """
        Подготавливает данные для шаблона
        
        Args:
            target: Данные цели
            
        Returns:
            Обработанные данные
        """
        # Сортируем timeline по дате
        if 'timeline' in target and target['timeline']:
            target['timeline'] = sorted(target['timeline'], key=lambda x: x['date'])
        
        # Считаем статистику
        stats = {
            'social_accounts': len(target.get('social_media', [])),
            'connections': len(target.get('connections', [])),
            'addresses': len(target.get('addresses', [])),
            'jobs': len(target.get('employment', [])),
            'education': len(target.get('education', []))
        }
        
        target['stats'] = stats
        
        return target
    
    def generate_report(self, target_id: str, output_filename: Optional[str] = None) -> str:
        """
        Генерирует HTML-отчет для цели
        
        Args:
            target_id: ID цели
            output_filename: Имя выходного файла (опционально)
            
        Returns:
            Путь к созданному файлу
        """
        # Получаем данные цели
        target = self.data_manager.get_target(target_id)
        
        if not target:
            raise ValueError(f"Цель с ID {target_id} не найдена")
        
        # Подготавливаем данные
        target = self._prepare_data(target)
        
        # Загружаем шаблон
        template = self.env.get_template('report.html')
        
        # Рендерим HTML
        html_content = template.render(target=target, generated_at=datetime.now())
        
        # Определяем имя файла
        if not output_filename:
            safe_name = target['personal']['full_name'].replace(' ', '_')
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_filename = f"{safe_name}_{timestamp}.html"
        
        # Сохраняем файл
        output_path = os.path.join(self.output_dir, output_filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return output_path
    
    def generate_all_reports(self):
        """Генерирует отчеты для всех целей"""
        targets = self.data_manager.get_all_targets()
        generated = []
        
        for target in targets:
            try:
                path = self.generate_report(target['id'])
                generated.append(path)
                print(f"✅ Отчет создан: {path}")
            except Exception as e:
                print(f"❌ Ошибка при создании отчета для {target['id']}: {e}")
        
        return generated
    
    def preview_report(self, target_id: str) -> str:
        """
        Генерирует отчет и возвращает HTML для предпросмотра
        
        Args:
            target_id: ID цели
            
        Returns:
            HTML-код отчета
        """
        target = self.data_manager.get_target(target_id)
        
        if not target:
            raise ValueError(f"Цель с ID {target_id} не найдена")
        
        target = self._prepare_data(target)
        template = self.env.get_template('report.html')
        
        return template.render(target=target, generated_at=datetime.now())


if __name__ == "__main__":
    # Пример использования
    generator = ReportGenerator()
    
    # Получаем все цели
    dm = DataManager()
    targets = dm.get_all_targets()
    
    if targets:
        # Генерируем отчет для первой цели
        target_id = targets[0]['id']
        output_path = generator.generate_report(target_id)
        print(f"🎯 Отчет создан: {output_path}")
    else:
        print("❌ Нет целей в базе данных")