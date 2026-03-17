from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class TrackState(StatesGroup):
    track = State()


async def tracking(message: types.Message):

    await TrackState.track.set()

    await message.answer(
        "🚚 Введите ТРЕК НОМЕР вашего груза:"
    )


async def tracking_result(message: types.Message, state: FSMContext):

    track = message.text.strip()

    if len(track) < 5:
        await message.answer("⚠️ Неверный трек номер")
        return

    await message.answer(
        f"📦 <b>Информация о грузе</b>\n\n"

        f"🔎 Трек номер: {track}\n\n"

        "📍 Последний статус:\n"
        "Склад Гуанчжоу\n\n"

        "🚚 Статус:\n"
        "Груз отправлен в Россию\n\n"

        "⏱ Примерное время доставки:\n"
        "10-14 дней",
        parse_mode="HTML"
    )

    await state.finish()


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(tracking, lambda m: m.text == "🚚 Отследить груз")
    dp.register_message_handler(tracking_result, state=TrackState.track)