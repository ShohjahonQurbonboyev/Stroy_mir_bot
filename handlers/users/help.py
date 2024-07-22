from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp(), state="*")
async def bot_help(message: types.Message):
    text = ("<b>D I Q Q A T:</b>\n\nXurmatli obunachilar bu bot Stroy Mir do'konini rasmiy telegram boti xisoblanadi\n\n<b>Botning maqsadi:</b>\n\nSiz bizning do'konimizdan sotib olgan maxsulotlar ustidagi kodni kiritish yordamida ball to'playsiz, va Shaxsiy kabinet yordamida siz ballaringizni tekshirib borishingiz mumkin bo'ladi, siz bu yig'ilgan ballar yordamida bizning do'kondagi keng imkoniyatlardan foydalanishingiz mumkin bo'ladi")
    
    await message.reply(text=text)
