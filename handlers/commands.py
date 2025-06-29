

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from states import BookState, GetBookData
from models import create_data, search_by_user

router = Router()

@router.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer(
        'Добро пожаловать, это бот для бронирования стола в ресторане \n\n'
        'Вот что я умею:\n'
        '/book — забронировать столик\n'
        '/mybooking — посмотреть ваши бронирования'
    )



@router.message(Command('book'))
async def cmd_book(message: Message, state: FSMContext):
    await message.answer('Введите дату бронирования:')
    await state.set_state(BookState.date)


@router.message(BookState.date)
async def process_date(message: Message, state: FSMContext):
    await state.update_data(date=message.text)
    await message.answer('Введите время бронирования:')
    await state.set_state(BookState.time)


@router.message(BookState.time)
async def process_time(message: Message, state: FSMContext):
    await state.update_data(time=message.text)
    await message.answer('Сколько человек будет на бронировании?')
    await state.set_state(BookState.people)


@router.message(BookState.people)
async def process_people(message: Message, state: FSMContext):
    await state.update_data(people=message.text)
    await message.answer('Хотите выбрать столик у окна? (да/нет)')
    await state.set_state(BookState.place)


@router.message(BookState.place)
async def process_place(message: Message, state: FSMContext):
    await state.update_data(place=message.text)
    data = await state.get_data()

    create_data(
        user_id=message.from_user.id,
        date=data['date'],
        time=data['time'],
        people=int(data['people']),
        place=data['place']
    )

    await message.answer('Бронирование успешно создано. Для подтверждения потребуется депозит')
    await state.clear()


@router.message(Command('mybooking'))
async def cmd_mybooking(message: Message, state: FSMContext):
    await message.answer('введите что-нибудь, чтобы посмотреть ваши бронирования:')
    await state.set_state(GetBookData.confirm)


@router.message(GetBookData.confirm)
async def show_bookings(message: Message, state: FSMContext):
    bookings = search_by_user(message.from_user.id)

    if bookings:
        await message.answer('Ваши бронирования:')

        for booking in bookings:
            date = booking[2]
            time = booking[3]
            people = booking[4]
            place = booking[5].strip().lower() if booking[5] else ''
            place_text = 'у окна ' if place == 'да' else 'нет'

            await message.answer(
                f'Дата: {date}\n'
                f'Время: {time}\n'
                f'Людей: {people}\n'
                f'Место: {place_text}'
            )
    else:
        await message.answer('У вас пока нет бронирований')

    await state.clear()
