from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from config import CARGO_PRICE, WHITE_PRICE, CARGO_TIME, WHITE_TIME, MIN_WEIGHT


class CalcState(StatesGroup):
    weight = State()
    city = State()


async def start_calc(message: types.Message):
    await CalcState.weight.set()

    await message.answer(
        f"📦 Введите вес груза (кг)\n"
        f"Минимальный вес: {MIN_WEIGHT} кг"
    )


async def get_weight(message: types.Message, state: FSMContext):

    try:
        weight = float(message.text)
    except:
        await message.answer("⚠️ Введите вес числом")
        return

    if weight < MIN_WEIGHT:
        await message.answer(
            f"⚠️ Минимальный вес {MIN_WEIGHT} кг"
        )
        return

    await state.update_data(weight=weight)

    await CalcState.next()

    await message.answer("🏙 Укажите город доставки:")


async def get_city(message: types.Message, state: FSMContext):

    data = await state.get_data()
    weight = data["weight"]

    city = message.text

    cargo_price = weight * CARGO_PRICE
    white_price = weight * WHITE_PRICE

    await message.answer(
    f"📦 <b>Расчет доставки</b>\n\n"

    f"⚖️ Вес: {weight} кг\n"
    f"🏙 Город: {city}\n\n"

    f"🚚 <b>Карго доставка</b>\n"
    f"💰 {cargo_price:.0f}$\n"
    f"⏱ {CARGO_TIME}\n\n"

    f"📄 <b>Белая доставка</b>\n"
    f"💰 {white_price:.0f}$\n"
    f"⏱ {WHITE_TIME}\n\n"

    "💬 Для точного расчета напишите менеджеру",
    parse_mode="HTML"
)
    

    await state.finish()


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_calc, lambda m: m.text == "📦 Рассчитать доставку")
    dp.register_message_handler(get_weight, state=CalcState.weight)
    dp.register_message_handler(get_city, state=CalcState.city)