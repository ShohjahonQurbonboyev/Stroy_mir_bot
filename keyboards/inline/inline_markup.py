from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup



confirm_btn = ["Tasdiqlash ✅", "Bekor qilish ❌"]
confirm_markup = InlineKeyboardMarkup()
for btn in confirm_btn:
    confirm_markup.insert(InlineKeyboardButton(text=btn, callback_data=btn))



def create_change_btn() -> InlineKeyboardMarkup():
    button_conf = InlineKeyboardButton(text="Boshlash", callback_data="0")
    change_markup = InlineKeyboardMarkup()
    change_markup.add(button_conf)


    button_unconf = InlineKeyboardButton(text="Qayta urinish", callback_data=1)
    change_markup_unconf = InlineKeyboardMarkup()
    change_markup_unconf.add(button_unconf)

    return change_markup, change_markup_unconf