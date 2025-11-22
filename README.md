<p align="center">
  <img src="https://img.icons8.com/external-flaticons-lineal-color-flat-icons/120/000000/external-habit-fitness-flaticons-lineal-color-flat-icons.png" width="120" />
</p>

<h1 align="center">🌿 Habit Tracker</h1>

<p align="center">
  Геймифицированный трекер привычек c XP, уровнями, достижениями и лидербордом.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Django-4.2-092E20?logo=django&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3.11-blue?logo=python" />
  <img src="https://img.shields.io/badge/PostgreSQL-14-336791?logo=postgresql&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" />
  <img src="https://img.shields.io/badge/PRs-Welcome-brightgreen.svg" />
</p>

---

## ⭐ Возможности

✔ Создание привычек  
✔ Выполнение привычек (+XP)  
✔ Уровни (логарифмический рост)  
✔ Достижения и стрики  
✔ Профиль с прогресс-баром  
✔ Публичные профили  
✔ Лидерборд  
✔ AJAX-обновление XP  

---

## 🧱 Стек технологий

| Компонент        | Технология |
|------------------|------------|
| Backend          | Django 4.2 |
| ORM              | Django ORM |
| БД               | PostgreSQL |
| Frontend         | HTML / CSS / JS |
| Auth             | Django Auth |
| Signals          | Django Signals |
| API-интеракции   | AJAX |

---

## 🚀 Запуск проекта

### 🔧 Локально
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### 🐳 Docker
```bash
docker-compose up --build
```

---

## 📂 Структура проекта

```
habit_tracker/
│
├── habit_tracker/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── habits/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── utils.py
│   ├── templates/
│   │   ├── habits/
│   │   └── auth/
│   └── signals.py
│
├── static/
├── templates/
├── manage.py
└── requirements.txt
```

---

## 🛠 Команды управления

### Миграции
```bash
python manage.py makemigrations
python manage.py migrate
```

### Суперпользователь
```bash
python manage.py createsuperuser
```

### Запуск
```bash
python manage.py runserver
```

---

## 🗄 Работа с базой данных

### Создать привычку
```python
Habit.objects.create(
    name="Чтение",
    description="30 минут книги",
    xp_reward=15,
    user=user
)
```

### Получить XP
```python
from habits.utils import get_total_xp
get_total_xp(user)
```

### Уровень и прогресс
```python
from habits.utils import get_level_info
get_level_info(total_xp)
```

---

## 🔧 Администрирование

- Панель администратора: `/admin`
- Управление:
  - Пользователями  
  - Привычками  
  - Логами  
  - Наградами  
  - Профилями  

---

## 🔐 Безопасность

- CSRF защита  
- Django PBKDF2 пароли  
- Ограничение доступа к привычкам владельцем  
- `login_required`  
- Unique constraints (HabitLog: habit + date)  

---

## 📄 Лицензия
```
MIT License
Свободное использование, модификация и распространение разрешены.
```

---

## 🤝 Вклад в проект

1. Форк репозитория  
2. Новая ветка  
```bash
git checkout -b feature/my-feature
```
3. Коммит  
4. Pull Request  

---

<p align="center">✨ Спасибо за использование Habit Tracker!</p>
