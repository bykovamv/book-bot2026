"""
Мониторинг и автоперезапуск бота
Запускает бота, отслеживает логи и перезапускает при падении
"""
import subprocess
import sys
import os
import time
import logging
from datetime import datetime
from pathlib import Path

# Настройка логирования монитора
LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

MONITOR_LOG = LOG_DIR / "monitor.log"
BOT_LOG = LOG_DIR / "bot.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(MONITOR_LOG, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

BOT_SCRIPT = Path(__file__).parent / "bot.py"
PYTHON_EXECUTABLE = sys.executable or "py"
MAX_RESTARTS = 10
RESTART_WINDOW = 300  # 5 минут
restart_times = []


def check_bot_health():
    """Проверка работоспособности бота"""
    # Здесь можно добавить проверку через API бота
    # Например, проверку HTTP health endpoint если есть
    return True


def run_bot():
    """Запуск бота с мониторингом"""
    # Проверяем наличие прокси
    from dotenv import load_dotenv
    load_dotenv()
    proxy_url = os.getenv("PROXY_URL", "")
    
    logging.info("=" * 50)
    logging.info("ЗАПУСК МОНИТОРА БОТА")
    logging.info(f"Скрипт бота: {BOT_SCRIPT}")
    logging.info(f"Python: {PYTHON_EXECUTABLE}")
    if proxy_url:
        logging.info(f"Прокси: {proxy_url}")
    else:
        logging.info("Прокси: не указан (прямое соединение)")
    logging.info("=" * 50)

    while True:
        # Проверяем частоту перезапусков
        now = time.time()
        restart_times.append(now)
        # Удаляем старые записи (старше 5 минут)
        restart_times[:] = [t for t in restart_times if now - t < RESTART_WINDOW]

        if len(restart_times) > MAX_RESTARTS:
            logging.critical(
                f"Бот перезапустился {MAX_RESTARTS} раз за {RESTART_WINDOW} секунд! "
                "Возможно, есть критическая ошибка. Остановка монитора."
            )
            break

        logging.info(f"Запуск бота (попытка {len(restart_times)})...")

        try:
            # Запускаем бота с логированием в файл
            with open(BOT_LOG, "a", encoding="utf-8") as log_file:
                log_file.write(f"\n{'='*50}\n")
                log_file.write(f"Запуск: {datetime.now()}\n")
                log_file.write(f"{'='*50}\n")
                log_file.flush()

                process = subprocess.Popen(
                    [PYTHON_EXECUTABLE, str(BOT_SCRIPT)],
                    stdout=log_file,
                    stderr=subprocess.STDOUT,
                    cwd=str(BOT_SCRIPT.parent),
                    encoding='utf-8'
                )

                # Ждём завершения процесса
                exit_code = process.wait()

                if exit_code == 0:
                    logging.info("Бот завершил работу корректно (код 0)")
                else:
                    logging.warning(f"Бот упал с кодом ошибки: {exit_code}")

        except FileNotFoundError:
            logging.error(f"Не найден Python интерпретатор: {PYTHON_EXECUTABLE}")
            break
        except KeyboardInterrupt:
            logging.info("Монитор остановлен пользователем")
            if 'process' in locals():
                process.terminate()
            break
        except Exception as e:
            logging.error(f"Ошибка при запуске бота: {e}")

        # Пауза перед перезапуском
        wait_time = min(2 ** min(len(restart_times), 5), 60)  # Экспоненциальная задержка
        logging.info(f"Перезапуск через {wait_time} секунд...")
        time.sleep(wait_time)

    logging.info("Мониторинг остановлен")


if __name__ == "__main__":
    try:
        run_bot()
    except KeyboardInterrupt:
        logging.info("Монитор остановлен пользователем")
