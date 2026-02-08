#!/usr/bin/env python3
"""
OSINT Profiler - Demo Script
Демонстрационный скрипт для тестирования системы
"""

from core.data_manager import DataManager
from generator import ReportGenerator
from rich.console import Console
from rich.progress import track
import time

console = Console()

def create_demo_target():
    """Создает демонстрационную цель"""
    
    demo_target = {
        "personal": {
            "full_name": "Алексей Морозов",
            "birth_date": "1993-06-15",
            "birth_place": "Санкт-Петербург, Россия",
            "gender": "male",
            "aliases": ["alex_spb", "morozov_dev"],
            "photo_url": ""
        },
        "contacts": {
            "phones": ["+7-921-555-12-34", "+7-812-555-67-89"],
            "emails": ["alex.morozov@example.com", "morozov93@mail.ru"],
            "messengers": {
                "telegram": "@alex_morozov",
                "whatsapp": "+7-921-555-12-34",
                "skype": "alex.spb"
            }
        },
        "social_media": [
            {
                "platform": "vk",
                "url": "https://vk.com/alex_spb",
                "username": "alex_spb",
                "followers": 523,
                "posts_count": 187
            },
            {
                "platform": "instagram",
                "url": "https://instagram.com/alex.morozov",
                "username": "alex.morozov",
                "followers": 1240,
                "posts_count": 95
            },
            {
                "platform": "github",
                "url": "https://github.com/morozov-dev",
                "username": "morozov-dev",
                "followers": 89,
                "posts_count": 45
            }
        ],
        "family": [
            {
                "relation": "mother",
                "full_name": "Морозова Елена Викторовна",
                "birth_year": 1970,
                "occupation": "Врач-терапевт",
                "workplace": "Городская поликлиника №5, СПб",
                "notes": "Стаж работы 25+ лет"
            },
            {
                "relation": "father",
                "full_name": "Морозов Сергей Николаевич",
                "birth_year": 1968,
                "occupation": "Инженер-конструктор",
                "workplace": "Адмиралтейские верфи",
                "notes": "Ведущий инженер"
            },
            {
                "relation": "sister",
                "full_name": "Морозова Ольга Сергеевна",
                "birth_year": 1996,
                "occupation": "Дизайнер",
                "workplace": "Freelance",
                "notes": "UI/UX дизайнер"
            }
        ],
        "education": [
            {
                "type": "school",
                "institution": "Лицей №239",
                "location": "Санкт-Петербург",
                "start_date": "2000-09-01",
                "end_date": "2010-06-30",
                "degree": "Общее среднее образование"
            },
            {
                "type": "university",
                "institution": "СПбПУ Петра Великого",
                "location": "Санкт-Петербург",
                "faculty": "Институт компьютерных наук и технологий",
                "specialization": "Программная инженерия",
                "start_date": "2010-09-01",
                "end_date": "2014-06-30",
                "degree": "Бакалавр"
            },
            {
                "type": "university",
                "institution": "СПбПУ Петра Великого",
                "location": "Санкт-Петербург",
                "faculty": "Институт компьютерных наук и технологий",
                "specialization": "Программная инженерия",
                "start_date": "2014-09-01",
                "end_date": "2016-06-30",
                "degree": "Магистр"
            }
        ],
        "employment": [
            {
                "company": "JetBrains",
                "position": "Junior Software Engineer",
                "location": "Санкт-Петербург",
                "start_date": "2016-07-01",
                "end_date": "2018-12-31",
                "description": "Разработка инструментов для IDE"
            },
            {
                "company": "Яндекс",
                "position": "Senior Software Engineer",
                "location": "Санкт-Петербург",
                "start_date": "2019-01-15",
                "end_date": "2022-08-31",
                "description": "Разработка поисковых алгоритмов"
            },
            {
                "company": "VK (ВКонтакте)",
                "position": "Tech Lead",
                "location": "Санкт-Петербург",
                "start_date": "2022-09-01",
                "end_date": None,
                "description": "Руководство командой разработки платформы"
            }
        ],
        "addresses": [
            {
                "type": "residence",
                "address": "Санкт-Петербург, пр. Просвещения 87, кв. 15",
                "start_date": "1993-06-15",
                "end_date": "2016-08-01",
                "coordinates": {
                    "lat": 60.0446,
                    "lon": 30.3262
                }
            },
            {
                "type": "residence",
                "address": "Санкт-Петербург, ул. Рубинштейна 23, кв. 42",
                "start_date": "2016-08-01",
                "end_date": None,
                "coordinates": {
                    "lat": 59.9280,
                    "lon": 30.3466
                },
                "notes": "Центр города, исторический район"
            },
            {
                "type": "work",
                "address": "Санкт-Петербург, Кантемировская ул. 2А (офис VK)",
                "start_date": "2022-09-01",
                "end_date": None,
                "coordinates": {
                    "lat": 59.9326,
                    "lon": 30.3579
                }
            }
        ],
        "connections": [
            {
                "name": "Смирнов Дмитрий",
                "relation": "colleague",
                "context": "Работали вместе в JetBrains (2016-2018)",
                "source": "LinkedIn",
                "strength": 7
            },
            {
                "name": "Петрова Анна",
                "relation": "friend",
                "context": "Одноклассница по лицею, поддерживают связь",
                "source": "VK",
                "strength": 9
            },
            {
                "name": "Кузнецов Максим",
                "relation": "colleague",
                "context": "Коллега в Яндексе, Tech Lead соседней команды",
                "source": "LinkedIn",
                "strength": 8
            },
            {
                "name": "Иванова Мария",
                "relation": "girlfriend",
                "context": "Отношения с 2021 года",
                "source": "Instagram",
                "strength": 10
            },
            {
                "name": "Сидоров Игорь",
                "relation": "colleague",
                "context": "Текущий коллега в VK, Senior Engineer",
                "source": "LinkedIn",
                "strength": 7
            }
        ],
        "timeline": [
            {
                "date": "1993-06-15",
                "event": "Рождение",
                "location": "Санкт-Петербург",
                "category": "personal"
            },
            {
                "date": "2010-09-01",
                "event": "Поступление в СПбПУ",
                "location": "Санкт-Петербург",
                "category": "education"
            },
            {
                "date": "2014-06-30",
                "event": "Получение диплома бакалавра",
                "location": "Санкт-Петербург",
                "category": "education"
            },
            {
                "date": "2016-06-30",
                "event": "Получение диплома магистра",
                "location": "Санкт-Петербург",
                "category": "education"
            },
            {
                "date": "2016-07-01",
                "event": "Начало работы в JetBrains",
                "location": "Санкт-Петербург",
                "category": "employment"
            },
            {
                "date": "2016-08-01",
                "event": "Переезд в собственную квартиру",
                "location": "Санкт-Петербург, ул. Рубинштейна",
                "category": "relocation"
            },
            {
                "date": "2019-01-15",
                "event": "Переход в Яндекс",
                "location": "Санкт-Петербург",
                "category": "employment"
            },
            {
                "date": "2022-09-01",
                "event": "Повышение до Tech Lead в VK",
                "location": "Санкт-Петербург",
                "category": "employment"
            }
        ],
        "assets": {
            "vehicles": [
                {
                    "type": "car",
                    "brand": "Skoda",
                    "model": "Octavia",
                    "year": 2020,
                    "plate_number": "А777АА178",
                    "color": "серый"
                }
            ],
            "property": []
        },
        "digital_footprint": [
            {
                "source": "GitHub",
                "type": "profile",
                "url": "https://github.com/morozov-dev",
                "date": "2015-03-20",
                "content": "Активный участник open-source проектов"
            },
            {
                "source": "VK",
                "type": "post",
                "url": "https://vk.com/wall12345_6789",
                "date": "2024-12-25",
                "content": "Новый год в офисе VK!"
            }
        ],
        "notes": "Активный разработчик, участвует в open-source проектах. Интересуется машинным обучением и алгоритмами. Живёт в центре Санкт-Петербурга, работает в VK на должности Tech Lead.",
        "tags": ["IT", "developer", "SPb", "VK", "Python", "open-source"]
    }
    
    return demo_target


