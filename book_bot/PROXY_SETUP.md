# 🔒 Настройка прокси для бота

## Проблема
Telegram может быть заблокирован в вашей сети. Если `health_check.py` показывает **"Таймаут соединения"**, вам нужен прокси.

## Варианты прокси

### 1. Бесплатные HTTP прокси
Найдите рабочие прокси на сайтах:
- https://free-proxy-list.net/
- https://www.proxy-list.download/

**Важно:** Бесплатные прокси часто нестабильны!

### 2. Платные прокси (рекомендуется)
- https://proxy6.net/ (от $0.5/мес)
- https://www.brightdata.com/
- https://socks5.net/

### 3. Собственный прокси сервер
Разверните на VPS (DigitalOcean, Linode и т.д.):
```bash
# Установка Squid прокси на Ubuntu
sudo apt install squid
sudo systemctl enable squid
```

## Настройка

### Шаг 1: Найдите рабочий прокси
Проверьте прокси командой:
```bash
curl -x http://proxy:port https://api.telegram.org
```

### Шаг 2: Добавьте в .env файл
Откройте `.env` и добавьте:
```env
PROXY_URL=http://proxy.example.com:8080
```

Для SOCKS5 прокси:
```env
PROXY_URL=socks5://user:pass@proxy.com:1080
```

### Шаг 3: Перезапустите бота
```bash
py monitor.py
```

## Проверка
```bash
py health_check.py
```

Если видите ✅ - бот подключился!

## Форматы прокси

| Тип | Формат | Пример |
|-----|--------|--------|
| HTTP | `http://host:port` | `http://123.45.67.89:8080` |
| HTTP с auth | `http://user:pass@host:port` | `http://admin:123@proxy.com:8080` |
| SOCKS5 | `socks5://host:port` | `socks5://proxy.com:1080` |
| SOCKS5 с auth | `socks5://user:pass@host:port` | `socks5://admin:123@proxy.com:1080` |

## Troubleshooting

### "Неверный формат прокси"
Проверьте формат URL. Должен начинаться с `http://`, `https://` или `socks5://`

### "Connection refused"
Прокси недоступен. Попробуйте другой прокси.

### "Authentication required"
Добавьте логин и пароль в URL: `http://user:pass@proxy:port`
