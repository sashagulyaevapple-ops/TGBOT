from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from config import MANAGER_ID
from keyboards.menu import menu


class SearchState(StatesGroup):
    query = State()


# старт
async def search(message: types.Message):
    await SearchState.query.set()

    await message.answer(
        "🔎 <b>Поиск товара</b>\n\n"
        "Напишите название товара\n"
        "или отправьте фото",
        parse_mode="HTML"
    )


# обработка текста и фото
async def search_result(message: types.Message, state: FSMContext):

    user = message.from_user

    # 📦 если текст
    if message.text:
        query = message.text

        # отправка менеджеру
        text = (
            "🔎 <b>Новая заявка (поиск)</b>\n\n"
            f"👤 @{user.username if user.username else 'нет username'}\n"
            f"🆔 {user.id}\n\n"
            f"📦 Запрос: {query}"
        )

        await message.bot.send_message(
            chat_id=MANAGER_ID,
            text=text,
            parse_mode="HTML"
        )

        # ответ пользователю
        await message.answer(
            f"🔎 <b>Вы ищете:</b> {query}\n\n"
            "💼 <b>Мы можем:</b>\n"
            "• Найти товар напрямую у поставщиков\n"
            "• Проверить качество перед отправкой\n"
            "• Сделать фото/видео отчет\n"
            "• Организовать доставку под ключ\n\n"
            "✅ Менеджер свяжется с вами для уточнения",
            parse_mode="HTML"
        )

    # 🖼 если фото
    elif message.photo:
        photo = message.photo[-1].file_id

        caption = (
            "🖼 <b>Новая заявка (поиск по фото)</b>\n\n"
            f"👤 @{user.username if user.username else 'нет username'}\n"
            f"🆔 {user.id}"
        )

        await message.bot.send_photo(
            chat_id=MANAGER_ID,
            photo=photo,
            caption=caption,
            parse_mode="HTML"
        )

        # ответ пользователю
        await message.answer(
            "🖼 <b>Вы ищете товар по фото</b>\n\n"
            "💼 <b>Мы можем:</b>\n"
            "• Найти аналогичный товар в Китае\n"
            "• Подобрать лучшие цены\n"
            "• Проверить качество\n"
            "• Организовать доставку\n\n"
            "✅ Менеджер свяжется с вами для уточнения",
            parse_mode="HTML"
        )

    await state.finish()

    await message.answer("🏠 Главное меню", reply_markup=menu)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(search, lambda m: m.text == "🔎 Поиск товаров")
    dp.register_message_handler(search_result, content_types=["text", "photo"], state=SearchState.query)