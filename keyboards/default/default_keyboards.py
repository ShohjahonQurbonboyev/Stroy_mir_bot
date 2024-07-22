from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, WebAppInfo





back_btn =  KeyboardButton("🔙 Orqaga")
back_markup = ReplyKeyboardMarkup(resize_keyboard=True)
back_markup.add(back_btn)


def register_button() -> ReplyKeyboardMarkup(): 
    register_btn = "Ro'yhatdan o'tish"
    register_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    register_markup.add(KeyboardButton(register_btn))


    phone_btn = KeyboardButton("Telefon raqamni ulashish", request_contact=True)
    phone_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width= 2)
    phone_markup.add(phone_btn, back_btn)

    return register_markup, phone_markup


def create_main_btn() -> ReplyKeyboardMarkup():
    btn = ["💰 Mening xisobim", "📲 Kodni kiritish"]
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for button in btn:
        markup.insert(KeyboardButton(button))
    return markup


def create_main_admin() -> ReplyKeyboardMarkup():
    btn = ["➕ Promokod", "🗑 O'chirish", "📁 Malumotlar", "✏️ O'zgartirish"]
    log_out = KeyboardButton("📤 Chiqish")
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for button in btn:
        markup.insert(KeyboardButton(button))
    markup.add(log_out)
    return markup


def delete_btn() -> ReplyKeyboardMarkup():
    btn = ["❌ Barcha userlar ❌", "❌ User ❌", "❌ Barcha promokodlar ❌"]
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for button in btn:
        markup.insert(KeyboardButton(button))
    markup.add(back_btn)
    return markup


def data_btn() -> ReplyKeyboardMarkup():
    btn = ["🚻 Foydalanuvchilar", "👥 Foydalanuvchilar soni", "👤 Foydalanuvchi haqida"]
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    for button in btn:
        markup.insert(KeyboardButton(button))
    markup.add(back_btn)
    return markup


def add_code():
    btn = ["➕ Donalab qo'shish", "🗂 Excelda qo'shish"]
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for button in btn:
        markup.insert(KeyboardButton(button))
    markup.add(back_btn)
    return markup