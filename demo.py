#!/usr/bin/env python3
"""
OSINT Profiler - Demo Script
Демонстрационный скрипт для тестирования системы
"""
from core.data_manager import DataManager
from generator import ReportGenerator
from rich.console import Console
from rich.progress import track
from rich.table import Table
from rich import box
import time

console = Console()


def create_demo_target():
    """Создает демонстрационную цель с расширенной информацией"""
    demo_target = {
        "personal": {
            "full_name": "Алексей Морозов",
            "birth_date": "1993-06-15",
            "birth_place": "Санкт-Петербург, Россия",
            "gender": "male",
            "aliases": ["alex_spb", "morozov_dev", "alexey.m"],
            "photo_url": ""
        },
        "contacts": {
            "phones": ["+7-921-555-12-34", "+7-812-555-67-89"],
            "emails": ["alex.morozov@example.com", "morozov93@mail.ru", "a.morozov@vk.com"],
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
            },
            {
                "platform": "linkedin",
                "url": "https://linkedin.com/in/alexey-morozov",
                "username": "alexey-morozov",
                "followers": 156,
                "posts_count": 23
            }
        ],
        "family": [
            {
                "relation": "mother",
                "full_name": "Морозова Елена Викторовна",
                "birth_date": "1970-05-10",
                "occupation": "Врач-терапевт",
                "workplace": "Городская поликлиника №5, СПб",
                "notes": "Стаж работы 25+ лет, заслуженный врач"
            },
            {
                "relation": "father",
                "full_name": "Морозов Сергей Николаевич",
                "birth_date": "1968-08-22",
                "occupation": "Инженер-конструктор",
                "workplace": "Адмиралтейские верфи",
                "notes": "Ведущий инженер, 30+ лет опыта"
            },
            {
                "relation": "sister",
                "full_name": "Морозова Ольга Сергеевна",
                "birth_date": "1996-11-30",
                "occupation": "Дизайнер",
                "workplace": "Freelance",
                "notes": "UI/UX дизайнер, работает с крупными брендами"
            }
        ],
        "education": [
            {
                "type": "school",
                "institution": "Лицей №239",
                "location": "Санкт-Петербург",
                "start_date": "2000-09-01",
                "end_date": "2010-06-30",
                "degree": "Общее среднее образование",
                "specialization": ""
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
            },
            {
                "type": "course",
                "institution": "Coursera/edX",
                "location": "Online",
                "specialization": "Machine Learning & AI",
                "start_date": "2021-01-15",
                "end_date": "2021-06-30",
                "degree": "Certificate"
            }
        ],
        "employment": [
            {
                "company": "JetBrains",
                "position": "Junior Software Engineer",
                "location": "Санкт-Петербург",
                "start_date": "2016-07-01",
                "end_date": "2018-12-31",
                "description": "Разработка инструментов для IDE, участие в проекте IntelliJ"
            },
            {
                "company": "Яндекс",
                "position": "Senior Software Engineer",
                "location": "Санкт-Петербург",
                "start_date": "2019-01-15",
                "end_date": "2022-08-31",
                "description": "Разработка поисковых алгоритмов, оптимизация ранжирования"
            },
            {
                "company": "VK (ВКонтакте)",
                "position": "Tech Lead",
                "location": "Санкт-Петербург",
                "start_date": "2022-09-01",
                "end_date": None,
                "description": "Руководство командой разработки платформы, архитектурные решения"
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
                },
                "notes": "Детство, проживал с родителями"
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
                "notes": "Центр города, исторический район, близко к центру"
            },
            {
                "type": "work",
                "address": "Санкт-Петербург, Кантемировская ул. 2А (офис VK)",
                "start_date": "2022-09-01",
                "end_date": None,
                "coordinates": {
                    "lat": 59.9326,
                    "lon": 30.3579
                },
                "notes": "Главный офис VK, современное здание"
            }
        ],
        "connections": [
            {
                "name": "Смирнов Дмитрий",
                "relation": "colleague",
                "context": "Работали вместе в JetBrains (2016-2018), совместные проекты",
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
                "context": "Отношения с 2021 года, совместные интересы в путешествиях",
                "source": "Instagram",
                "strength": 10
            },
            {
                "name": "Сидоров Игорь",
                "relation": "colleague",
                "context": "Текущий коллега в VK, Senior Engineer в другой команде",
                "source": "LinkedIn",
                "strength": 7
            },
            {
                "name": "Волков Павел",
                "relation": "friend",
                "context": "Друг из университета, часто встречаются",
                "source": "Facebook",
                "strength": 8
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
                "date": "2000-09-01",
                "event": "Поступление в лицей №239",
                "location": "Санкт-Петербург",
                "category": "education"
            },
            {
                "date": "2010-06-30",
                "event": "Окончание лицея",
                "location": "Санкт-Петербург",
                "category": "education"
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
                "date": "2014-09-01",
                "event": "Начало магистратуры",
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
                "event": "Переход в Яндекс на должность Senior Engineer",
                "location": "Санкт-Петербург",
                "category": "employment"
            },
            {
                "date": "2021-01-15",
                "event": "Начало обучения на курсе Machine Learning",
                "location": "Online",
                "category": "education"
            },
            {
                "date": "2021-06-30",
                "event": "Завершение курса Machine Learning",
                "location": "Online",
                "category": "education"
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
            "property": [
                {
                    "type": "apartment",
                    "address": "Санкт-Петербург, ул. Рубинштейна 23, кв. 42",
                    "year_acquired": 2016,
                    "estimated_value": "5000000 RUB"
                }
            ]
        },
        "digital_footprint": [
            {
                "source": "GitHub",
                "type": "profile",
                "url": "https://github.com/morozov-dev",
                "date": "2015-03-20",
                "content": "Активный участник open-source проектов, 89 followers"
            },
            {
                "source": "VK",
                "type": "post",
                "url": "https://vk.com/wall12345_6789",
                "date": "2024-12-25",
                "content": "Новый год в офисе VK!"
            },
            {
                "source": "LinkedIn",
                "type": "profile",
                "url": "https://linkedin.com/in/alexey-morozov",
                "date": "2019-01-15",
                "content": "Tech Lead в VK, 156 connections"
            },
            {
                "source": "GitHub",
                "type": "repository",
                "url": "https://github.com/morozov-dev/ai-framework",
                "date": "2023-05-10",
                "content": "Open source ML framework, 234 stars"
            }
        ],
        "notes": """Активный разработчик, участвует в open-source проектах. 
                    Интересуется машинным обучением и алгоритмами. 
                    Живёт в центре Санкт-Петербурга, работает в VK на должности Tech Lead.
                    Опытный инженер с глубокими знаниями в области backend-разработки.
                    Лидер команды, занимается наставничеством junior разработчиков.""",
        "tags": ["IT", "developer", "SPb", "VK", "Python", "open-source", "ML", "C++", "Architecture", "Tech Lead"]
    }
    return demo_target


