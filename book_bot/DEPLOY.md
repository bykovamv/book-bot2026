# 🚀 Деплой бота на Render

## Что такое Render?
[Render](https://render.com/) - бесплатная облачная платформа для хостинга веб-приложений. Бот будет работать 24/7 и будет доступен из интернета для UptimeRobot.

## 📋 Шаг 1: Регистрация на Render

1. Перейдите на [https://render.com/](https://render.com/)
2. Нажмите **Get Started for Free**
3. Зарегистрируйтесь через **GitHub** (рекомендуется)
4. Разрешите доступ к репозиториям

## 🎯 Шаг 2: Создание Web Service

### Вариант A: Автоматический деплой (рекомендуется)

1. Перейдите на [Dashboard](https://dashboard.render.com/)
2. Нажмите **New +** → **Blueprint**
3. Подключите репозиторий `book-bot2026`
4. Render автоматически прочитает `render.yaml`
5. Нажмите **Apply**

### Вариант B: Ручной деплой

1. **New +** → **Web Service**
2. Подключите репозиторий `book-bot2026`
3. Заполните форму:

| Поле | Значение |
|------|----------|
| **Name** | `book-bot-2026` |
| **Region** | Frankfurt (Germany) |
| **Branch** | `master` |
| **Root Directory** | `book_bot` |
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python bot.py` |
| **Plan** | Free |

## ⚙️ Шаг 3: Настройка переменных окружения

На странице **Environment** добавьте переменные:

### Обязательные переменные

```env
BOT_TOKEN=7809984083:AAFYWkhihx5YYd9R1fLlbOo6t_qPLg4B1F0
```

### Прокси (для России)

```env
PROXY_URL=http://167.103.31.122:8800
```

**Важно:** Бесплатные прокси нестабильны! Если бот не запускается:
1. Запустите локально: `py find_proxy.py`
2. Найдите новый рабочий прокси
3. Обновите `PROXY_URL` на Render

### Порт (автоматически)

```env
HTTP_PORT=8080
```

Render автоматически устанавливает `PORT`, но мы используем свой.

## 🌐 Шаг 4: Получение URL бота

После деплоя Render выдаст URL:
```
https://book-bot-2026-xxxx.onrender.com
```

Проверьте работу:
```
https://book-bot-2026-xxxx.onrender.com/health
```

Должны увидеть:
```json
{
  "status": "ok",
  "bot": "running",
  "uptime": "0:05:23",
  "timestamp": "2026-04-03T14:30:00"
}
```

## 📊 Шаг 5: Настройка UptimeRobot

1. Войдите на [UptimeRobot](https://uptimerobot.com/)
2. **Add New Monitor** → **HTTP(s)**
3. **URL**: `https://book-bot-2026-xxxx.onrender.com/health`
4. **Interval**: 5 minutes
5. **Create Monitor**

## 🔄 Шаг 6: Автоматический деплой при пуше

Render автоматически обновляет бот при каждом push в GitHub:

```bash
# Внесите изменения в код
git add .
git commit -m "Update bot"
git push origin master

# Render автоматически перезапустит бот через 1-2 минуты
```

## ⚠️ Важные моменты

### Free Plan ограничения

| Параметр | Значение |
|----------|----------|
| **Время работы** | 750 часов/мес (24/7) |
| **Сон после бездействия** | 15 минут |
| **Холодный старт** | 30-60 секунд |
| **RAM** | 512 MB |
| **CPU** | 0.1 CPU |

### Проблема: Бот "засыпает"

На бесплатном плане Render останавливает сервис после 15 минут без HTTP-запросов.

**Решение:** UptimeRobot будет проверять `/health` каждые 5 минут, не давая боту уснуть! ✅

### Проблема: Прокси перестал работать

1. Найдите новый прокси: `py find_proxy.py`
2. Обновите на Render Dashboard → Environment → `PROXY_URL`
3. Перезапустите сервис: **Manual Deploy** → **Clear build cache & Deploy**

### Проблема: Бот не запускается

1. Проверьте логи на Render Dashboard → **Logs**
2. Убедитесь, что `BOT_TOKEN` правильный
3. Проверьте `PROXY_URL` (должен быть рабочий)

## 📈 Мониторинг

### Render Dashboard
- **Metrics** - использование CPU/RAM
- **Logs** - логи бота в реальном времени
- **Events** - история деплоев и рестартов

### UptimeRobot
- Статус бота (Up/Down)
- Время отклика
- История доступности (99.9%+)

### Telegram
- Получайте уведомления при падении
- Настройте `@UptimeRobotBot`

## 🔧 Команды для управления

### Перезапуск бота
Render Dashboard → **Manual Deploy** → **Restart**

### Просмотр логов
Render Dashboard → **Logs**

### Обновление переменных
Render Dashboard → **Environment** → Изменить → **Save Changes**

## 💡 Советы

1. **Настройте Telegram уведомления** через UptimeRobot
2. **Используйте кастомный домен** (опционально)
3. **Создайте статусную страницу** для команды
4. **Мониторьте логи** при проблемах
5. **Обновляйте прокси** при необходимости

## 🆘 Поддержка

- Render Docs: https://render.com/docs
- Render Support: support@render.com
- UptimeRobot: https://uptimerobot.com/faq

## 📝 Чек-лист деплоя

- [ ] Зарегистрироваться на Render
- [ ] Подключить GitHub репозиторий
- [ ] Создать Web Service
- [ ] Добавить `BOT_TOKEN`
- [ ] Добавить `PROXY_URL`
- [ ] Дождаться деплоя (2-3 минуты)
- [ ] Проверить `/health` эндпоинт
- [ ] Создать монитор на UptimeRobot
- [ ] Протестировать бота в Telegram
- [ ] Настроить уведомления
