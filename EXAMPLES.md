# 📚 OSINT Profiler - Code Examples

Коллекция примеров использования API для различных задач.

---

## 🎯 Базовые операции

### Создание простого профиля

```python
from core.data_manager import DataManager

dm = DataManager()

# Минимальный профиль
simple_target = {
    "personal": {
        "full_name": "Иван Иванов",
        "birth_date": "1990-05-15"
    },
    "tags": ["test"],
    "notes": "Тестовый профиль"
}

target_id = dm.create_target(simple_target)
print(f"✓ Создан профиль: {target_id}")
```

### Получение и обновление

```python
# Получить профиль
target = dm.get_target(target_id)
print(f"Имя: {target['personal']['full_name']}")

# Обновить данные
dm.update_target(target_id, {
    "notes": "Обновлённая информация",
    "tags": ["test", "updated"]
})
```

---

## 👨‍👩‍👧 Работа с семьёй

### Добавление родственников

```python
family_data = {
    "personal": {
        "full_name": "Пётр Петров"
    },
    "family": [
        {
            "relation": "mother",
            "full_name": "Петрова Мария Ивановна",
            "birth_year": 1965,
            "occupation": "Врач",
            "workplace": "Городская больница №3",
            "notes": "Кардиолог, стаж 30+ лет"
        },
        {
            "relation": "father",
            "full_name": "Петров Иван Сергеевич",
            "birth_year": 1963,
            "occupation": "Инженер",
            "workplace": "Машиностроительный завод"
        },
        {
            "relation": "sister",
            "full_name": "Петрова Анна",
            "birth_year": 1995,
            "occupation": "Учитель"
        }
    ]
}

target_id = dm.create_target(family_data)
```

---

## 🌐 Социальные сети

### Добавление соцсетей

```python
social_target = {
    "personal": {
        "full_name": "Алексей Смирнов"
    },
    "social_media": [
        {
            "platform": "vk",
            "url": "https://vk.com/alexey_smirnov",
            "username": "alexey_smirnov",
            "followers": 1523,
            "posts_count": 342
        },
        {
            "platform": "instagram",
            "url": "https://instagram.com/alex.smirnov",
            "username": "alex.smirnov",
            "followers": 3240,
            "posts_count": 189
        },
        {
            "platform": "telegram",
            "url": "https://t.me/alexey_sm",
            "username": "@alexey_sm",
            "followers": 0,  # для Telegram
            "posts_count": 0
        },
        {
            "platform": "github",
            "url": "https://github.com/alex-dev",
            "username": "alex-dev",
            "followers": 234,
            "posts_count": 67  # репозитории
        }
    ]
}
```

---

## 🎓 Образование и карьера

### Полный трек образования

```python
education_target = {
    "personal": {
        "full_name": "Дмитрий Кузнецов"
    },
    "education": [
        {
            "type": "school",
            "institution": "Гимназия №1",
            "location": "Москва",
            "start_date": "2000-09-01",
            "end_date": "2011-06-30",
            "degree": "Среднее образование"
        },
        {
            "type": "university",
            "institution": "МГУ им. М.В. Ломоносова",
            "location": "Москва",
            "faculty": "Факультет вычислительной математики",
            "specialization": "Прикладная математика",
            "start_date": "2011-09-01",
            "end_date": "2015-06-30",
            "degree": "Бакалавр"
        },
        {
            "type": "university",
            "institution": "МГУ им. М.В. Ломоносова",
            "location": "Москва",
            "faculty": "Факультет вычислительной математики",
            "specialization": "Машинное обучение",
            "start_date": "2015-09-01",
            "end_date": "2017-06-30",
            "degree": "Магистр"
        },
        {
            "type": "course",
            "institution": "Coursera",
            "location": "Online",
            "specialization": "Deep Learning Specialization",
            "start_date": "2018-03-01",
            "end_date": "2018-08-31",
            "degree": "Сертификат"
        }
    ]
}
```

### История работы

```python
employment_target = {
    "personal": {
        "full_name": "Сергей Волков"
    },
    "employment": [
        {
            "company": "Стартап XYZ",
            "position": "Junior Developer",
            "location": "Санкт-Петербург",
            "start_date": "2015-07-01",
            "end_date": "2017-03-31",
            "description": "Разработка веб-приложений на Python/Django"
        },
        {
            "company": "Яндекс",
            "position": "Middle Python Developer",
            "location": "Москва",
            "start_date": "2017-04-01",
            "end_date": "2020-12-31",
            "description": "Разработка поисковых сервисов"
        },
        {
            "company": "VK",
            "position": "Senior Backend Developer",
            "location": "Санкт-Петербург",
            "start_date": "2021-01-15",
            "end_date": None,  # текущее место работы
            "description": "Руководство командой backend-разработки"
        }
    ]
}
```

