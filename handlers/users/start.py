from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp, db, bot
from data.config import ADMINS, USERS_CHANNEL
from aiogram.dispatcher.storage import FSMContext
from states.states import registration, main
from keyboards.default.default_keyboards import register_button, back_markup, ReplyKeyboardRemove, create_main_btn
from keyboards.inline.inline_markup import confirm_markup, create_change_btn



@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
    try:
        await state.finish()  
        full_name = message.from_user.full_name
        user = await db.select_user(telegram_id=message.from_user.id)
        if user is None:
            await message.answer(f"Assalomu aleykum {full_name}\nBotdan foydalanish uchun ro'yhatdan o'tishingiz lozim 👇", reply_markup=register_button()[0])
        else:
            await message.answer("Siz asosiy saxifadasiz", reply_markup= create_main_btn())
            await main.menu.set()
    except  Exception as ex:
        await message.answer(ex)



@dp.message_handler(text = "Ro'yhatdan o'tish")
async def bot_start(message: types.Message, state: FSMContext):  
    try:
        await state.finish()  
        full_name = message.from_user.full_name
        user = await db.select_user(telegram_id=message.from_user.id)
        if user is None:
            await message.answer(f"Ismingizni kiriting 👇", reply_markup=back_markup)
            await registration.name.set()
        else:
            await message.answer("kodni kiriting 👇")
            await main.menu.set()
    except  Exception as ex:
        await message.answer(ex)

@dp.message_handler(state=registration.name)
async def name(message: types.Message, state: FSMContext):
    try:
        name = message.text
        telegram_id = message.from_user.id
        if name.isalpha():
            if len(name) >= 3 and len(name) < 15:
                await state.update_data(data={"name": name})
                await state.update_data(data={"telegram" : telegram_id})
                await message.answer("Familiyangizni kiriting 👇", reply_markup=back_markup)
                await registration.surname.set()
            elif len(name) <= 2:
                await message.answer("Ismingiz 2 ta belgidan kam bolmasligi kerak !")

            elif  len(name) >= 21:
                await message.answer("Ismingiz 15 ta belgidan katta bo'lmasligi kerak !")
        else:
            await message.answer("Hurmatli foydalanuvchi ism faqat matn ko'rinishida yozilishi kerak !")
    except  Exception as ex:
        await message.answer(ex)


@dp.message_handler(state = registration.surname)
async def surname(message: types.Message, state: FSMContext):
    try:
        surname = message.text
        if surname.isalpha():
            if len(surname) >= 2 and len(surname) < 15:
                await state.update_data(data={"surname": surname})
                await message.answer("Telefon raqamingizni tugma orqali ulashing 👇", reply_markup=register_button()[1])
                await registration.phone.set()
            elif  len(surname) <= 2:
                await message.answer("Familiyangiz 3 ta belgidan kam bo'lmasligi kerak !")
            elif len(surname) >= 20:
                await message.answer("Familiyangiz 15 ta belgidan ko'p bo'lmasligi kerak !")
        else:
            await message.answer("Familiya faqat matn ko'rinishida yozilishi kerak !")
    except  Exception as ex:
        await message.answer(ex)


@dp.message_handler(content_types = ["contact"], state=registration.phone)
async def phone(message: types.Message, state:FSMContext):
    try:
        contact = message.contact.phone_number
        await state.update_data(data={"phone": contact})
        await message.delete()
        await message.answer("Sizning telefon raqamingiz qabul qilindi", reply_markup=ReplyKeyboardRemove())
        await message.answer("Identifikatsiya uchun rasmingizni tashlang", reply_markup=back_markup)
        await registration.photo.set()
    except Exception as e:
        await message.answer(f"Xatolik yuz berdi {e}")


@dp.message_handler(content_types= ["photo"], state=registration.photo)
async def photo(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        telegram_id = data.get("telegram")
        user = await db.select_fake(telegram_id=telegram_id)
        if user is None:
            photo_id = message.photo[-1].file_id
            username = message.from_user.username
            await state.update_data(data={"username" :username})
            await state.update_data(data={"photo" : photo_id})
            name = data.get("name")
            surname  = data.get("surname")
            phone = data.get("phone")
            await db.add_fake(
                name=name, 
                surname=surname, 
                phone_number=phone, 
                username=username, 
                photo=photo_id,
                telegram_id=telegram_id 
            )
            await bot.send_photo(chat_id=ADMINS[0], photo=photo_id, caption=f"<b>MALUMOTLAR</b>\n\nISM : {name}\n\nFAMILIYA : {surname}\n\nTel. Raqam : {phone}\n\nUsername : @{username}\n\nTelegram_ID : {telegram_id}", reply_markup=confirm_markup)
            await message.delete()
            await message.answer("Malumotlaringiz adminga yuborildi ✅", reply_markup=ReplyKeyboardRemove())
            await registration.change.set()
        else:
            await message.answer("Siz allaqachon sorov yuborgansiz")
    except Exception as e:
        await message.answer(e)



@dp.callback_query_handler(lambda call: call.data in ["Tasdiqlash ✅", "Bekor qilish ❌"], state="*", user_id=ADMINS)
async def confirmation(call: types.callback_query, state: FSMContext):
    try:
        user = await db.select_all_faker()
        user_id = []
        for item in user:
            user_id.append(item[-1])
            break
        conf_user = await db.select_fake(telegram_id=user_id[0])
        data_call= call.data
        if data_call == "Tasdiqlash ✅":   
            await db.add_user(
                name=conf_user[1],
                surname=conf_user[2],
                phone_number=conf_user[3],
                photo=conf_user[4],
                username=conf_user[5],
                account=str(0),
                telegram_id=conf_user[6]
            )
            await bot.copy_message(chat_id=USERS_CHANNEL, from_chat_id=call.message.chat.id, message_id=call.message.message_id)
            await call.message.delete()
            await call.message.answer(f"Ma`lumotlar bazaga muvoffaqiyatli saqlandi ✅")
            await bot.send_message(chat_id=user_id[0], text=f"Xurmatli {conf_user[1]} sizning malumotlaringiz tasdiqlandi ✅", reply_markup=create_change_btn()[0])
            await db.delete_fake(conf_user[6])
            user_id.clear()
        elif data_call == "Bekor qilish ❌":
            await call.message.delete()
            await call.message.answer("Malumotlar bekor qilindi ❌")
            await bot.send_message(chat_id=user_id[0], text='Sizning ma`lumotingiz bekor qilindi ! ❌', reply_markup=create_change_btn()[1])
            await db.delete_fake(conf_user[6])
            user_id.clear()
    except Exception as e:
        await  call.message.answer(str(e))
        


@dp.callback_query_handler(lambda call: call.data in ["0", "1"], state=registration.change)
async def begin(call: types.callback_query, state: FSMContext):
    try:
        if call.data == "0":
            await call.message.answer("Asosiy saxifamizga Xush kelibsiz ✅", reply_markup=create_main_btn())
            await call.message.delete()
            await main.menu.set()
        elif call.data == "1":
            await call.message.answer("Botdan foydalanish uchun ro'yhatdan o'tishingiz lozim 👇", reply_markup=register_button()[0])
            await call.message.delete()
            await state.finish()
    except Exception as e:
        await call.message.answer(str(e))               
