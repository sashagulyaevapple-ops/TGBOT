from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from config import MANAGER_ID
from keyboards.menu import menu


class OrderState(StatesGroup):
    link = State()
    quantity = State()
    city = State()
    phone = State()


# клавиатуры
cancel_kb = ReplyKeyboardMarkup(resize_keyboard=True)
cancel_kb.add(KeyboardButton("❌ Отмена"))

phone_kb = ReplyKeyboardMarkup(resize_keyboard=True)
phone_kb.add(
    KeyboardButton("📱 Отправить телефон", request_contact=True),
    KeyboardButton("❌ Отмена")
)


# ❌ отмена (работает на любом этапе)
async def cancel_order(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        "❌ Оформление заказа отменено",
        reply_markup=menu
    )


# 📝 старт
async def start_order(message: types.Message):
    await OrderState.link.set()

    await message.answer(
        "📝 Оформление заказа\n\n"
        "Отправьте ссылку на товар",
        reply_markup=cancel_kb
    )


# 🔗 ссылка
async def get_link(message: types.Message, state: FSMContext):
    await state.update_data(link=message.text)

    await OrderState.next()
    await message.answer(
        "📦 Укажите количество товара:",
        reply_markup=cancel_kb
    )


# 📦 количество
async def get_quantity(message: types.Message, state: FSMContext):
    await state.update_data(quantity=message.text)

    await OrderState.next()
    await message.answer(
        "🏙 Укажите город доставки:",
        reply_markup=cancel_kb
    )


# 🏙 город
async def get_city(message: types.Message, state: FSMContext):
    await state.update_data(city=message.text)

    await OrderState.next()

    await message.answer(
        "📱 Отправьте номер телефона",
        reply_markup=phone_kb
    )


# 📱 телефон
async def get_phone(message: types.Message, state: FSMContext):
    if message.contact:
        phone = message.contact.phone_number
    else:
        phone = message.text

    data = await state.get_data()
    user = message.from_user

    text = (
        "🔥 Новая заявка (заказ)\n\n"
        f"👤 @{user.username if user.username else 'нет username'}\n"
        f"🆔 {user.id}\n\n"
        f"🔗 Ссылка: {data['link']}\n"
        f"📦 Количество: {data['quantity']}\n"
        f"🏙 Город: {data['city']}\n"
        f"📱 Телефон: {phone}"
    )

    await message.bot.send_message(
        chat_id=MANAGER_ID,
        text=text
    )

    await message.answer(
        "✅ Заявка отправлена!\n\n"
        "Менеджер свяжется с вами в ближайшее время."
    )

    await state.finish()

    await message.answer(
        "🏠 Главное меню",
        reply_markup=menu
    )


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_order, lambda m: m.text == "📝 Сделать заказ")

    dp.register_message_handler(cancel_order, lambda m: m.text == "❌ Отмена", state="*")

    dp.register_message_handler(get_link, state=OrderState.link)
    dp.register_message_handler(get_quantity, state=OrderState.quantity)
    dp.register_message_handler(get_city, state=OrderState.city)
    dp.register_message_handler(get_phone, content_types=["contact", "text"], state=OrderState.phone)