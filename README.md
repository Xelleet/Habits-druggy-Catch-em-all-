# 🌿 Habit Tracker

Геймифицированный трекер привычек с системой опыта (XP), уровнями, наградами, статистикой и лидербордом.

---

## ✨ Возможности
- 🔐 Регистрация и авторизация  
- 📌 Создание, выполнение и удаление привычек  
- ⭐ Система наград (стрики, XP, разнообразие)  
- 📊 Прогресс-бар, уровень, общий XP  
- 🌐 Публичные профили  
- 🏆 Лидерборд  
- ⚡ AJAX-обновление уровня и XP  
- 🧮 Логарифмическая формула роста уровня  

---

## 🧱 Стек технологий
- **Backend:** Django 4.2  
- **Database:** PostgreSQL  
- **Frontend:** HTML / CSS / JavaScript  
- **ORM:** Django ORM  
- **Auth:** Django Authentication  
- **Инфраструктура:** Docker (при необходимости)

---

## 🚀 Запуск проекта

### 📍 Локально
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### 📦 Docker
```bash
docker-compose build
docker-compose up
```

---

## 📂 Структура проекта
```
habit_tracker/
│
├── habit_tracker/        # основные настройки проекта
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── habits/               # приложение привычек
│   ├── models.py         # модели Habit, HabitLog, Badge, Profile
│   ├── views.py          # логика XP, уровней, лидерборда, CRUD
│   ├── forms.py
│   ├── utils.py          # расчёт XP, уровней, прогресса
│   ├── templates/
│       ├── habits/
│       └── auth/
│
├── static/               # CSS, JS, изображения
├── manage.py
└── requirements.txt
```

---

## 🛠 Команды управления

### 💾 Миграции
```bash
python manage.py makemigrations
python manage.py migrate
```

### 👑 Суперпользователь
```bash
python manage.py createsuperuser
```

### ▶ Запуск сервера
```bash
python manage.py runserver
```

---

## 🗄 Работа с базой данных

### ⭐ Создать привычку
```python
Habit.objects.create(
    name="Пить воду",
    xp_reward=10,
    user=user
)
```

### 📈 Получить XP пользователя
```python
from habits.utils import get_total_xp
get_total_xp(user)
```

### 🧮 Рассчитать уровень
```python
from habits.utils import get_level_info
get_level_info(total_xp)
```

---

## 🔧 Администрирование
- Панель администратора: `/admin`
- Управление:
  - пользователями  
  - привычками  
  - логами выполнения  
  - наградами  
  - профилями  

---

## 🔐 Безопасность
- Django CSRF защита  
- Защита паролей (PBKDF2)  
- `login_required` на всех защищённых страницах  
- Ограничение изменения привычек только их владельцем  
- Unique constraint на `HabitLog(habit, date)`  

---

## 📄 Лицензия
```
MIT License — свободное использование, модификация, распространение.
```

---

## 🤝 Вклад в проект
1. Форк  
2. Новая ветка  
```bash
git checkout -b feature/your-feature
```
3. Изменения  
4. Pull Request  

---

✨ *Спасибо, что используешь Habit Tracker!*
