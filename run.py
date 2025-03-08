import asyncio
import logging
from aiogram import Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State

from handlers.shop import router as shop_router
from handlers.staff import router as staff_router
from handlers.mines import router as mine_router

from database.models import async_main

from config import admin_list, ban_list
from bot import bot

from middlewares.admin import admin_check
from middlewares.ban import ban_check

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Диспетчер
dp = Dispatcher()


# Запуск процесса поллинга новых апдейтов
async def main():
    shop_router.message.middleware(ban_check(ban_list))
    shop_router.callback_query.middleware(ban_check(ban_list))
    staff_router.message.middleware(admin_check(admin_list))
    staff_router.callback_query.middleware(admin_check(admin_list))
    await async_main()
    dp.include_router(mine_router)
    dp.include_router(shop_router)
    dp.include_router(staff_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")