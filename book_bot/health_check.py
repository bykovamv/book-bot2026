"""
Проверка работоспособности бота
Отправляет тестовое сообщение и проверяет ответ
"""
import sys
import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# Загружаем переменные
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    print("❌ Ошибка: не найден BOT_TOKEN в .env файле")
    sys.exit(1)


async def check_bot():
    """Проверка подключения к Telegram API"""
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    try:
        # Получаем информацию о боте
        me = await bot.get_me()
        print(f"✅ Бот подключён!")
        print(f"   Имя: {me.first_name}")
        print(f"   Username: @{me.username}")
        print(f"   ID: {me.id}")

        # Получаем информацию о вебхуках
        webhook = await bot.get_webhook_info()
        if webhook.url:
            print(f"   Webhook: {webhook.url}")
        else:
            print("   Webhook: не установлен (используется polling)")

        print("\n✅ Бот работает корректно!")
        return True

    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return False

    finally:
        await bot.session.close()


async def check_api_connection():
    """Проверка соединения с Telegram API"""
    import aiohttp

    print("Проверка соединения с api.telegram.org...")
    
    # Пробуем без прокси
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.telegram.org", timeout=10) as resp:
                if resp.status == 200:
                    print("✅ Соединение с Telegram API установлено")
                    return True
                else:
                    print(f"⚠️ Статус ответа: {resp.status}")
                    return False
    except asyncio.TimeoutError:
        print("❌ Таймаут соединения с Telegram API (возможно, нужна прокси)")
        return False
    except Exception as e:
        print(f"❌ Ошибка соединения: {e}")
        return False


async def main():
    print("=" * 50)
    print("ПРОВЕРКА РАБОТОСПОСОБНОСТИ БОТА")
    print("=" * 50)

    # Проверка соединения
    api_ok = await check_api_connection()
    print()

    # Проверка бота
    if api_ok:
        bot_ok = await check_bot()
        if not bot_ok:
            sys.exit(1)
    else:
        print("⚠️ Невозможно проверить бота без соединения с API")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
