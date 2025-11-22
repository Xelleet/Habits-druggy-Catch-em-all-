# Habit Tracker

## Описание проекта
Веб-приложение для отслеживания привычек с системой опыта (XP), уровней, достижений, статистики и публичных профилей.

## Функциональность
- Регистрация и авторизация пользователей  
- Создание, выполнение и удаление привычек  
- Подсчёт XP и уровней (экспоненциальная формула)  
- Награды за стрики, XP и разнообразие  
- Профиль: статистика, прогресс-бар, уровень  
- Публичные профили  
- Лидерборд  
- AJAX-обновление уровня и XP  

## Стек технологий
- Django 4.2  
- Python 3  
- PostgreSQL  
- Django ORM  
- HTML / CSS  
- JavaScript (AJAX)  

## Инструкция запуска
### Локальный запуск
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Docker (если используется)
```bash
docker-compose build
docker-compose up
```

## Структура проекта
```
habit_tracker/
│
├── habit_tracker/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│
├── habits/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── utils.py
│   ├── templates/
│   │   ├── habits/
│   │   ├── auth/
│
├── static/              # статические файлы
├── templates/           # глобальные шаблоны
├── manage.py
```

## Команды управления
### Миграции
```bash
python manage.py makemigrations
python manage.py migrate
```

### Создать суперпользователя
```bash
python manage.py createsuperuser
```

### Запуск сервера
```bash
python manage.py runserver
```

## Управление с БД
### Создание привычки
Через Django ORM:
```python
Habit.objects.create(
    name="Пить воду",
    description="2 литра в день",
    xp_reward=10,
    user=user
)
```

### Получение XP
```python
from habits.utils import get_total_xp
get_total_xp(user)
```

### Получение уровня
```python
from habits.utils import get_level_info
get_level_info(total_xp)
```

## Администрирование
- Панель администратора: `/admin/`
- Управление:
  - пользователями  
  - привычками  
  - логами выполнения  
  - наградами  
  - профилями  

## Безопасность
- CSRF защита  
- Пароли хранятся через Django PBKDF2  
- Ограниченный доступ к CRUD операций  
- Декоратор `login_required`  
- Защита от выполнения чужих привычек  

## Лицензия разработчика
```
MIT License  
Автор разрешает использовать проект свободно, включая модификации и коммерческие цели.
```

## Вклад в проект
Pull-request приветствуются:
1. Форкните репозиторий  
2. Создайте ветку:
```bash
git checkout -b feature/something
```
3. Сделайте изменения  
4. Отправьте PR  
