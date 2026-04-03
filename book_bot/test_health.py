"""
Локальная проверка health check эндпоинта
Запустите бота, затем этот скрипт для проверки
"""
import asyncio
import aiohttp
import sys

HTTP_PORT = 8080
HEALTH_URL = f"http://localhost:{HTTP_PORT}/health"


async def check_health():
    """Проверка health check эндпоинта"""
    print(f"Проверка: {HEALTH_URL}")
    print("-" * 50)
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(HEALTH_URL, timeout=10) as resp:
                print(f"Статус: {resp.status}")
                
                if resp.status == 200:
                    data = await resp.json()
                    print(f"✅ Бот работает!")
                    print(f"   Статус: {data['status']}")
                    print(f"   Бот: {data['bot']}")
                    print(f"   Uptime: {data['uptime']}")
                    print(f"   Время: {data['timestamp']}")
                    return True
                else:
                    data = await resp.json()
                    print(f"❌ Бот не работает: {data['status']}")
                    return False
                    
    except asyncio.TimeoutError:
        print("❌ Таймаут соединения")
        print("   Убедитесь, что бот запущен: py bot.py")
        return False
    except aiohttp.ClientError as e:
        print(f"❌ Ошибка соединения: {e}")
        print("   Убедитесь, что бот запущен: py bot.py")
        return False


async def check_index():
    """Проверка главной страницы"""
    index_url = f"http://localhost:{HTTP_PORT}/"
    print(f"\nПроверка главной: {index_url}")
    print("-" * 50)
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(index_url, timeout=10) as resp:
                if resp.status == 200:
                    print("✅ Главная страница доступна")
                    return True
                else:
                    print(f"❌ Статус: {resp.status}")
                    return False
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False


async def main():
    print("=" * 50)
    print("ПРОВЕРКА HEALTH CHECK ЭНДПОИНТОВ")
    print("=" * 50)
    
    health_ok = await check_health()
    index_ok = await check_index()
    
    print("\n" + "=" * 50)
    if health_ok and index_ok:
        print("✅ Все эндпоинты работают!")
        print("\nДля UptimeRobot используйте:")
        print(f"  URL: http://your-domain:{HTTP_PORT}/health")
        print(f"  Monitor Type: HTTP(s)")
        print(f"  Interval: 5 minutes")
    else:
        print("❌ Некоторые эндпоинты недоступны")
        print("   Запустите бота: py bot.py")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())