def show_demo_statistics(target: dict):
    """Показывает статистику по демо-цели"""
    stats_table = Table(title="📊 Статистика профиля", box=box.ROUNDED, border_style="cyan")
    stats_table.add_column("Параметр", style="cyan")
    stats_table.add_column("Значение", justify="right", style="green")
    
    stats_table.add_row("Соцсети", str(len(target.get('social_media', []))))
    stats_table.add_row("Связи", str(len(target.get('connections', []))))
    stats_table.add_row("Адреса", str(len(target.get('addresses', []))))
    stats_table.add_row("Места работы", str(len(target.get('employment', []))))
    stats_table.add_row("Образование", str(len(target.get('education', []))))
    stats_table.add_row("Члены семьи", str(len(target.get('family', []))))
    stats_table.add_row("События в таймлайне", str(len(target.get('timeline', []))))
    stats_table.add_row("Цифровой след", str(len(target.get('digital_footprint', []))))
    stats_table.add_row("Активы", str(len(target.get('assets', {}).get('vehicles', [])) + len(target.get('assets', {}).get('property', []))))
    stats_table.add_row("Теги", str(len(target.get('tags', []))))
    
    console.print(stats_table)


def main():
    """Главная функция демо"""
    console.print("\n[bold cyan]╔═══════════════════════════════════════════╗[/bold cyan]")
    console.print("[bold cyan]║   OSINT Profiler - Advanced Demo Script   ║[/bold cyan]")
    console.print("[bold cyan]╚═══════════════════════════════════════════╝[/bold cyan]\n")

    # Инициализация
    console.print("[yellow]→ Инициализация системы...[/yellow]")
    dm = DataManager()
    generator = ReportGenerator()
    
    for step in track(range(5), description="[cyan]Загрузка компонентов..."):
        time.sleep(0.1)

    # Создание демо-цели
    console.print("\n[yellow]→ Создание демонстрационной цели с расширенными данными...[/yellow]")
    demo_target = create_demo_target()
    
    for step in track(range(10), description="[cyan]Обработка данных..."):
        time.sleep(0.1)
    
    target_id = dm.create_target(demo_target)
    console.print(f"\n[bold green]✓ Демо-цель создана![/bold green] [dim]ID: {target_id}[/dim]\n")

    # Показываем статистику
    console.print("[bold cyan]Информация о профиле:[/bold cyan]\n")
    console.print(f"[yellow]Имя:[/yellow] {demo_target['personal']['full_name']}")
    console.print(f"[yellow]Дата рождения:[/yellow] {demo_target['personal']['birth_date']}")
    console.print(f"[yellow]Место рождения:[/yellow] {demo_target['personal']['birth_place']}")
    console.print(f"[yellow]Псевдонимы:[/yellow] {', '.join(demo_target['personal']['aliases'])}")
    
    show_demo_statistics(demo_target)

    # Генерация отчёта
    console.print("\n[yellow]→ Генерация HTML-отчёта...[/yellow]")
    for step in track(range(15), description="[cyan]Рендеринг шаблона..."):
        time.sleep(0.08)
    
    try:
        output_path = generator.generate_report(target_id)
        console.print(f"\n[bold green]✓ Отчёт успешно создан![/bold green]")
        console.print(f"[cyan]→ Путь:[/cyan] {output_path}\n")
    except Exception as e:
        console.print(f"\n[bold red]✗ Ошибка при генерации отчета:[/bold red] {e}\n")
        return

    # Генерация сводного отчета
    console.print("[yellow]→ Генерация сводного отчёта...[/yellow]")
    for step in track(range(8), description="[cyan]Обработка данных..."):
        time.sleep(0.1)
    
    try:
        summary_path = generator.generate_summary_report()
        console.print(f"\n[bold green]✓ Сводный отчёт успешно создан![/bold green]")
        console.print(f"[cyan]→ Путь:[/cyan] {summary_path}\n")
    except Exception as e:
        console.print(f"\n[bold red]✗ Ошибка при генерации сводного отчета:[/bold red] {e}\n")

    # Успешное завершение
    console.print("[bold green]🎉 Демонстрация завершена![/bold green]")
    console.print("[dim]→ Откройте HTML-файлы в браузере для просмотра отчётов[/dim]")
    console.print("[dim]→ Используйте главное приложение для работы с другими целями[/dim]\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        console.print(f"\n[bold red]💥 Критическая ошибка:[/bold red] {e}\n")
