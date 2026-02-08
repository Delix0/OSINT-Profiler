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

console = Console()

class OSINTProfilerCLI:
    """CLI-интерфейс для OSINT Profiler"""
    
    def __init__(self):
        self.dm = DataManager()
        self.generator = ReportGenerator()
    
    def show_banner(self):
        """Показывает баннер приложения"""
        banner = """
╔════════════════════════════════════════════════╗
║   ░█████╗░░██████╗██╗███╗░░██╗████████╗        ║
║   ██╔══██╗██╔════╝██║████╗░██║╚══██╔══╝        ║
║   ██║░░██║╚█████╗░██║██╔██╗██║░░░██║░░░        ║
║   ██║░░██║░╚═══██╗██║██║╚████║░░░██║░░░        ║
║   ╚█████╔╝██████╔╝██║██║░╚███║░░░██║░░░        ║
║   ░╚════╝░╚═════╝░╚═╝╚═╝░░╚══╝░░░╚═╝░░░        ║
║                                                ║
║         P R O F I L E R   v1.0                 ║
║    Intelligence Gathering & Reporting Tool     ║
║         Telegram: @Delix0_tgk                  ║
╚════════════════════════════════════════════════╝
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
            "notes": ""
        }
        
        # Персональные данные
        console.print("[yellow]→ Персональные данные[/yellow]")
        target["personal"]["full_name"] = Prompt.ask("  Полное имя", default="")
        target["personal"]["birth_date"] = Prompt.ask("  Дата рождения (YYYY-MM-DD)", default="")
        target["personal"]["birth_place"] = Prompt.ask("  Место рождения", default="")
        target["personal"]["gender"] = Prompt.ask("  Пол (male/female)", default="male")
        
        aliases = Prompt.ask("  Псевдонимы (через запятую)", default="")
        if aliases:
            target["personal"]["aliases"] = [a.strip() for a in aliases.split(",")]
        
        # Контакты
        if Confirm.ask("\n[yellow]Добавить контакты?[/yellow]", default=True):
            console.print("[yellow]→ Контакты[/yellow]")
            
            phones = Prompt.ask("  Телефоны (через запятую)", default="")
            if phones:
                target["contacts"]["phones"] = [p.strip() for p in phones.split(",")]
            
            emails = Prompt.ask("  Email-адреса (через запятую)", default="")
            if emails:
                target["contacts"]["emails"] = [e.strip() for e in emails.split(",")]
        
        # Соцсети
        if Confirm.ask("\n[yellow]Добавить социальные сети?[/yellow]", default=True):
            console.print("[yellow]→ Социальные сети[/yellow]")
            
            while True:
                platform = Prompt.ask("  Платформа (vk/instagram/telegram/facebook)", default="")
                if not platform:
                    break
                
                social = {
                    "platform": platform,
                    "url": Prompt.ask("  URL профиля", default=""),
                    "username": Prompt.ask("  Username", default=""),
                    "followers": int(Prompt.ask("  Подписчики", default="0")),
                    "posts_count": int(Prompt.ask("  Количество постов", default="0"))
                }
                target["social_media"].append(social)
                
                if not Confirm.ask("  Добавить ещё соцсеть?", default=False):
                    break
        
        # Теги
        console.print("\n[yellow]→ Дополнительно[/yellow]")
        tags = Prompt.ask("  Теги (через запятую)", default="")
        if tags:
            target["tags"] = [t.strip() for t in tags.split(",")]
        
        target["notes"] = Prompt.ask("  Заметки", default="")
        
        # Сохраняем
        try:
            target_id = self.dm.create_target(target)
            console.print(f"\n[bold green]✓ Цель успешно создана![/bold green]")
            console.print(f"[dim]ID: {target_id}[/dim]\n")
            return target_id
        except Exception as e:
            console.print(f"\n[bold red]✗ Ошибка при создании цели:[/bold red] {e}\n")
            return None
    
    def list_targets(self):
        """Показывает список всех целей"""
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
            except:
                pass
            
            table.add_row(target_id, name, birth, tags, updated)
        
        console.print("\n", table, "\n")
    
    def generate_report_for_target(self):
        """Генерирует отчёт для выбранной цели"""
        self.list_targets()
        
        target_id = Prompt.ask("\n[cyan]Введите ID цели[/cyan]")
        
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
        
        console.print("\n[yellow]⏳ Генерация отчётов...[/yellow]\n")
        
        paths = self.generator.generate_all_reports()
        
        if paths:
            console.print(f"\n[bold green]✓ Создано отчётов: {len(paths)}[/bold green]\n")
        else:
            console.print("\n[yellow]Нет целей для генерации[/yellow]\n")
    
    def delete_target(self):
        """Удаляет цель"""
        self.list_targets()
        
        target_id = Prompt.ask("\n[cyan]Введите ID цели для удаления[/cyan]")
        
        target = self.dm.get_target(target_id)
        if not target:
            console.print(f"\n[bold red]✗ Цель не найдена[/bold red]\n")
            return
        
        name = target.get('personal', {}).get('full_name', 'N/A')
        
        if Confirm.ask(f"\n[red]Удалить цель '{name}' ({target_id})?[/red]", default=False):
            if self.dm.delete_target(target_id):
                console.print(f"\n[bold green]✓ Цель удалена[/bold green]\n")
            else:
                console.print(f"\n[bold red]✗ Ошибка при удалении[/bold red]\n")
    
    def search_targets(self):
        """Поиск целей"""
        query = Prompt.ask("\n[cyan]Поисковый запрос[/cyan]")
        
        results = self.dm.search_targets(query)
        
        if not results:
            console.print(f"\n[yellow]По запросу '{query}' ничего не найдено[/yellow]\n")
            return
        
        console.print(f"\n[green]Найдено результатов: {len(results)}[/green]\n")
        
        for target in results:
            name = target.get('personal', {}).get('full_name', 'N/A')
            target_id = target['id']
            console.print(f"  [cyan]→[/cyan] {name} [dim]({target_id})[/dim]")
        
        console.print()
    
    def run(self):
        """Главный цикл приложения"""
        self.show_banner()
        
        while True:
            self.show_main_menu()
            
            choice = Prompt.ask("\n[bold cyan]Выберите действие[/bold cyan]", choices=["0", "1", "2", "3", "4", "5", "6", "7"])
            
            if choice == "0":
                console.print("\n[cyan]До свидания! 👋[/cyan]\n")
                break
            elif choice == "1":
                self.create_target_wizard()
            elif choice == "2":
                self.list_targets()
            elif choice == "3":
                console.print("\n[yellow]Функция в разработке[/yellow]\n")
            elif choice == "4":
                self.generate_report_for_target()
            elif choice == "5":
                self.generate_all_reports()
            elif choice == "6":
                self.delete_target()
            elif choice == "7":
                self.search_targets()


def main():
    """Точка входа в приложение"""
    try:
        cli = OSINTProfilerCLI()
        cli.run()
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Прервано пользователем[/yellow]\n")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[bold red]Критическая ошибка:[/bold red] {e}\n")
        sys.exit(1)


if __name__ == "__main__":

    main()
