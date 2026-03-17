from aiogram import types
from aiogram.dispatcher import Dispatcher

from services.ai import ask_ai


async def ai_chat(message: types.Message):

    await message.answer("🤖 Думаю...")

    answer = await ask_ai(message.text)

    await message.answer(answer)


def register_handlers(dp: Dispatcher):

    dp.register_message_handler(ai_chat)