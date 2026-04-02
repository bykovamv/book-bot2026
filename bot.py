import asyncio
import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiohttp import web

# Загружаем переменные из .env файла
load_dotenv()

# Токен бота (получите у @BotFather)
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Прокси (если нужно для обхода блокировок)
PROXY_URL = os.getenv("PROXY_URL", None)

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Создаём роутер
router = Router()

# ==================== БАЗА КНИГ ====================
BOOKS = {
    "фантастика": [
        {"title": "Дюна", "author": "Фрэнк Герберт", "desc": "Эпическая научная фантастика о пустынной планете Арракис"},
        {"title": "Основание", "author": "Айзек Азимов", "desc": "Классика о падении Галактической империи"},
        {"title": "Нейромант", "author": "Уильям Гибсон", "desc": "Киберпанк-роман, определивший жанр"},
        {"title": "Задача трёх тел", "author": "Лю Цысинь", "desc": "Современная НФ о контакте с инопланетной цивилизацией"},
    ],
    "детектив": [
        {"title": "Убийство в Восточном экспрессе", "author": "Агата Кристи", "desc": "Классический детектив с Эркюлем Пуаро"},
        {"title": "Девушка с татуировкой дракона", "author": "Стиг Ларссон", "desc": "Мрачный шведский триллер"},
        {"title": "Щегол", "author": "Донна Тартт", "desc": "Детектив с элементами искусства и тайны"},
    ],
    "роман": [
        {"title": "Гордость и предубеждение", "author": "Джейн Остин", "desc": "Классический роман о любви и обществе"},
        {"title": "Нормальные люди", "author": "Салли Руни", "desc": "Современная история о сложных отношениях"},
        {"title": "Виноваты звёзды", "author": "Джон Грин", "desc": "Трогательная история любви"},
    ],
    "фэнтези": [
        {"title": "Властелин колец", "author": "Дж. Р. Р. Толкин", "desc": "Эпическое фэнтези о Средиземье"},
        {"title": "Гарри Поттер", "author": "Дж. К. Роулинг", "desc": "История о мальчике-волшебнике"},
        {"title": "Имя ветра", "author": "Патрик Ротфусс", "desc": "История легендарного мага"},
        {"title": "Ведьмак", "author": "Анджей Сапковский", "desc": "Приключения Геральта из Ривии"},
    ],
    "психология": [
        {"title": "Думай медленно... решай быстро", "author": "Даниэль Канеман", "desc": "О мышлении и принятии решений"},
        {"title": "Атомные привычки", "author": "Джеймс Клир", "desc": "Как формировать полезные привычки"},
        {"title": "Тонкое искусство пофигизма", "author": "Марк Мэнсон", "desc": "Нестандартный подход к счастливой жизни"},
    ],
    "бизнес": [
        {"title": "Богатый папа, бедный папа", "author": "Роберт Кийосаки", "desc": "Финансовая грамотность для всех"},
        {"title": "От хорошего к великому", "author": "Джим Коллинз", "desc": "Почему одни компании становятся великими"},
        {"title": "Rework", "author": "Джейсон Фрайд", "desc": "Перезагрузка бизнеса по-новому"},
    ],
    "история": [
        {"title": "Sapiens", "author": "Юваль Ной Харари", "desc": "Краткая история человечества"},
        {"title": "Искусство войны", "author": "Сунь-цзы", "desc": "Древний трактат о стратегии"},
        {"title": "17 мгновений весны", "author": "Юлиан Семёнов", "desc": "Легендарный шпионский роман"},
    ],
    "ужасы": [
        {"title": "Сияние", "author": "Стивен Кинг", "desc": "Мрачная история об отеле и безумии"},
        {"title": "Дракула", "author": "Брэм Стокер", "desc": "Классика о вампирах"},
        {"title": "Дом листьев", "author": "Марк З. Даниелевски", "desc": "Экспериментальный хоррор-роман"},
    ],
}

# ==================== МАШИНА СОСТОЯНИЙ (FSM) ====================
class BookRecommendation(StatesGroup):
    waiting_for_interest = State()


# ==================== КЛАВИАТУРЫ ====================
def get_interests_keyboard():
    """Создаёт клавиатуру с жанрами книг"""
    builder = InlineKeyboardBuilder()
    for genre in BOOKS.keys():
        builder.button(text=genre.capitalize(), callback_data=f"genre_{genre}")
    builder.adjust(2)  # 2 кнопки в ряд
    return builder.as_markup()


def get_retry_keyboard():
    """Клавиатура для повторной попытки"""
    builder = InlineKeyboardBuilder()
    builder.button(text="🔄 Выбрать другой интерес", callback_data="retry")
    return builder.as_markup()


# ==================== ОБРАБОТЧИКИ КОМАНД ====================
@router.message(Command("start"))
async def cmd_start(message: Message):
    """Обработчик команды /start"""
    logging.info(f"Получена команда /start от пользователя {message.from_user.id}")
    await message.answer(
        "👋 Привет! Я бот для подбора книг.\n\n"
        "Расскажи, какой жанр тебя интересует?",
        reply_markup=get_interests_keyboard()
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    """Обработчик команды /help"""
    await message.answer(
        "📚 <b>Команды бота:</b>\n\n"
        "/start - начать подбор книги\n"
        "/help - показать эту справку\n\n"
        "Выбери жанр из списка, и я порекомендую тебе книгу!"
    )


# ==================== ОБРАБОТЧИКИ КНОПОК ====================
@router.callback_query(F.data.startswith("genre_"))
async def process_genre(callback: CallbackQuery):
    """Обработка выбора жанра"""
    genre = callback.data.replace("genre_", "")
    
    if genre not in BOOKS:
        await callback.answer("❌ Жанр не найден", show_alert=True)
        return
    
    # Выбираем случайную книгу из жанра
    import random
    book = random.choice(BOOKS[genre])
    
    await callback.message.answer(
        f"📖 <b>Рекомендация для жанра '{genre.capitalize()}':</b>\n\n"
        f"📕 <b>{book['title']}</b>\n"
        f"✍️ Автор: {book['author']}\n"
        f"📝 {book['desc']}",
        reply_markup=get_retry_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "retry")
async def process_retry(callback: CallbackQuery):
    """Повторный выбор жанра"""
    await callback.message.edit_text(
        "Выберите другой жанр:",
        reply_markup=get_interests_keyboard()
    )
    await callback.answer()


# Обработчик всех сообщений (для отладки)
@router.message()
async def echo_all(message: Message):
    """Логирование всех сообщений"""
    logging.info(f"Получено сообщение: {message.text} от {message.from_user.id}")
    await message.answer("Я пока умею только подбирать книги. Нажмите /start")


# ==================== ЗАПУСК БОТА ====================
async def main():
    """Основная функция запуска"""
    # Создаём бота
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    # Регистрируем роутер
    dp.include_router(router)

    # Создаём HTTP-сервер для Render (чтобы был открытый порт)
    async def health_handler(request):
        return web.Response(text="OK")
    
    app = web.Application()
    app.router.add_get('/', health_handler)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()
    
    print("🤖 Бот запущен... HTTP-сервер на порту 8080")
    logging.info("Бот запущен и готов к работе")
    
    # Запускаем polling и HTTP-сервер параллельно
    async def start_polling_task():
        try:
            await dp.start_polling(bot)
        finally:
            await bot.session.close()
    
    await asyncio.gather(
        start_polling_task(),
        asyncio.sleep(float('inf'))  # Держим HTTP-сервер запущенным
    )


if __name__ == "__main__":
    asyncio.run(main())
