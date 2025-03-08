from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from asyncio import sleep
from config import ban_list

from bot import bot

import re

from database import requests

from database import requests as rq

import keyboards.kb as kb
import keyboards.pagination as pag


router = Router()
class AddCategory(StatesGroup):
    category = State()

class AddItem(StatesGroup):
    category_id = State()
    name = State()
    description = State()
    price = State()

class AddProduct(StatesGroup):
    item_id = State()
    product = State()

class DeleteProduct(StatesGroup):
    item_id = State()
    product_id = State()

class BanUser(StatesGroup):
    user_id = State()

class Mailing(StatesGroup):
    mess = State()

class AnswerAppeal(StatesGroup):
    mess = State()




@router.message(F.text.contains("Staff"))
async def cmd_admin_panel(message: Message):
    await message.answer(
        "Вы вошли в админ панель", 
        reply_markup = kb.admin_panel
    )

@router.message(F.text.contains("Добавить категорию"))
async def cmd_add_category_1(message: Message, state: FSMContext):
    await message.answer(
        "Введите название категории", 
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(AddCategory.category)

@router.message(AddCategory.category)
async def cmd_add_category_2(message: Message, state: FSMContext):
    add_cat = await rq.add_category(message.text)
    if (add_cat):
        await message.answer(
            f'Категория {message.text} успешно добавлена', 
            reply_markup = kb.admin_panel
        )
    else:
        await message.answer(
            f'Категория {message.text} уже существует!', 
            reply_markup = kb.admin_panel
        )
    await state.clear()

@router.message(F.text.contains("Добавить товар"))
async def cmd_add_item(message: Message):
    await message.answer(
        "Выберите название категории, в которую хотите добавить товар", 
        reply_markup=await kb.items_add_categories()
    )

@router.callback_query(F.data.startswith("add_item_"))
async def callback_category(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите название товара")
    await callback.answer()
    await state.update_data(category_id = callback.data.split('_')[2])
    await state.set_state(AddItem.name)

@router.message(AddItem.name)
async def cmd_add_item_1(message: Message, state: FSMContext):
    await state.update_data(name = message.text)
    await message.answer("Введите описание товара")
    await state.set_state(AddItem.description)

@router.message(AddItem.description)
async def cmd_add_item_1(message: Message, state: FSMContext):
    await state.update_data(description = message.text)
    await message.answer("Введите цену товара")
    await state.set_state(AddItem.price)

@router.message(AddItem.price)
async def cmd_add_item_1(message: Message, state: FSMContext):
    if (re.fullmatch(r'\d+', message.text)):
        await state.update_data(price = message.text)
        data = await state.get_data()
        result = await rq.add_item(data['name'], data['description'], int(data['price']), int(data['category_id']))
        if (result):
            await message.answer(f"Вы успешно добавили товар {data['name']}")
        await state.clear()
    else:
        await message.answer("Введите цену товара")

@router.message(F.text.contains("Добавить данные товара"))
async def cmd_add_item(message: Message):
    await message.answer(
        "Выберите название категории, в которую хотите добавить товар", 
        reply_markup=await kb.data_add_categories()
    )

@router.callback_query(F.data.startswith("add_data_category_"))
async def callback_item(callback: CallbackQuery):
    await callback.message.edit_text(
        "Выберите товар, в который хотите загрузить данные", 
        reply_markup=await kb.data_items_categories(int(callback.data.split('_')[3]))
    )
    await callback.answer()

@router.callback_query(F.data.startswith("add_data_item_"))
async def callback_product(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        f"Введите данные товара. Если хотите загрузить несколько, пишите каждый с новой строки. "
        f"Если не хотите ничего добавлять, напишите 0"
    )
    await state.update_data(item_id = callback.data.split('_')[3])
    await state.set_state(AddProduct.product)
    await callback.answer()

@router.message(AddProduct.product)
async def cmd_product_add(message: Message, state: FSMContext):
    if int(message.text) == 0:
        await state.clear()
        await message.answer("Вы вышли из состояния добавления данных")
    else:
        data = (message.text).split()
        prod = await state.get_data()
        await rq.add_product_of_item(int(prod['item_id']), data)
        await state.clear()
        await message.answer(f'{len(data)} товара(ов) успешно загружены.')


@router.message(F.text.contains("Удалить категорию"))
async def cmd_add_item(message: Message):
    await message.answer(
        "Выберите название категории", 
        reply_markup= await kb.delete_categories()
    )


@router.callback_query(F.data.startswith("delete_category_"))
async def callback_item(callback: CallbackQuery):
    await rq.delete_category(int(callback.data.split('_')[2]))
    await callback.message.answer(
        "Категория успешно удалена.", 
        reply_markup = kb.admin_panel
    )
    await callback.answer()

@router.message(F.text.contains("Удалить товар"))
async def cmd_add_item(message: Message):
    await message.answer(
        "Выберите название категории, в которой хотите удалить товар", 
        reply_markup= await kb.delete_items_categories()
    )

@router.callback_query(F.data.startswith("delete_item_category_"))
async def callback_item(callback: CallbackQuery):
    await callback.message.edit_text(
        "Выберите название товара, который хотите удалить", 
        reply_markup= await kb.delete_items(int(callback.data.split('_')[3]))
    )
    await callback.answer()

@router.callback_query(F.data.startswith("delete_item_"))
async def callback_item(callback: CallbackQuery):
    await rq.delete_item(int(callback.data.split('_')[2]))
    await callback.message.answer(
        "Товар успешно удален.", 
        reply_markup = kb.admin_panel
    )
    await callback.answer()



@router.message(F.text.contains("Удалить данные товара"))
async def cmd_add_item(message: Message):
    await message.answer(
        "Выберите название категории", 
        reply_markup= await kb.delete_data_categories()
    )

@router.callback_query(F.data.startswith("delete_data_category_"))
async def callback_item(callback: CallbackQuery, state: FSMContext):
    category_id = int(callback.data.split('_')[3])
    await callback.message.edit_text(
        "Выберите название товара", 
        reply_markup= await kb.delete_data_items(category_id)
    )
    await callback.answer()

@router.callback_query(F.data.startswith("delete_data_item_"))
async def callback_item(callback: CallbackQuery, state: FSMContext):
    item_id = int(callback.data.split('_')[3])
    item_name = await rq.info_item(item_id)
    product_info = await rq.get_products_of_item(item_id)
    text_message = ''
    for info in product_info:
        text_message += f'{info.id}. {info.data}\n'
    await callback.message.answer(f'{item_name[0]}: {item_name[1]} - {item_name[2]} \n{text_message}')
    await callback.message.answer(
        f'Напишите под каким номером находится товар, который вы хотите удалить.'
        f' Если хотите удалить все данные, напишите "all". Если не хотите ничего удалять, напишите 0'
    )
    await state.set_state(DeleteProduct.item_id)
    await state.update_data(item_id = item_id)
    await state.set_state(DeleteProduct.product_id)


@router.message(DeleteProduct.product_id)
async def callback_item(message: Message, state: FSMContext):
    if (re.fullmatch(r'\d+', message.text)):
        if (int(message.text) == 0):
            await state.clear()
            await message.answer(f'Вы вышли из состояния удаления данных.')
        else:
            data = await state.get_data()
            await rq.delete_product(data['item_id'], int(message.text))
            await message.answer(f'Данные под номером {message.text} успешно удалены.')
            await state.clear()
    else:
        if message.text == "all":
            data = await state.get_data()
            await rq.delete_all_product(data['item_id'])
            await message.answer(f'Данные успешно удалены.')
            await state.clear()
        else:
            await message.answer(f'Введите целое число или текст "all"')


@router.message(F.text.contains("Забанить пользователя"))
async def ban_user(message: Message, state: FSMContext):
    await message.answer("Введите telegram_id пользователя")
    state.set_state(BanUser.user_id)

@router.message(BanUser.user_id)
async def ban_user(message: Message, state: FSMContext):
    ban_list.append(int(message.text))
    state.clear()


@router.message(F.text.contains("Обращения"))
async def appeal_user(message: Message, state:FSMContext):
    await message.answer(
        "Обращения пользователей: ", 
        reply_markup = await pag.get_apeals_kb()
    )

@router.callback_query(F.data == "appeals_back")
async def appeal_users(callback: CallbackQuery):
    await callback.message.edit_text(
        "Обращения пользователей: ", 
        reply_markup = await pag.get_apeals_kb()
    )

@router.callback_query(pag.ApealsData.filter())
async def products_pagination_callback(callback: CallbackQuery, callback_data: pag.ApealsData):
    id = callback_data.id
    appeal = await rq.get_apeal_for_id(id)
    
    await callback.message.edit_text(
        f'Обращение от пользователя {appeal.tg_id}\n\n{appeal.appeal}',
        reply_markup=await pag.appeals_handler(appeal.id)
    )
    await callback.answer()

@router.callback_query(F.data.startswith("appeal_answer_"))
async def appeal_answer(callback: CallbackQuery, state: FSMContext):
    appeal_id = int(callback.data.split('_')[2])
    await callback.message.answer("Напишите ответ на обращение.")
    await state.set_state(AnswerAppeal.mess)
    await state.update_data(mess = appeal_id)
    await callback.answer()

@router.message(AnswerAppeal.mess)
async def appeal_answer_2(message: Message, state: FSMContext):
    data = await state.get_data()
    appeal_id = data['mess']
    appeal = await rq.get_apeal_for_id(appeal_id)
    await bot.send_message(appeal.tg_id, message.text)
    await message.answer("Ответ успешно отправлен пользователю.")
    await state.clear()

@router.callback_query(F.data.startswith("appeal_delete_"))
async def del_appeal(callback: CallbackQuery, state: FSMContext):
    appeal_id = int(callback.data.split('_')[2])
    await rq.del_apeal(appeal_id)
    await callback.message.answer("Обращение успешно удалено!")
    await callback.answer()


@router.message(F.text.contains("Рассылка"))
async def mailing_get_text(message: Message, state: FSMContext):
    users = await rq.get_tg_all()
    await message.answer(
        f'Введите сообщение, которое хотите разослать'
    )
    await state.set_state(Mailing.mess)

@router.message(Mailing.mess)
async def mailing_send(message: Message, state: FSMContext):
    users = await rq.get_tg_all()
    for tg in users:
        try:
            await bot.send_message(tg, message.text)
        except Exception:
            print(f"Пользователь {tg} заблокировал бота")
    await message.answer("Рассылка прошла успешно!")
    await state.clear()
