#!/usr/bin/env python3
"""
OSINT Profiler - Main Application
Главный файл приложения с CLI-интерфейсом
"""
import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich import box
from rich.text import Text
from core.data_manager import DataManager
from generator import ReportGenerator
import json
from datetime import datetime
import re

console = Console()


class OSINTProfilerCLI:
    """CLI-интерфейс для OSINT Profiler"""

    def __init__(self):
        self.dm = DataManager()
        self.generator = ReportGenerator()

    def show_banner(self):
        """Показывает баннер приложения"""
        banner = """
╔═══════════════════════════════════════════════╗
║   ░█████╗░░██████╗██╗███╗░░██╗████████╗       ║
║   ██╔══██╗██╔════╝██║████╗░██║╚══██╔══╝       ║
║   ██║░░██║╚█████╗░██║██╔██╗██║░░░██║░░░       ║
║   ██║░░██║░╚═══██╗██║██║╚████║░░░██║░░░       ║
║   ╚█████╔╝██████╔╝██║██║░╚███║░░░██║░░░       ║
║   ░╚════╝░╚═════╝░╚═╝╚═╝░░╚══╝░░░╚═╝░░░       ║
║         P R O F I L E R   v1.1                ║
║         Telegram: @Delix0_Tgk                 ║
╚═══════════════════════════════════════════════╝
"""
        console.print(banner, style="bold cyan")
        console.print("\n[dim]Система сбора и анализа OSINT-данных[/dim]\n")

    def show_main_menu(self):
        """Показывает главное меню"""
        table = Table(show_header=False, box=box.ROUNDED, border_style="cyan")
        table.add_row("[1]", "[cyan]Создать новую цель[/cyan]")
        table.add_row("[2]", "[cyan]Просмотреть цели[/cyan]")
        table.add_row("[3]", "[cyan]Редактировать цель[/cyan]")
        table.add_row("[4]", "[cyan]Генерировать отчёт[/cyan]")
        table.add_row("[5]", "[cyan]Генерировать все отчёты[/cyan]")
        table.add_row("[6]", "[cyan]Удалить цель[/cyan]")
        table.add_row("[7]", "[cyan]Поиск[/cyan]")
        table.add_row("[8]", "[cyan]Статистика[/cyan]")
        table.add_row("[9]", "[cyan]Экспорт/Импорт[/cyan]")
        table.add_row("[0]", "[red]Выход[/red]")

        console.print(Panel(table, title="[bold cyan]Главное меню[/bold cyan]", border_style="cyan"))

    def create_target_wizard(self):
        """Мастер создания новой цели"""
        console.print("\n[bold cyan]╔═══ Создание новой цели ═══╗[/bold cyan]\n")

        target = {
            "personal": {},
            "contacts": {},
            "social_media": [],
            "family": [],
            "education": [],
            "employment": [],
            "addresses": [],
            "connections": [],
            "timeline": [],
            "tags": [],
            "notes": "",
            "assets": {"vehicles": [], "property": []},
            "digital_footprint": []
        }

        # Персональные данные
        console.print("[yellow]→ Персональные данные[/yellow]")
        target["personal"]["full_name"] = Prompt.ask("  Полное имя", default="").strip()
        if not target["personal"]["full_name"]:
            console.print("[red]✗ Полное имя обязательно![/red]")
            return None

        birth_date_input = Prompt.ask("  Дата рождения (YYYY-MM-DD)", default="").strip()
        if birth_date_input and not re.match(r'^\d{4}-\d{2}-\d{2}$', birth_date_input):
            console.print("[red]✗ Неверный формат даты рождения. Используйте YYYY-MM-DD.[/red]")
            return None
        if birth_date_input:
            target["personal"]["birth_date"] = birth_date_input

        target["personal"]["birth_place"] = Prompt.ask("  Место рождения", default="").strip()
        gender = Prompt.ask("  Пол (male/female/other)", default="male").strip().lower()
        if gender in ['male', 'female', 'other']:
            target["personal"]["gender"] = gender

        aliases = Prompt.ask("  Псевдонимы (через запятую)", default="").strip()
        if aliases:
            target["personal"]["aliases"] = [a.strip() for a in aliases.split(",") if a.strip()]

        # Контакты
        if Confirm.ask("\n[yellow]Добавить контакты?[/yellow]", default=True):
            console.print("[yellow]→ Контакты[/yellow]")
            phones = Prompt.ask("  Телефоны (через запятую)", default="").strip()
            if phones:
                target["contacts"]["phones"] = [p.strip() for p in phones.split(",") if p.strip()]
            emails = Prompt.ask("  Email-адреса (через запятую)", default="").strip()
            if emails:
                target["contacts"]["emails"] = [e.strip() for e in emails.split(",") if e.strip()]
            messengers_str = Prompt.ask("  Мессенджеры (telegram, whatsapp и т.д. - через запятую)", default="").strip()
            if messengers_str:
                messengers = {}
                for msgr in messengers_str.split(','):
                    msgr_clean = msgr.strip()
                    if msgr_clean:
                        messengers[msgr_clean] = Prompt.ask(f"    Логин для {msgr_clean}", default="").strip()
                if messengers:
                    target["contacts"]["messengers"] = messengers

        # Соцсети
        if Confirm.ask("\n[yellow]Добавить социальные сети?[/yellow]", default=True):
            console.print("[yellow]→ Социальные сети[/yellow]")
            while True:
                platform = Prompt.ask("  Платформа (vk/instagram/telegram/facebook/twitter и т.д.)", default="").strip()
                if not platform:
                    break
                social = {
                    "platform": platform,
                    "url": Prompt.ask("  URL профиля", default="").strip(),
                    "username": Prompt.ask("  Username", default="").strip(),
                    "followers": int(Prompt.ask("  Подписчики", default="0")),
                    "posts_count": int(Prompt.ask("  Количество постов", default="0"))
                }
                # Убедимся, что URL не пустой
                if not social['url']:
                    social['url'] = f"https://{platform}.com/{social['username']}" if social['username'] else "#"
                target["social_media"].append(social)
                if not Confirm.ask("  Добавить ещё соцсеть?", default=False):
                    break

        # Семья
        if Confirm.ask("\n[yellow]Добавить информацию о семье?[/yellow]", default=True):
            console.print("[yellow]→ Семья[/yellow]")
            while True:
                rel_name = Prompt.ask("  Имя члена семьи (или Enter для завершения)", default="").strip()
                if not rel_name:
                    break
                family_member = {
                    "full_name": rel_name,
                    "relation": Prompt.ask("  Родство (мать, отец, брат и т.д.)", default="").strip(),
                    "birth_date": Prompt.ask("  Дата рождения (YYYY-MM-DD)", default="").strip(),
                    "occupation": Prompt.ask("  Род занятий", default="").strip(),
                    "workplace": Prompt.ask("  Место работы", default="").strip(),
                    "notes": Prompt.ask("  Заметки", default="").strip()
                }
                target["family"].append(family_member)
                if not Confirm.ask("  Добавить ещё одного члена семьи?", default=False):
                    break

        # Образование
        if Confirm.ask("\n[yellow]Добавить информацию об образовании?[/yellow]", default=True):
            console.print("[yellow]→ Образование[/yellow]")
            while True:
                edu_institution = Prompt.ask("  Учебное заведение (или Enter для завершения)", default="").strip()
                if not edu_institution:
                    break
                education_entry = {
                    "type": Prompt.ask("  Тип (school/university/course)", default="school").strip(),
                    "institution": edu_institution,
                    "location": Prompt.ask("  Местоположение", default="").strip(),
                    "degree": Prompt.ask("  Степень/курс", default="").strip(),
                    "specialization": Prompt.ask("  Специализация", default="").strip(),
                    "start_date": Prompt.ask("  Начало (YYYY-MM-DD)", default="").strip(),
                    "end_date": Prompt.ask("  Окончание (YYYY-MM-DD)", default="").strip()
                }
                target["education"].append(education_entry)
                if not Confirm.ask("  Добавить ещё одно место обучения?", default=False):
                    break

        # Работа
        if Confirm.ask("\n[yellow]Добавить информацию о работе?[/yellow]", default=True):
            console.print("[yellow]→ Трудовая история[/yellow]")
            while True:
                company = Prompt.ask("  Компания (или Enter для завершения)", default="").strip()
                if not company:
                    break
                employment_entry = {
                    "company": company,
                    "position": Prompt.ask("  Должность", default="").strip(),
                    "location": Prompt.ask("  Местоположение", default="").strip(),
                    "start_date": Prompt.ask("  Начало (YYYY-MM-DD)", default="").strip(),
                    "end_date": Prompt.ask("  Окончание (YYYY-MM-DD или оставить пусто)", default="").strip(),
                    "description": Prompt.ask("  Описание роли", default="").strip()
                }
                target["employment"].append(employment_entry)
                if not Confirm.ask("  Добавить ещё одно место работы?", default=False):
                    break

        # Адреса
        if Confirm.ask("\n[yellow]Добавить адреса проживания?[/yellow]", default=True):
            console.print("[yellow]→ Адреса[/yellow]")
            while True:
                address = Prompt.ask("  Адрес (или Enter для завершения)", default="").strip()
                if not address:
                    break
                address_entry = {
                    "type": Prompt.ask("  Тип (residence/work/other)", default="residence").strip(),
                    "address": address,
                    "start_date": Prompt.ask("  Начало проживания (YYYY-MM-DD)", default="").strip(),
                    "end_date": Prompt.ask("  Конец проживания (YYYY-MM-DD или оставить пусто)", default="").strip(),
                    "coordinates": {
                        "lat": float(Prompt.ask("  Широта (или 0)", default="0")),
                        "lon": float(Prompt.ask("  Долгота (или 0)", default="0"))
                    },
                    "notes": Prompt.ask("  Заметки", default="").strip()
                }
                target["addresses"].append(address_entry)
                if not Confirm.ask("  Добавить ещё один адрес?", default=False):
                    break

        # Связи
        if Confirm.ask("\n[yellow]Добавить информацию о связях?[/yellow]", default=True):
            console.print("[yellow]→ Связи[/yellow]")
            while True:
                conn_name = Prompt.ask("  Имя человека (или Enter для завершения)", default="").strip()
                if not conn_name:
                    break
                connection = {
                    "name": conn_name,
                    "relation": Prompt.ask("  Тип отношения (colleague/friend/family/etc)", default="").strip(),
                    "context": Prompt.ask("  Контекст связи", default="").strip(),
                    "source": Prompt.ask("  Источник (LinkedIn/VK/etc)", default="").strip(),
                    "strength": int(Prompt.ask("  Сила связи (1-10)", default="5"))
                }
                target["connections"].append(connection)
                if not Confirm.ask("  Добавить ещё одну связь?", default=False):
                    break

        # Теги
        tags = Prompt.ask("\n[yellow]Теги (через запятую)[/yellow]", default="").strip()
        if tags:
            target["tags"] = [t.strip() for t in tags.split(",") if t.strip()]

        # Заметки
        notes = Prompt.ask("[yellow]Заметки[/yellow]", default="").strip()
        if notes:
            target["notes"] = notes

        # Сохранение
        try:
            target_id = self.dm.create_target(target)
            console.print(f"\n[bold green]✓ Цель создана![/bold green] [dim]ID: {target_id}[/dim]\n")
            return target_id
        except Exception as e:
            console.print(f"\n[bold red]✗ Ошибка при создании цели:[/bold red] {e}\n")
            return None

    def edit_target(self):
        """Редактирование существующей цели"""
        self.list_targets()
        target_id = Prompt.ask("\n[cyan]Введите ID цели для редактирования[/cyan]").strip()
        if not target_id:
            console.print("[red]✗ ID цели не может быть пустым.[/red]\n")
            return

        target = self.dm.get_target(target_id)
        if not target:
            console.print(f"\n[bold red]✗ Цель с ID {target_id} не найдена[/bold red]\n")
            return

        console.print(f"\n[bold cyan]Редактирование цели: {target.get('personal', {}).get('full_name', 'N/A')}[/bold cyan]\n")
        
        # Простое редактирование: обновляем заметки
        new_notes = Prompt.ask("[yellow]Новые заметки (или Enter для пропуска)[/yellow]", default="").strip()
        if new_notes:
            target["notes"] = new_notes

        # Добавляем теги
        new_tags = Prompt.ask("[yellow]Добавить теги (через запятую, или Enter для пропуска)[/yellow]", default="").strip()
        if new_tags:
            new_tags_list = [t.strip() for t in new_tags.split(",") if t.strip()]
            target["tags"] = list(set((target.get("tags", []) + new_tags_list)))

        try:
            self.dm.update_target(target_id, target)
            console.print(f"\n[bold green]✓ Цель обновлена![/bold green]\n")
        except Exception as e:
            console.print(f"\n[bold red]✗ Ошибка при обновлении:[/bold red] {e}\n")

    def list_targets(self):
        """Показывает список целей"""
        targets = self.dm.get_all_targets()
        if not targets:
            console.print("\n[yellow]Нет целей в базе данных[/yellow]\n")
            return

        table = Table(title="[bold cyan]Список целей[/bold cyan]", box=box.ROUNDED, border_style="cyan")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Имя", style="white")
        table.add_column("Дата рождения", style="dim")
        table.add_column("Теги", style="yellow")
        table.add_column("Обновлено", style="dim")

        for target in targets:
            target_id = target['id']
            name = target.get('personal', {}).get('full_name', 'N/A')
            birth = target.get('personal', {}).get('birth_date', 'N/A')
            tags = ", ".join(target.get('tags', [])[:3])
            if len(target.get('tags', [])) > 3:
                tags += "..."
            updated = target.get('updated_at', 'N/A')
            try:
                updated_dt = datetime.fromisoformat(updated.replace('Z', '+00:00'))
                updated = updated_dt.strftime('%Y-%m-%d %H:%M')
            except (ValueError, TypeError):
                pass

            table.add_row(target_id, name, birth, tags, updated)

        console.print("\n", table, "\n")

    def generate_report_for_target(self):
        """Генерирует отчёт для выбранной цели"""
        self.list_targets()
        target_id = Prompt.ask("\n[cyan]Введите ID цели[/cyan]").strip()
        if not target_id:
            console.print("[red]✗ ID цели не может быть пустым.[/red]\n")
            return

        try:
            console.print(f"\n[yellow]⏳ Генерация отчёта...[/yellow]")
            output_path = self.generator.generate_report(target_id)
            console.print(f"\n[bold green]✓ Отчёт успешно создан![/bold green]")
            console.print(f"[cyan]→ Путь:[/cyan] {output_path}\n")
        except Exception as e:
            console.print(f"\n[bold red]✗ Ошибка:[/bold red] {e}\n")

    def generate_all_reports(self):
        """Генерирует отчёты для всех целей"""
        if not Confirm.ask("\n[yellow]Генерировать отчёты для всех целей?[/yellow]", default=True):
            return

        console.print("\n[yellow]⏳ Генерация отчётов...\n[/yellow]")
        try:
            paths = self.generator.generate_all_reports()
            if paths:
                console.print(f"\n[bold green]✓ Создано отчётов: {len(paths)}[/bold green]\n")
            else:
                console.print("\n[yellow]Нет целей для генерации[/yellow]\n")
        except Exception as e:
            console.print(f"\n[bold red]✗ Ошибка при генерации:[/bold red] {e}\n")

    def delete_target(self):
        """Удаляет цель"""
        self.list_targets()
        target_id = Prompt.ask("\n[cyan]Введите ID цели для удаления[/cyan]").strip()
        if not target_id:
            console.print("[red]✗ ID цели не может быть пустым.[/red]\n")
            return

        target = self.dm.get_target(target_id)
        if not target:
            console.print(f"\n[bold red]✗ Цель не найдена[/bold red]\n")
            return

        name = target.get('personal', {}).get('full_name', 'N/A')
        if Confirm.ask(f"\n[red]Удалить цель '{name}' ({target_id})?[/red]", default=False):
            try:
                if self.dm.delete_target(target_id):
                    console.print(f"\n[bold green]✓ Цель удалена[/bold green]\n")
                else:
                    console.print(f"\n[bold red]✗ Ошибка при удалении[/bold red]\n")
            except Exception as e:
                console.print(f"\n[bold red]✗ Ошибка при удалении:[/bold red] {e}\n")

    def search_targets(self):
        """Поиск целей"""
        query = Prompt.ask("\n[cyan]Поисковый запрос[/cyan]").strip()
        if not query:
            console.print("[red]✗ Запрос не может быть пустым.[/red]\n")
            return

        results = self.dm.search_targets(query)
        if not results:
            console.print(f"\n[yellow]По запросу '{query}' ничего не найдено[/yellow]\n")
            return

        console.print(f"\n[green]✓ Найдено результатов: {len(results)}[/green]\n")
        for target in results:
            name = target.get('personal', {}).get('full_name', 'N/A')
            target_id = target['id']
            console.print(f"  [cyan]→[/cyan] {name} [dim]({target_id})[/dim]")
        console.print()

    def show_statistics(self):
        """Показывает статистику базы данных"""
        try:
            stats = self.dm.get_statistics()
            console.print("\n[bold cyan]📊 Статистика базы данных[/bold cyan]\n")
            stats_table = Table(box=box.ROUNDED, border_style="cyan")
            stats_table.add_column("Метрика", style="cyan")
            stats_table.add_column("Значение", justify="right")

            stats_table.add_row("Всего целей", str(stats.get('total_targets', 0)))
            stats_table.add_row("Всего связей", str(stats.get('total_connections', 0)))
            stats_table.add_row("Всего адресов", str(stats.get('total_addresses', 0)))
            stats_table.add_row("Среднее кол-во соцсетей на цель", f"{stats.get('avg_social_accounts', 0):.2f}")
            stats_table.add_row("Последняя созданная цель", stats.get('newest_target', 'N/A'))
            stats_table.add_row("Последняя обновлённая цель", stats.get('last_updated', 'N/A'))

            console.print(stats_table)

            if stats.get('most_common_tags'):
                console.print("\n[bold yellow]🏷️  Часто используемые теги:[/bold yellow]\n")
                tags_table = Table(box=box.ROUNDED, border_style="yellow")
                tags_table.add_column("Тег", style="yellow")
                tags_table.add_column("Частота", justify="right")
                for tag, count in stats['most_common_tags'][:10]:
                    tags_table.add_row(tag, str(count))
                console.print(tags_table)
            
            console.print()
        except Exception as e:
            console.print(f"\n[bold red]✗ Ошибка при получении статистики:[/bold red] {e}\n")

    def export_import_menu(self):
        """Меню экспорта/импорта"""
        console.print("\n[bold cyan]╔═══ Экспорт/Импорт ═══╗[/bold cyan]\n")
        
        table = Table(show_header=False, box=box.ROUNDED, border_style="cyan")
        table.add_row("[1]", "[cyan]Экспортировать всё в JSON[/cyan]")
        table.add_row("[2]", "[cyan]Экспортировать цель в JSON[/cyan]")
        table.add_row("[3]", "[cyan]Импортировать из JSON[/cyan]")
        table.add_row("[0]", "[yellow]Назад[/yellow]")
        
        console.print(Panel(table, title="[bold cyan]Опции[/bold cyan]", border_style="cyan"))
        
        choice = Prompt.ask("[bold cyan]Выберите действие[/bold cyan]", choices=["0", "1", "2", "3"])
        
        if choice == "0":
            return
        elif choice == "1":
            self._export_all_json()
        elif choice == "2":
            self._export_target_json()
        elif choice == "3":
            self._import_from_json()

    def _export_all_json(self):
        """Экспортирует все цели в JSON"""
        try:
            targets = self.dm.get_all_targets()
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"osint_export_{timestamp}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({"targets": targets}, f, indent=2, ensure_ascii=False)
            
            console.print(f"\n[bold green]✓ Экспорт завершён![/bold green] [dim]Файл: {filename}[/dim]\n")
        except Exception as e:
            console.print(f"\n[bold red]✗ Ошибка при экспорте:[/bold red] {e}\n")

    def _export_target_json(self):
        """Экспортирует одну цель в JSON"""
        self.list_targets()
        target_id = Prompt.ask("\n[cyan]Введите ID цели для экспорта[/cyan]").strip()
        if not target_id:
            console.print("[red]✗ ID цели не может быть пустым.[/red]\n")
            return
        
        try:
            target = self.dm.get_target(target_id)
            if not target:
                console.print(f"\n[bold red]✗ Цель не найдена[/bold red]\n")
                return
            
            name = target.get('personal', {}).get('full_name', target_id)
            safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).strip()
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{safe_name}_{timestamp}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(target, f, indent=2, ensure_ascii=False)
            
            console.print(f"\n[bold green]✓ Экспорт завершён![/bold green] [dim]Файл: {filename}[/dim]\n")
        except Exception as e:
            console.print(f"\n[bold red]✗ Ошибка при экспорте:[/bold red] {e}\n")

    def _import_from_json(self):
        """Импортирует цель из JSON файла"""
        filename = Prompt.ask("\n[cyan]Введите имя JSON файла[/cyan]").strip()
        if not filename:
            console.print("[red]✗ Имя файла не может быть пустым.[/red]\n")
            return
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Проверяем формат
            if "targets" in data:
                # Это экспорт всех целей
                for target in data["targets"]:
                    self.dm.create_target(target)
                console.print(f"\n[bold green]✓ Импортировано целей: {len(data['targets'])}[/bold green]\n")
            else:
                # Это одна цель
                self.dm.create_target(data)
                console.print(f"\n[bold green]✓ Цель импортирована![/bold green]\n")
        except FileNotFoundError:
            console.print(f"\n[bold red]✗ Файл '{filename}' не найден[/bold red]\n")
        except json.JSONDecodeError:
            console.print(f"\n[bold red]✗ Ошибка при чтении JSON[/bold red]\n")
        except Exception as e:
            console.print(f"\n[bold red]✗ Ошибка при импорте:[/bold red] {e}\n")

    def run(self):
        """Главный цикл приложения"""
        self.show_banner()
        while True:
            self.show_main_menu()
            choice = Prompt.ask("\n[bold cyan]Выберите действие[/bold cyan]", 
                               choices=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"])

            if choice == "0":
                console.print("\n[cyan]До свидания! 👋[/cyan]\n")
                break
            elif choice == "1":
                self.create_target_wizard()
            elif choice == "2":
                self.list_targets()
            elif choice == "3":
                self.edit_target()
            elif choice == "4":
                self.generate_report_for_target()
            elif choice == "5":
                self.generate_all_reports()
            elif choice == "6":
                self.delete_target()
            elif choice == "7":
                self.search_targets()
            elif choice == "8":
                self.show_statistics()
            elif choice == "9":
                self.export_import_menu()


def main():
    """Точка входа в приложение"""
    try:
        cli = OSINTProfilerCLI()
        cli.run()
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️  Прервано пользователем[/yellow]\n")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[bold red]💥 Критическая ошибка:[/bold red] {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