def main():
    """Главная функция демо"""
    console.print("\n[bold cyan]╔═══════════════════════════════════╗[/bold cyan]")
    console.print("[bold cyan]║   OSINT Profiler - Demo Script   ║[/bold cyan]")
    console.print("[bold cyan]╚═══════════════════════════════════╝[/bold cyan]\n")
    
    # Инициализация
    console.print("[yellow]→ Инициализация системы...[/yellow]")
    dm = DataManager()
    generator = ReportGenerator()
    time.sleep(0.5)
    
    # Создание демо-цели
    console.print("[yellow]→ Создание демонстрационной цели...[/yellow]")
    demo_target = create_demo_target()
    
    for step in track(range(5), description="[cyan]Сохранение данных..."):
        time.sleep(0.2)
    
    target_id = dm.create_target(demo_target)
    console.print(f"[green]✓ Демо-цель создана![/green] [dim]ID: {target_id}[/dim]\n")
    
    # Генерация отчёта
    console.print("[yellow]→ Генерация HTML-отчёта...[/yellow]")
    
    for step in track(range(10), description="[cyan]Рендеринг шаблона..."):
        time.sleep(0.15)
    
    output_path = generator.generate_report(target_id)
    
    console.print(f"\n[bold green]✓ Отчёт успешно создан![/bold green]")
    console.print(f"[cyan]→ Путь:[/cyan] {output_path}\n")
    
    # Статистика
    console.print("[bold cyan]Статистика демо-профиля:[/bold cyan]")
    console.print(f"  [dim]→[/dim] Соцсети: [green]{len(demo_target['social_media'])}[/green]")
    console.print(f"  [dim]→[/dim] Связи: [green]{len(demo_target['connections'])}[/green]")
    console.print(f"  [dim]→[/dim] Адреса: [green]{len(demo_target['addresses'])}[/green]")
    console.print(f"  [dim]→[/dim] Места работы: [green]{len(demo_target['employment'])}[/green]")
    console.print(f"  [dim]→[/dim] Событий в таймлайне: [green]{len(demo_target['timeline'])}[/green]\n")
    
    console.print("[bold green]🎉 Демонстрация завершена![/bold green]")
    console.print("[dim]Откройте HTML-файл в браузере для просмотра отчёта[/dim]\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        console.print(f"\n[bold red]Ошибка:[/bold red] {e}\n")