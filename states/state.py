from aiogram.fsm.state import State, StatesGroup

class BookState(StatesGroup):
    date = State()
    time = State()
    people = State()
    place = State()

class GetBookData(StatesGroup):
    confirm = State()
