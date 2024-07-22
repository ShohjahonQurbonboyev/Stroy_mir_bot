from aiogram.dispatcher.filters.state import State, StatesGroup




class registration(StatesGroup):
    name = State()
    surname = State()
    phone = State()
    photo = State()
    confirm = State()
    change = State()

class main(StatesGroup):
    menu = State()


class generation_code(StatesGroup):
    kod = State()


class admin(StatesGroup):
    password = State()
    menu = State()
    create_code = State()
    change_type_code = State()
    promokod = State()
    excel = State()
    bal = State()
    delete = State()
    delete_from_id = State()
    data = State()
    user_id = State()
    update_bal = State()
    update = State()