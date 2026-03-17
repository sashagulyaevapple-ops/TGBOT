from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from keyboards.questions_menu import questions_menu
from keyboards.menu import menu
from config import MANAGER_USERNAME, CARGO_TIME, WHITE_TIME


class QuestionState(StatesGroup):
    waiting_question = State()


# открыть меню вопросов
async def open_questions(message: types.Message):
    await message.answer(
        "❓ <b>Вопросы по доставке из Китая</b>\n\n"
        "Выберите интересующий вопрос:",
        parse_mode="HTML",
        reply_markup=questions_menu
    )


# Карго
async def cargo_info(message: types.Message):
    await message.answer(
        "📦 <b>Карго доставка</b>\n\n"

        "Карго — это самый популярный способ доставки товаров из Китая.\n\n"

        "Груз консолидируется на нашем складе в Китае и "
        "отправляется в Россию без индивидуального таможенного оформления.\n\n"

        "<b>Преимущества:</b>\n"
        "✅ Низкая стоимость доставки\n"
        "✅ Быстрая логистика\n"
        "✅ Подходит для большинства товаров\n"
        "✅ Можно отправлять небольшие партии\n\n"

        "<b>Недостатки:</b>\n"
        "⚠️ Нет индивидуальной таможенной декларации\n"
        "⚠️ Не подходит для официальной продажи крупным компаниям\n\n"

        f"⏱ Средний срок доставки: <b>{CARGO_TIME}</b>\n\n"

        f"💬 Если нужна помощь с расчетом — напишите менеджеру {MANAGER_USERNAME}",
        parse_mode="HTML"
    )


# Белая доставка
async def white_info(message: types.Message):
    await message.answer(
        "📄 <b>Белая доставка</b>\n\n"

        "Белая доставка — это официальный импорт товаров "
        "с полной таможенной очисткой.\n\n"

        "Такая доставка подходит для бизнеса, "
        "когда требуется полный пакет документов.\n\n"

        "<b>Преимущества:</b>\n"
        "✅ Полностью легальная доставка\n"
        "✅ Таможенные документы\n"
        "✅ Можно продавать товар официально\n"
        "✅ Подходит для маркетплейсов\n\n"

        "<b>Недостатки:</b>\n"
        "⚠️ Стоимость выше чем у карго\n"
        "⚠️ Более длительный срок доставки\n\n"

        f"⏱ Средний срок доставки: <b>{WHITE_TIME}</b>\n\n"

        f"💬 Подробности можно уточнить у менеджера {MANAGER_USERNAME}",
        parse_mode="HTML"
    )


# Стоимость
async def price_info(message: types.Message):
    await message.answer(
        "💰 <b>Стоимость доставки</b>\n\n"

        "Стоимость зависит от:\n\n"

        "📦 веса груза\n"
        "📍 города доставки\n"
        "📄 типа доставки\n\n"

        "Обычно стоимость начинается:\n\n"

        "🚚 Карго: от 4$/кг\n"
        "📄 Белая доставка: от 7$/кг\n\n"

        "Для точного расчета воспользуйтесь "
        "калькулятором доставки в меню бота.",
        parse_mode="HTML"
    )


# сроки
async def time_info(message: types.Message):
    await message.answer(
        "⏱ <b>Сроки доставки из Китая</b>\n\n"

        "🚚 Карго доставка:\n"
        "≈ 20 дней\n\n"

        "📄 Белая доставка:\n"
        "≈ 40 дней\n\n"

        "Срок зависит от:\n"
        "• типа товара\n"
        "• загруженности логистики\n"
        "• города доставки\n\n"

        "Мы всегда стараемся доставить груз максимально быстро.",
        parse_mode="HTML"
    )


# почему мы
async def why_us(message: types.Message):
    await message.answer(
        "🏢 <b>Почему выбирают нас</b>\n\n"

        "Компания <b>Китайский Партнер</b> уже более "
        "<b>11 лет</b> занимается доставкой товаров из Китая.\n\n"

        "За это время мы организовали тысячи поставок "
        "для предпринимателей и компаний.\n\n"

        "<b>Наши преимущества:</b>\n\n"

        "🏭 Собственный склад в Китае\n"
        "📦 Консолидация грузов\n"
        "📷 Фото и проверка товара\n"
        "🔎 Помощь в поиске поставщиков\n"
        "🚚 Быстрая логистика\n"
        "📑 Помощь с документами\n\n"

        "Мы сопровождаем клиента на каждом этапе — "
        "от поиска товара до получения груза.\n\n"

        f"💬 Написать менеджеру: {MANAGER_USERNAME}",
        parse_mode="HTML"
    )


# Другое
async def other_question(message: types.Message, state: FSMContext):
    await QuestionState.waiting_question.set()

    await message.answer(
        "✍️ Напишите ваш вопрос по доставке.\n\n"
        "Наш AI попробует ответить, "
        "а при необходимости менеджер поможет дополнительно."
    )


# назад
async def back(message: types.Message, state: FSMContext):
    await state.finish()

    await message.answer(
        "⬅️ Вы вернулись в главное меню",
        reply_markup=menu
    )


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(open_questions, lambda m: m.text == "❓ Вопросы по доставке")
    dp.register_message_handler(cargo_info, lambda m: m.text == "📦 Что такое карго доставка")
    dp.register_message_handler(white_info, lambda m: m.text == "📄 Что такое белая доставка")
    dp.register_message_handler(price_info, lambda m: m.text == "💰 Стоимость доставки")
    dp.register_message_handler(time_info, lambda m: m.text == "⏱ Сроки доставки")
    dp.register_message_handler(why_us, lambda m: m.text == "🏢 Почему мы")
    dp.register_message_handler(other_question, lambda m: m.text == "📝 Другое")
    dp.register_message_handler(back, lambda m: m.text == "⬅️ Назад", state="*")