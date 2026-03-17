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


# 📱 кнопка телефона
phone_kb = ReplyKeyboardMarkup(resize_keyboard=True)
phone_kb.add(
    KeyboardButton("📱 Отправить телефон", request_contact=True)
)
phone_kb.add(KeyboardButton("❌ Отмена"))


# ❌ отмена
async def cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("❌ Оформление отменено", reply_markup=menu)


# 📝 старт
async def start_order(message: types.Message):
    await OrderState.link.set()

    await message.answer(
        "📝 <b>Оформление заказа</b>\n\n"
        "🔗 Отправьте ссылку на товар",
        parse_mode="HTML"
    )


# 🔗 ссылка
async def get_link(message: types.Message, state: FSMContext):
    text = message.text.strip()

    if text == "❌ Отмена":
        await cancel(message, state)
        return

    if not text.startswith("http"):
        await message.answer("⚠️ Отправьте корректную ссылку")
        return

    await state.update_data(link=text)

    await OrderState.next()
    await message.answer("📦 Укажите количество товара:")


# 📦 количество (без ограничений)
async def get_quantity(message: types.Message, state: FSMContext):
    text = message.text.strip()

    if text == "❌ Отмена":
        await cancel(message, state)
        return

    if len(text) < 1:
        await message.answer("⚠️ Укажите количество")
        return

    await state.update_data(quantity=text)

    await OrderState.next()
    await message.answer("🏙 Укажите город доставки:")


# 🏙 город
async def get_city(message: types.Message, state: FSMContext):
    text = message.text.strip()

    if text == "❌ Отмена":
        await cancel(message, state)
        return

    await state.update_data(city=text)

    await OrderState.next()

    await message.answer(
        "📱 Отправьте номер телефона",
        reply_markup=phone_kb
    )


# 📱 телефон
async def get_phone(message: types.Message, state: FSMContext):

    if message.text == "❌ Отмена":
        await cancel(message, state)
        return

    if message.contact:
        phone = message.contact.phone_number
    else:
        phone = message.text

    data = await state.get_data()
    user = message.from_user

    text = (
        "🔥 <b>Новая заявка (заказ)</b>\n\n"
        f"👤 @{user.username if user.username else 'нет username'}\n"
        f"🆔 {user.id}\n\n"
        f"🔗 {data['link']}\n"
        f"📦 {data['quantity']}\n"
        f"🏙 {data['city']}\n"
        f"📱 {phone}"
    )

    await message.bot.send_message(
        chat_id=MANAGER_ID,
        text=text,
        parse_mode="HTML"
    )

    await message.answer(
        "✅ <b>Заявка отправлена!</b>\n\nМенеджер свяжется с вами",
        parse_mode="HTML"
    )

    await state.finish()

    await message.answer("🏠 Главное меню", reply_markup=menu)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_order, lambda m: m.text == "📝 Сделать заказ")

    dp.register_message_handler(cancel, lambda m: m.text == "❌ Отмена", state="*")

    dp.register_message_handler(get_link, state=OrderState.link)
    dp.register_message_handler(get_quantity, state=OrderState.quantity)
    dp.register_message_handler(get_city, state=OrderState.city)
    dp.register_message_handler(get_phone, content_types=["contact", "text"], state=OrderState.phone)