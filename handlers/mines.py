from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from asyncio import sleep
from database import requests as rq

from keyboards import mines as mine
import keyboards.mines as minekb

import random
import re


class mines(StatesGroup):
    count = State()
    bet = State()

router = Router()


# @router.message(Command("mines"))
# async def cmd_mines(message: Message, state: FSMContext):
#     await message.answer(
#         "Вы выбрали режим мины! Выберите количество бомб", 
#         reply_markup = await mine.mines()
#     )

# @router.callback_query(F.data.startswith("mines_"))
# async def mines_count(callback: CallbackQuery, state: FSMContext):
#     await state.set_state(mines.bet)
#     await state.update_data(count = int(callback.data.split("_")[1]))
#     await callback.message.answer("Введите сумму вашей ставки")
#     await callback.answer()

# @router.message(mines.bet)
# async def mines_bet(message: Message, state: FSMContext):
#     if (re.fullmatch(r'\d+', message.text)):
#         data = await state.get_data()
#         count = data['count']
#         bombs = ""
#         bombs_set = set()
#         while len(bombs_set) < count:
#             bombs_set.add(random.randint(1, 25))
#         for bomb in bombs_set:
#             bombs += f'{bomb}_'
#         moves = ""
#         await message.answer(
#             "Игра началась!",
#             reply_markup = await mine.play_mines(bombs, moves)
#     )
#     else:
#         await message.answer("Введите целое число!")

# @router.callback_query(minekb.mines_moves.filter())
# async def products_pagination_callback(callback: CallbackQuery, callback_data: minekb.mines_moves):
#     bombs = callback_data.bombs
#     moves = callback_data.moves
#     play = callback_data.play
#     if play == "yes":
#         await callback.message.edit_reply_markup(reply_markup=await minekb.play_mines(bombs, moves))
#     elif play == "no":
#         await callback.message.edit_text("Ты проебал лохозавр опущенный", reply_markup = await minekb.play_mines(bombs, moves, play))
#     await callback.answer()