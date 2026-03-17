from aiogram.types import ReplyKeyboardMarkup

questions_menu = ReplyKeyboardMarkup(resize_keyboard=True)
questions_menu.add("📦 Что такое карго доставка")
questions_menu.add("📄 Что такое белая доставка")
questions_menu.add("💰 Стоимость доставки")
questions_menu.add("⏱ Сроки доставки")
questions_menu.add("🏢 Почему мы")
questions_menu.add("📝 Другое")
questions_menu.add("⬅️ Назад")