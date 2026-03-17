from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(resize_keyboard=True)

menu.add(
    KeyboardButton("📝 Сделать заказ"),
    
)

menu.add(
    KeyboardButton("🔎 Поиск товаров"),
    KeyboardButton("❓ Вопросы по доставке")
)

menu.add(
    KeyboardButton("👨 Связь с менеджером")
)