from aiogram import types
from aiogram.dispatcher import Dispatcher
from config import MANAGER_USERNAME


async def manager(message: types.Message):

    await message.answer(
        "👨‍💼 <b>Связь с менеджером</b>\n\n"

        "Наш менеджер поможет вам:\n\n"

        "📦 Рассчитать стоимость доставки\n"
        "🏭 Найти поставщика\n"
        "📷 Проверить товар\n"
        "🚚 Организовать доставку\n\n"

        f"💬 Telegram менеджера:\n"
        f"{MANAGER_USERNAME}",
        parse_mode="HTML"
    )


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(manager, lambda m: m.text == "👨 Связь с менеджером")