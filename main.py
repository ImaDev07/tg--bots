import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import commands
from config import TOKEN


async def main():
    logging.basicConfig(level=logging.INFO)
    storage = MemoryStorage()
    bot = Bot(token=TOKEN)
    dp = Dispatcher(storage=storage)

    dp.include_router(commands.router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
