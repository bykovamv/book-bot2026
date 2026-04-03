"""
Просмотр логов бота в реальном времени
"""
import sys
import time
from pathlib import Path

LOG_DIR = Path(__file__).parent / "logs"
BOT_LOG = LOG_DIR / "bot.log"


def tail_log(lines=50, follow=True):
    """Показывает последние строки лога и следит за новыми"""
    if not BOT_LOG.exists():
        print(f"Файл лога не найден: {BOT_LOG}")
        print("Запустите бота сначала: py monitor.py")
        return

    with open(BOT_LOG, "r", encoding="utf-8") as f:
        # Читаем последние строки
        all_lines = f.readlines()
        for line in all_lines[-lines:]:
            print(line, end="")

        print("\n" + "=" * 50)
        print("Ожидание новых записей (Ctrl+C для выхода)...")
        print("=" * 50 + "\n")

        if follow:
            # Следим за новыми записями
            while True:
                line = f.readline()
                if line:
                    print(line, end="")
                else:
                    time.sleep(0.5)


if __name__ == "__main__":
    try:
        tail_log()
    except KeyboardInterrupt:
        print("\nПросмотр логов остановлен")
