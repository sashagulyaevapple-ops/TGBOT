from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import BOT_TOKEN

# handlers
from handlers.start import register_handlers as start_handlers
from handlers.questions import register_handlers as questions_handlers
from handlers.manager import register_handlers as manager_handlers
from handlers.search import register_handlers as search_handlers
from handlers.order import register_handlers as order_handlers

# бот
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# регистрация хендлеров
start_handlers(dp)
questions_handlers(dp)
manager_handlers(dp)
tracking_handlers(dp)
search_handlers(dp)
order_handlers(dp)


if __name__ == "__main__":
    print("🚀 Бот запущен...")
    executor.start_polling(dp, skip_updates=True)