from aiogram import types
from loader import dp, db
from aiogram.dispatcher.storage import FSMContext
from states.states import main, generation_code
from keyboards.default.default_keyboards import register_button, back_markup



@dp.message_handler(text= "💰 Mening xisobim", state=main.menu)
async def account(message: types.Message, state: FSMContext):
    try:
        users = await db.select_user(telegram_id=message.from_user.id)
        if users:
            if users[5] is None:
                username = "Mavjud emas"
            else:
                username = str(f"@{users[5]}")
            await message.answer_photo(photo=users[4], caption=f"SHAXSIY XISOB\n\n<b>Ism :</b> {users[1]}\n\n<b>Familiya :</b> {users[2]}\n\n<b>Telefon raqam :</b> {users[3]}\n\n<b>Username :</b> {username}\n\n<b>To'plangan ballar soni :</b> {users[6]} ta")
        else:
            await message.answer("Siz ro'yhatdan o'tmagansiz", register_button()[0])
            await state.finish()
    except  Exception as ex:
        await message.answer(ex)



@dp.message_handler(text= "📲 Kodni kiritish", state=main.menu)
async def generate_code(message: types.Message, state: FSMContext):
    try:
        user = await db.select_user(telegram_id=message.from_user.id)
        await message.answer(f"Xurmatli {user[1]}, mahsulot ustidagi kodni yuboring !", reply_markup=back_markup)
        await generation_code.kod.set()
    except  Exception as ex:
        await message.answer(ex)


@dp.message_handler(state=generation_code.kod)
async def generate_code(message: types.Message, state: FSMContext):
    try:
        input_code = str(message.text)
        user = await db.select_user(telegram_id=message.from_user.id)
        active_codes = await db.select_code(code=input_code)
        if active_codes is None:
            await message.reply(f"Bunday promokod topilmadi ❌")
        elif str(input_code) == active_codes[1] and active_codes[3] is True:
            await db.update_code(
                code=str(input_code), 
                used=False
                )
            user_point = int(user[6]) + int(active_codes[2])
            await db.update_user_acoount(
                telegram_id=message.from_user.id,
                account=str(user_point)
            )
            await message.reply(f"Xurmatli <b>{user[1]}</b>\nSiz kiritgan promokod tasdiqlandi va sizga {active_codes[2]} ball berildi ✅", reply_markup=back_markup)
        elif str(input_code) == active_codes[1] and active_codes[3] is False:
            await message.reply(f"Siz tergan promokod allaqachon ishlatilgan 🤷‍♂️")
    except  Exception as ex:
        await message.answer(ex)                


    
        