---

## 🗺️ Адреса и геолокация

### Адреса с координатами

```python
addresses_target = {
    "personal": {
        "full_name": "Мария Соколова"
    },
    "addresses": [
        {
            "type": "residence",
            "address": "Москва, ул. Арбат 10, кв. 5",
            "start_date": "1995-03-20",
            "end_date": "2015-08-01",
            "coordinates": {
                "lat": 55.7506,
                "lon": 37.5917
            },
            "notes": "Родительский дом"
        },
        {
            "type": "residence",
            "address": "Санкт-Петербург, Невский пр. 100, кв. 42",
            "start_date": "2015-08-01",
            "end_date": None,
            "coordinates": {
                "lat": 59.9343,
                "lon": 30.3351
            },
            "notes": "Текущее место жительства"
        },
        {
            "type": "work",
            "address": "Санкт-Петербург, Лиговский пр. 266",
            "start_date": "2020-01-15",
            "end_date": None,
            "coordinates": {
                "lat": 59.8833,
                "lon": 30.3481
            },
            "notes": "Офис компании"
        },
        {
            "type": "education",
            "address": "СПбГУ, Университетская наб. 7/9",
            "start_date": "2013-09-01",
            "end_date": "2018-06-30",
            "coordinates": {
                "lat": 59.9410,
                "lon": 30.2961
            }
        }
    ]
}
```

---

## 🕸️ Граф связей

### Создание сети связей

```python
connections_target = {
    "personal": {
        "full_name": "Андрей Новиков"
    },
    "connections": [
        {
            "name": "Иванов Иван",
            "relation": "colleague",
            "context": "Работали вместе в компании X (2015-2018)",
            "source": "LinkedIn",
            "strength": 7  # от 1 до 10
        },
        {
            "name": "Петрова Ольга",
            "relation": "friend",
            "context": "Учились в университете, поддерживают связь",
            "source": "VK",
            "strength": 9
        },
        {
            "name": "Сидоров Максим",
            "relation": "family",
            "context": "Двоюродный брат",
            "source": "Personal",
            "strength": 10
        },
        {
            "name": "Кузнецова Анна",
            "relation": "partner",
            "context": "Деловой партнёр, совместный проект",
            "source": "LinkedIn",
            "strength": 8
        },
        {
            "name": "Волков Дмитрий",
            "relation": "colleague",
            "context": "Текущий коллега, работают в одной команде",
            "source": "LinkedIn",
            "strength": 6
        }
    ]
}
```

---

## ⏱️ Таймлайн событий

### Хронология жизни

```python
timeline_target = {
    "personal": {
        "full_name": "Елена Морозова"
    },
    "timeline": [
        {
            "date": "1992-08-15",
            "event": "Рождение",
            "location": "Москва",
            "category": "personal"
        },
        {
            "date": "2009-09-01",
            "event": "Поступление в МГУ",
            "location": "Москва",
            "category": "education"
        },
        {
            "date": "2013-06-30",
            "event": "Получение диплома бакалавра",
            "location": "Москва",
            "category": "education"
        },
        {
            "date": "2013-09-15",
            "event": "Начало работы в Яндексе",
            "location": "Москва",
            "category": "employment"
        },
        {
            "date": "2015-05-01",
            "event": "Переезд в Санкт-Петербург",
            "location": "Санкт-Петербург",
            "category": "relocation"
        },
        {
            "date": "2017-10-20",
            "event": "Повышение до Senior Developer",
            "location": "Санкт-Петербург",
            "category": "employment"
        },
        {
            "date": "2020-03-01",
            "event": "Запуск собственного стартапа",
            "location": "Санкт-Петербург",
            "category": "business"
        }
    ]
}

# События автоматически сортируются по дате
target_id = dm.create_target(timeline_target)
```

---

## 🔍 Поиск и фильтрация

### Поиск по разным критериям

```python
# Поиск по имени
results = dm.search_targets("Иванов")

# Поиск по тегу
results = dm.search_targets("developer")

# Поиск по заметкам
results = dm.search_targets("программист")

for target in results:
    name = target['personal']['full_name']
    target_id = target['id']
    print(f"Найдено: {name} ({target_id})")
```

### Получение всех целей

```python
all_targets = dm.get_all_targets()

print(f"Всего профилей: {len(all_targets)}")

for target in all_targets:
    print(f"- {target['personal']['full_name']}")
```

---

## 📊 Генерация отчётов

### Генерация одного отчёта

```python
from generator import ReportGenerator

gen = ReportGenerator()

# Генерация отчёта
output_path = gen.generate_report("target_abc123")
print(f"Отчёт сохранён: {output_path}")

# С кастомным именем файла
output_path = gen.generate_report(
    "target_abc123",
    output_filename="special_report.html"
)
```

