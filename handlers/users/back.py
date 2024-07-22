from aiogram import types
from loader import dp
from states.states import registration, main, admin, generation_code
from aiogram.dispatcher.storage import FSMContext
from keyboards.default.default_keyboards import register_button, back_markup, create_main_btn, create_main_admin, delete_btn, data_btn, add_code



@dp.message_handler(text="🔙 Orqaga", state=registration.name)
async def back(message:  types.Message, state: FSMContext):
    await message.answer("Botdan foydalanish uchun ro'yhatdan o'tishingiz lozim 👇", reply_markup=register_button()[0])
    await state.finish()

@dp.message_handler(text="🔙 Orqaga", state=registration.surname)
async def back(message:  types.Message):
    await message.answer("Ismingizni kiriting 👇", reply_markup=back_markup)
    await registration.name.set()

@dp.message_handler(text="🔙 Orqaga", state=registration.phone)
async def back(message:  types.Message):
    await message.answer("Familiyangizni kiriting 👇", reply_markup=back_markup)
    await registration.surname.set()


@dp.message_handler(text="🔙 Orqaga", state=registration.photo)
async def back(message:  types.Message):
    await message.answer("Telefon raqamingizni ulashing 👇", reply_markup=register_button()[1])
    await registration.phone.set()


@dp.message_handler(text="📤 Chiqish", state=admin.menu)
async def back(message:  types.Message):
    await message.answer("Siz asosiy saxifaga qaytdingiz", reply_markup=create_main_btn())
    await main.menu.set()


@dp.message_handler(text="🔙 Orqaga", state=admin.password)
async def back(message:  types.Message):
    await message.answer("Asosiy saxifaga qaytdingiz !", reply_markup=create_main_btn())
    await main.menu.set()

@dp.message_handler(text="🔙 Orqaga", state=admin.promokod)
async def back(message:  types.Message):
    await message.answer("Qaysi turda qo'shmoqchisiz ?", reply_markup=add_code())
    await admin.change_type_code.set()

@dp.message_handler(text="🔙 Orqaga", state=admin.change_type_code)
async def back(message:  types.Message):
    await message.answer("Bosh saxifaga qaytdingiz !", reply_markup=create_main_admin())
    await admin.menu.set()


@dp.message_handler(text="🔙 Orqaga", state=admin.excel)
async def back(message:  types.Message):
    await message.answer("Qaysi turda qo'shmoqchisiz ?", reply_markup=add_code())
    await admin.change_type_code.set()

@dp.message_handler(text="🔙 Orqaga", state=admin.bal)
async def back(message:  types.Message):
    await message.answer("Promokodni kiriting 👇", reply_markup=back_markup)
    await admin.promokod.set()

@dp.message_handler(text="🔙 Orqaga", state=admin.delete)
async def back(message:  types.Message):
    await message.answer("Bosh saxifaga qaytdingiz !", reply_markup=create_main_admin())
    await admin.menu.set()

@dp.message_handler(text="🔙 Orqaga", state=generation_code.kod)
async def back(message:  types.Message):
    await message.answer("Asosiy saxifaga qaytdingiz !", reply_markup=create_main_btn())
    await main.menu.set()

@dp.message_handler(text="🔙 Orqaga", state=admin.delete_from_id)
async def back(message:  types.Message):
    await message.answer("Qaysi ma'lumotni o'chirmoqchisiz ?", reply_markup=delete_btn())
    await admin.delete.set()


@dp.message_handler(text="🔙 Orqaga", state=admin.user_id)
async def back(message:  types.Message):
    await message.answer("Qaysi turdagi ma'lumotni tekshirmoqchisiz ?", reply_markup=data_btn())
    await admin.data.set()


@dp.message_handler(text="🔙 Orqaga", state=admin.data)
async def back(message:  types.Message):
    await message.answer("Bosh saxifaga qaytdingiz !", reply_markup=create_main_admin())
    await admin.menu.set()

@dp.message_handler(text="🔙 Orqaga", state=admin.update_bal)
async def back(message:  types.Message):
    await message.answer("Bosh saxifaga qaytdingiz !", reply_markup=create_main_admin())
    await admin.menu.set()


@dp.message_handler(text="🔙 Orqaga", state=admin.update)
async def back(message:  types.Message):
    await message.answer("Foydalanuvchining telegram Id sini kiriting 👇", reply_markup=back_markup)
    await admin.update_bal.set()