"""
OSINT Profiler - Report Generator
Генератор HTML-отчетов из данных OSINT
"""
import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape
from typing import Dict, Optional, List
from core.data_manager import DataManager

class ReportGenerator:
    """Класс для генерации HTML-отчетов"""

    def __init__(self, templates_dir: str = "templates", output_dir: str = "output"):
        self.templates_dir = templates_dir
        self.output_dir = output_dir
        self.data_manager = DataManager()

        # Настраиваем Jinja2
        self.env = Environment(
            loader=FileSystemLoader([self.templates_dir, "."]),
            autoescape=select_autoescape(['html', 'xml'])
        )

        # Добавляем кастомные фильтры
        self.env.filters['format_date'] = self._format_date
        self.env.filters['age'] = self._calculate_age
        self.env.filters['duration_years'] = self._calculate_duration

        # Создаем output директорию
        os.makedirs(output_dir, exist_ok=True)

    def _format_date(self, date_string: str, format: str = "%d.%m.%Y") -> str:
        """Форматирует дату"""
        if not date_string:
            return "N/A"
        
        try:
            # Используем replace для корректной обработки Z-суффикса
            date_obj = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
            return date_obj.strftime(format)
        except (ValueError, TypeError, AttributeError):
            # Если формат не распознан, возвращаем как есть
            return str(date_string) if date_string else "N/A"

    def _calculate_age(self, birth_date: str) -> int:
        """Вычисляет возраст"""
        if not birth_date:
            return 0
        
        try:
            # Используем replace для корректной обработки Z-суффикса
            birth = datetime.fromisoformat(birth_date.replace('Z', '+00:00'))
            today = datetime.now()
            age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
            return max(0, age)  # Не возвращаем отрицательный возраст
        except (ValueError, TypeError, AttributeError):
            # Если формат даты неверен, возвращаем 0
            return 0

    def _calculate_duration(self, start_date: str, end_date: Optional[str] = None) -> str:
        """Вычисляет продолжительность между двумя датами"""
        if not start_date:
            return "N/A"
        
        try:
            start = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            
            if end_date:
                end = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            else:
                end = datetime.now()
            
            delta = end - start
            years = delta.days // 365
            months = (delta.days % 365) // 30
            
            if years > 0:
                return f"{years} г. {months} мес." if months > 0 else f"{years} года"
            else:
                return f"{months} месяцев"
        except (ValueError, TypeError, AttributeError):
            return "N/A"

    def _prepare_data(self, target: Dict) -> Dict:
        """
        Подготавливает данные для шаблона

        Args:
            target: Данные цели

        Returns:
            Обработанные данные
        """
        # Безопасная сортировка timeline
        if 'timeline' in target and target.get('timeline'):
            valid_timeline_items = []
            for item in target['timeline']:
                if 'date' in item and item['date']:
                    try:
                        # Проверяем формат даты (YYYY-MM-DD)
                        datetime.fromisoformat(item['date'].replace('Z', '+00:00'))
                        valid_timeline_items.append(item)
                    except (ValueError, AttributeError):
                        # Пропускаем элементы с некорректной датой
                        print(f"⚠️  Некорректная дата в timeline: {item.get('date', 'N/A')} для цели {target.get('id', 'N/A')}. Пропущено.")
                        continue
            # Сортируем только валидные элементы
            target['timeline'] = sorted(valid_timeline_items, key=lambda x: x['date'], reverse=True)

        # Безопасная сортировка образования
        if 'education' in target and target.get('education'):
            valid_education = []
            for edu in target['education']:
                if 'start_date' in edu and edu['start_date']:
                    try:
                        datetime.fromisoformat(edu['start_date'].replace('Z', '+00:00'))
                        valid_education.append(edu)
                    except (ValueError, AttributeError):
                        continue
            target['education'] = sorted(valid_education, 
                                        key=lambda x: x.get('start_date', ''), 
                                        reverse=True)

        # Безопасная сортировка трудовой истории
        if 'employment' in target and target.get('employment'):
            valid_employment = []
            for job in target['employment']:
                if 'start_date' in job and job['start_date']:
                    try:
                        datetime.fromisoformat(job['start_date'].replace('Z', '+00:00'))
                        valid_employment.append(job)
                    except (ValueError, AttributeError):
                        continue
            target['employment'] = sorted(valid_employment, 
                                         key=lambda x: x.get('start_date', ''), 
                                         reverse=True)

        # Считаем статистику, проверяя наличие ключей
        stats = {
            'social_accounts': len(target.get('social_media', [])),
            'connections': len(target.get('connections', [])),
            'addresses': len(target.get('addresses', [])),
            'jobs': len(target.get('employment', [])),
            'education': len(target.get('education', [])),
            'family': len(target.get('family', [])),
            'assets': len(target.get('assets', {}).get('vehicles', [])) + len(target.get('assets', {}).get('property', []))
        }
        target['stats'] = stats

        return target

    def _sanitize_filename(self, filename: str, max_length: int = 100) -> str:
        """Очищает имя файла от недопустимых символов"""
        # Удаляем недопустимые символы
        safe_name = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_', '.'))
        # Удаляем пробелы в начале и конце
        safe_name = safe_name.strip()
        # Ограничиваем длину
        if len(safe_name) > max_length:
            safe_name = safe_name[:max_length]
        # Если имя пустое, используем дефолт
        return safe_name if safe_name else "report"

    def generate_report(self, target_id: str, output_filename: Optional[str] = None) -> str:
        """
        Генерирует HTML-отчет для цели

        Args:
            target_id: ID цели
            output_filename: Имя выходного файла (опционально)

        Returns:
            Путь к созданному файлу
            
        Raises:
            ValueError: Если цель не найдена
        """
        # Получаем данные цели
        target = self.data_manager.get_target(target_id)

        if not target:
            raise ValueError(f"Цель с ID {target_id} не найдена")

        # Подготавливаем данные
        target = self._prepare_data(target)

        # Загружаем шаблон
        try:
            template = self.env.get_template('report.html')
        except Exception as e:
            raise ValueError(f"Ошибка при загрузке шаблона: {e}")

        # Рендерим HTML
        html_content = template.render(target=target, generated_at=datetime.now())

        # Определяем имя файла
        if not output_filename:
            # Используем 'full_name' из 'personal', если существует, иначе 'target_id'
            safe_name_part = target.get('personal', {}).get('full_name', target_id)
            safe_name = self._sanitize_filename(safe_name_part)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_filename = f"{safe_name}_{timestamp}.html"

        # Сохраняем файл
        output_path = os.path.join(self.output_dir, output_filename)
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
        except IOError as e:
            raise ValueError(f"Ошибка при сохранении файла: {e}")

        return output_path

    def generate_all_reports(self) -> List[str]:
        """
        Генерирует отчеты для всех целей
        
        Returns:
            Список путей к созданным файлам
        """
        targets = self.data_manager.get_all_targets()
        generated = []

        for target in targets:
            try:
                path = self.generate_report(target['id'])
                generated.append(path)
                print(f"✅ Отчет создан: {path}")
            except Exception as e:
                print(f"❌ Ошибка при создании отчета для {target.get('id', 'unknown')}: {e}")

        return generated

