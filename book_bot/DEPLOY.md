# 📚 Как развернуть бота на Render.com

## Шаг 1: Подготовьте репозиторий на GitHub

1. Откройте терминал в папке `book_bot`:
```bash
cd c:\Users\marina.v.bykova\Desktop\book_bot
```

2. Инициализируйте git (если ещё не инициализирован):
```bash
git init
git add .
git commit -m "Initial commit: book bot"
```

3. Создайте репозиторий на GitHub (https://github.com/new)

4. Добавьте удалённый репозиторий и сделайте push:
```bash
git remote add origin https://github.com/ВАШ_НИК/ВАШ_РЕПОЗИТОРИЙ.git
git branch -M main
git push -u origin main
```

---

## Шаг 2: Настройте Render

1. Зайдите на https://render.com и войдите через GitHub

2. Нажмите **New +** → **Web Service**

3. Подключите ваш GitHub репозиторий с ботом

4. Заполните настройки:

| Поле | Значение |
|------|----------|
| **Name** | `book-bot` (или любое другое) |
| **Region** | `Frankfurt` (ближе к России) |
| **Branch** | `main` |
| **Root Directory** | (оставьте пустым) |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python bot.py` |
| **Instance Type** | `Free` |

5. Нажмите **Advanced** и добавьте переменные окружения:

| Key | Value |
|-----|-------|
| `BOT_TOKEN` | Ваш токен из .env файла |

6. Нажмите **Create Web Service**

---

## Шаг 3: Проверьте работу

1. В логах Render вы увидите: `🤖 Бот запущен...`

2. Откройте бота в Telegram и нажмите `/start`

3. Должны появиться кнопки с жанрами!

---

## ⚠️ Важно для бесплатного тарифа

- Бот «засыпает» через 15 минут без активности
- При первом запросе «просыпается» ~30 секунд
- Для постоянной работы рассмотрите платный тариф ($7/мес)

---

## 🔧 Если бот не работает

1. Проверьте логи в панели Render (Logs)
2. Убедитесь, что токен правильный
3. Проверьте, что бот активен в @BotFather
