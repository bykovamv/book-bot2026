# 🤖 Настройка UptimeRobot мониторинга

## Что такое UptimeRobot?
[UptimeRobot](https://uptimerobot.com/) - бесплатный сервис для мониторинга сайтов и приложений. Проверяет доступность вашего бота каждые 5 минут и отправляет уведомления при сбоях.

## 📋 Шаг 1: Регистрация на UptimeRobot

1. Перейдите на [https://uptimerobot.com/](https://uptimerobot.com/)
2. Нажмите **Sign Up**
3. Зарегистрируйтесь через email или Google
4. Подтвердите email

## 🌐 Шаг 2: Публикация бота в интернет

Для UptimeRobot ваш бот должен быть доступен из интернета. Вот варианты:

### Вариант A: Render (бесплатно, рекомендуется)
1. Зарегистрируйтесь на [https://render.com/](https://render.com/)
2. Подключите GitHub репозиторий
3. Создайте Web Service
4. Render выдаст URL: `https://your-bot.onrender.com`

### Вариант B: ngrok (для тестирования)
1. Скачайте [ngrok](https://ngrok.com/)
2. Запустите: `ngrok http 8080`
3. Получите временный URL: `https://xxxx.ngrok.io`

### Вариант C: VPS сервер
Разверните бот на VPS с белым IP-адресом.

## ⚙️ Шаг 3: Создание монитора

### 1. Войдите в UptimeRobot Dashboard
Перейдите на [https://uptimerobot.com/dashboard](https://uptimerobot.com/dashboard)

### 2. Добавьте новый монитор
Нажмите **Add New Monitor**

### 3. Настройте монитор

| Поле | Значение |
|------|----------|
| **Monitor Type** | HTTP(s) |
| **Friendly Name** | `Book Bot` |
| **URL or IP** | `https://your-bot-domain.com/health` |
| **Monitoring Interval** | 5 minutes (бесплатно) |
| **Monitor Timeout** | 30 seconds |

### 4. Нажмите **Create Monitor**

## 🔔 Шаг 4: Настройка оповещений

### Email уведомления (по умолчанию)
- Автоматически включены
- Получайте письма при падении бота

### Telegram уведомления (рекомендуется)
1. **Alert Contacts** → **Add Alert Contact**
2. Выберите **Telegram**
3. Отправьте сообщение боту `@UptimeRobotBot`
4. Введите код из инструкции
5. Включите уведомления для монитора

### SMS уведомления
1. **Alert Contacts** → **Add Alert Contact**
2. Выберите **SMS**
3. Введите номер телефона
4. Подтвердите код

## 📊 Шаг 5: Проверка работы

### Локальная проверка
```bash
# Запустите бота
py bot.py

# В браузере откройте:
http://localhost:8080/health
```

Должны увидеть:
```json
{
  "status": "ok",
  "bot": "running",
  "uptime": "0:05:23.456789",
  "timestamp": "2026-04-03T14:30:00.123456"
}
```

### Проверка UptimeRobot
1. Перейдите в Dashboard
2. Статус должен быть **Up** (зелёный)
3. Время отклика: ~100-500ms

## 🎯 Пример настройки для Render

### 1. Файл `render.yaml` (в корне репозитория)
```yaml
services:
  - type: web
    name: book-bot
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python bot.py
    envVars:
      - key: BOT_TOKEN
        sync: false
      - key: PROXY_URL
        sync: false
      - key: HTTP_PORT
        value: 8080
```

### 2. URL для UptimeRobot
```
https://book-bot-xxxx.onrender.com/health
```

## 📈 Статусы монитора

| Статус | Описание | Действия |
|--------|----------|----------|
| 🟢 **Up** | Бот работает | Всё ок |
| 🔴 **Down** | Бот недоступен | Проверьте логи, перезапустите |
| 🟡 **Paused** | Мониторинг приостановлен | Нажмите **Resume** |
| ⚪ **Not Checked** | Ещё не проверялся | Подождите 5 минут |

## 🔧 Troubleshooting

### "Connection Refused"
- Убедитесь, что бот запущен
- Проверьте порт в `.env` файле
- Проверьте firewall/антивирус

### "Timeout"
- Сервер слишком медленно отвечает
- Увеличьте timeout до 60 секунд
- Проверьте интернет-соединение

### "SSL Error"
- Используйте `https://` URL
- Проверьте SSL сертификат
- Для тестирования используйте `http://`

## 💡 Советы

1. **Используйте `/health` эндпоинт** - он возвращает JSON с состоянием бота
2. **Настройте Telegram уведомления** - получайте уведомления прямо в мессенджер
3. **Проверяйте логи** - при падении смотрите `logs/bot.log`
4. **Используйте мониторинг monitor.py** - для локального автоперезапуска
5. **Создайте статусную страницу** - UptimeRobot позволяет создать публичную страницу статуса

## 📱 Статусная страница

1. **Status Pages** → **Add Status Page**
2. Выберите мониторы для отображения
3. Получите публичную ссылку: `https://stats.uptimerobot.com/xxxxx`
4. Поделитесь с командой

## 🆘 Поддержка

- Документация UptimeRobot: https://uptimerobot.com/api
- FAQ: https://uptimerobot.com/faq
- Email поддержки: support@uptimerobot.com