def __init__(self, templates_dir: str = "templates", output_dir: str = "output"):
    self.templates_dir = templates_dir
    self.output_dir = output_dir
    self.data_manager = DataManager()

    # Настраиваем Jinja2 - добавляем текущую директорию и родительскую
    self.env = Environment(
        loader=FileSystemLoader([
            self.templates_dir,
            ".",  # Текущая директория
            os.path.dirname(__file__)  # Директория со скриптом
        ]),
        autoescape=select_autoescape(['html', 'xml'])
    )
    # ...

    def preview_report(self, target_id: str) -> str:
        """
        Генерирует отчет и возвращает HTML для предпросмотра

        Args:
            target_id: ID цели

        Returns:
            HTML-код отчета
            
        Raises:
            ValueError: Если цель не найдена
        """
        target = self.data_manager.get_target(target_id)

        if not target:
            raise ValueError(f"Цель с ID {target_id} не найдена")

        target = self._prepare_data(target)
        template = self.env.get_template('report.html')

        return template.render(target=target, generated_at=datetime.now())

    def generate_summary_report(self, output_filename: str = "summary.html") -> str:
        """
        Генерирует сводный отчет по всем целям
        
        Args:
            output_filename: Имя выходного файла
            
        Returns:
            Путь к созданному файлу
        """
        targets = self.data_manager.get_all_targets()
        
        # Подготавливаем сводные данные
        summary_data = {
            'total_targets': len(targets),
            'total_connections': sum(len(t.get('connections', [])) for t in targets),
            'total_addresses': sum(len(t.get('addresses', [])) for t in targets),
            'total_social_accounts': sum(len(t.get('social_media', [])) for t in targets),
            'generated_at': datetime.now(),
            'targets': targets
        }
        
        # Если есть summary.html шаблон, используем его, иначе создаем базовый
        try:
            template = self.env.get_template('summary.html')
        except:
            # Создаем базовый отчет
            template = self.env.from_string(self._get_default_summary_template())
        
        html_content = template.render(**summary_data)
        
        output_path = os.path.join(self.output_dir, output_filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return output_path

    def _get_default_summary_template(self) -> str:
        """Возвращает дефолтный шаблон сводного отчета"""
        return """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>OSINT Summary Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; }
        h1 { color: #333; border-bottom: 2px solid #007bff; padding-bottom: 10px; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }
        .stat-card { background: #f9f9f9; border-left: 4px solid #007bff; padding: 15px; }
        .stat-value { font-size: 32px; font-weight: bold; color: #007bff; }
        .stat-label { color: #666; margin-top: 5px; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background: #007bff; color: white; }
        tr:hover { background: #f9f9f9; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Сводный отчет OSINT</h1>
        <p>Создан: {{ generated_at.strftime('%Y-%m-%d %H:%M:%S') }}</p>
        
        <h2>Статистика</h2>
        <div class="stats">
            <div class="stat-card">
                <div class="stat-value">{{ total_targets }}</div>
                <div class="stat-label">Всего целей</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{{ total_connections }}</div>
                <div class="stat-label">Всего связей</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{{ total_addresses }}</div>
                <div class="stat-label">Всего адресов</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{{ total_social_accounts }}</div>
                <div class="stat-label">Соцсетей</div>
            </div>
        </div>
        
        <h2>Цели</h2>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Имя</th>
                    <th>Связи</th>
                    <th>Адреса</th>
                    <th>Соцсети</th>
                </tr>
            </thead>
            <tbody>
                {% for target in targets %}
                <tr>
                    <td>{{ target.id }}</td>
                    <td>{{ target.personal.full_name }}</td>
                    <td>{{ target.connections|length }}</td>
                    <td>{{ target.addresses|length }}</td>
                    <td>{{ target.social_media|length }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</body>
</html>
        """


if __name__ == "__main__":
    # Пример использования
    generator = ReportGenerator()

    # Получаем все цели
    dm = DataManager()
    targets = dm.get_all_targets()

    if targets:
        # Генерируем отчет для первой цели
        target_id = targets[0]['id']
        try:
            output_path = generator.generate_report(target_id)
            print(f"🎯 Отчет создан: {output_path}")
            
            # Генерируем сводный отчет
            summary_path = generator.generate_summary_report()
            print(f"📊 Сводный отчет создан: {summary_path}")
        except Exception as e:
            print(f"❌ Ошибка: {e}")
    else:
        print("❌ Нет целей в базе данных")
