# 📚 Book Bot 2026

Telegram бот для подбора книг с мониторингом UptimeRobot.

## 🚀 Быстрый старт

### Локальный запуск

```bash
# Установка зависимостей
pip install -r requirements.txt

# Проверка соединения
py health_check.py

# Запуск бота
py bot.py
```

### Деплой на Render

См. [DEPLOY.md](DEPLOY.md) - полная инструкция по развёртыванию.

## 📊 Мониторинг

- **UptimeRobot** - внешний мониторинг каждые 5 минут
- **Health Check** - эндпоинт `/health` для проверки статуса
- **Автоперезапуск** - локальный мониторинг с `monitor.py`

См. [UPTIMEROBOT.md](UPTIMEROBOT.md) и [MONITORING.md](MONITORING.md)

## 🔧 Настройка прокси

Если Telegram заблокирован в вашей сети:

```bash
# Найти рабочий прокси
py find_proxy.py

# Добавить в .env
PROXY_URL=http://proxy:port
```

См. [PROXY_SETUP.md](PROXY_SETUP.md)

## 📁 Структура проекта

```
book_bot/
├── bot.py                  # Основной скрипт бота
├── monitor.py              # Локальный мониторинг
├── health_check.py         # Проверка соединения
├── find_proxy.py           # Поиск прокси
├── test_health.py          # Тест health check
├── render.yaml             # Конфигурация Render
├── Procfile                # Для Render
├── requirements.txt        # Зависимости
├── .env.example            # Пример .env
├── DEPLOY.md               # Инструкция по деплою
├── UPTIMEROBOT.md          # Настройка UptimeRobot
├── MONITORING.md           # Локальный мониторинг
└── PROXY_SETUP.md          # Настройка прокси
```

## 🌐 Health Check

После деплоя на Render:
```
https://your-app.onrender.com/health
```

Ответ:
```json
{
  "status": "ok",
  "bot": "running",
  "uptime": "0:05:23",
  "timestamp": "2026-04-03T14:30:00"
}
```

## 📝 Команды бота

- `/start` - начать подбор книги
- `/help` - показать справку

## 🛠 Технологии

- **Python 3.14**
- **aiogram 3.x** - Telegram Bot Framework
- **aiohttp** - HTTP сервер для health check
- **Render** - облачный хостинг
- **UptimeRobot** - мониторинг

## 📄 Лицензия

MIT
