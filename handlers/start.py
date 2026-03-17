from aiogram import types
from aiogram.dispatcher import Dispatcher
from keyboards.menu import menu
from config import COMPANY_NAME


async def start(message: types.Message):
    await message.answer(
        f"🚚 <b>Добро пожаловать в {COMPANY_NAME}</b>\n\n"

        "Мы занимаемся доставкой товаров из Китая.\n\n"

        "Наши услуги:\n"
        "📦 Карго доставка\n"
        "📄 Белая доставка\n"
        "🔎 Поиск товаров в Китае\n"
        "📷 Проверка товара\n"
        "🚚 Доставка до вашего города\n\n"

        "👇 Выберите нужный раздел:",
        parse_mode="HTML",
        reply_markup=menu
    )


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start"])