### Генерация всех отчётов

```python
# Генерируем отчёты для всех профилей
paths = gen.generate_all_reports()

print(f"Создано отчётов: {len(paths)}")
for path in paths:
    print(f"  → {path}")
```

### Предпросмотр без сохранения

```python
# Получить HTML-код отчёта
html_content = gen.preview_report("target_abc123")

# Можно использовать для отправки по email, например
print(html_content[:100])  # первые 100 символов
```

---

## 🔄 Обновление данных

### Добавление события в таймлайн

```python
# Добавляем событие к существующей цели
success = dm.add_timeline_event("target_abc123", {
    "date": "2024-01-15",
    "event": "Запуск нового проекта",
    "location": "Москва",
    "category": "business"
})

if success:
    print("✓ Событие добавлено")
```

### Добавление связи

```python
# Добавляем новую связь
success = dm.add_connection("target_abc123", {
    "name": "Новиков Сергей",
    "relation": "colleague",
    "context": "Новый коллега в команде",
    "source": "LinkedIn",
    "strength": 5
})

if success:
    print("✓ Связь добавлена")
```

---

## 🎨 Полный профиль с всеми данными

```python
complete_target = {
    "personal": {
        "full_name": "Анна Волкова",
        "birth_date": "1990-03-25",
        "birth_place": "Екатеринбург, Россия",
        "gender": "female",
        "aliases": ["anna_v", "volkova90"],
        "photo_url": "https://example.com/photo.jpg"
    },
    "contacts": {
        "phones": ["+7-900-111-22-33"],
        "emails": ["anna@example.com"],
        "messengers": {
            "telegram": "@anna_v",
            "whatsapp": "+7-900-111-22-33"
        }
    },
    "social_media": [
        {
            "platform": "vk",
            "url": "https://vk.com/anna_v",
            "username": "anna_v",
            "followers": 450,
            "posts_count": 120
        }
    ],
    "family": [
        {
            "relation": "mother",
            "full_name": "Волкова Елена",
            "birth_year": 1965,
            "occupation": "Учитель"
        }
    ],
    "education": [
        {
            "type": "university",
            "institution": "УрФУ",
            "location": "Екатеринбург",
            "faculty": "Математика",
            "start_date": "2007-09-01",
            "end_date": "2012-06-30",
            "degree": "Специалист"
        }
    ],
    "employment": [
        {
            "company": "IT Company",
            "position": "Data Analyst",
            "location": "Екатеринбург",
            "start_date": "2012-08-01",
            "end_date": None,
            "description": "Анализ данных"
        }
    ],
    "addresses": [
        {
            "type": "residence",
            "address": "Екатеринбург, ул. Ленина 10",
            "start_date": "1990-03-25",
            "end_date": None,
            "coordinates": {
                "lat": 56.8389,
                "lon": 60.6057
            }
        }
    ],
    "connections": [
        {
            "name": "Иванов Петр",
            "relation": "colleague",
            "context": "Коллега по работе",
            "source": "LinkedIn",
            "strength": 7
        }
    ],
    "timeline": [
        {
            "date": "1990-03-25",
            "event": "Рождение",
            "location": "Екатеринбург",
            "category": "personal"
        }
    ],
    "assets": {
        "vehicles": [
            {
                "type": "car",
                "brand": "Toyota",
                "model": "Corolla",
                "year": 2018,
                "plate_number": "А123БВ66",
                "color": "белый"
            }
        ],
        "property": []
    },
    "notes": "Профессиональный аналитик данных",
    "tags": ["IT", "analyst", "Ekaterinburg"]
}

target_id = dm.create_target(complete_target)
print(f"✓ Полный профиль создан: {target_id}")
```

---

## 🔧 Продвинутые техники

### Массовый импорт из списка

```python
people_list = [
    {"full_name": "Иван Иванов", "tags": ["test"]},
    {"full_name": "Пётр Петров", "tags": ["test"]},
    {"full_name": "Сидор Сидоров", "tags": ["test"]}
]

for person in people_list:
    target = {
        "personal": person,
        "tags": person["tags"]
    }
    target_id = dm.create_target(target)
    print(f"✓ Создан: {person['full_name']} ({target_id})")
```

### Экспорт всех данных

```python
import json

all_data = dm.get_all_targets()

with open('export.json', 'w', encoding='utf-8') as f:
    json.dump(all_data, f, ensure_ascii=False, indent=2)

print("✓ Данные экспортированы в export.json")
```

---

**💡 Tip:** Комбинируйте эти примеры для создания полноценных OSINT-профилей!